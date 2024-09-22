from fake_useragent import UserAgent
import requests, json
from database import DB
from modules import Date
import traceback
from modules.fails_handler.logging_bot import error_send_func


class Headers:
    ua = UserAgent()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://fedresurs.ru/search/entity',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
    }

    def make(self, referer):
        return {**self.headers, 'User-Agent': self.ua.random, 'Referer': referer}

class Parser:
    def __init__(self):
        self.s = requests.session()
        self.headers = Headers()

    def take_regions(self):
        """Returns array of json's: {code, description}"""
        headers = self.headers.make('https://fedresurs.ru/entities')
        return json.loads(self.s.get('https://fedresurs.ru/backend/reference-book/regions', headers = headers).text)

    def take_comps(self, type, offset = 0, region_number = None, inn = None):
        headers = self.headers.make('https://fedresurs.ru/entities')
        params = {'limit': 15, 'offset': offset, 'isActive': 'true'}
        if region_number != None:
            params.update({'regionNumber': region_number})
        if inn != None:
            params.update({'searchString': inn})
        return json.loads(self.s.get(f'https://fedresurs.ru/backend/{type}', headers = headers, params = params).text)
    
    def take_messages(self, guid, type, message_type = 'bankrupt'):
        headers = self.headers.make(f'https://fedresurs.ru/{type}/{guid}')
        params = {
            'limit': '15',
            'offset': '0',
        }
        if message_type == 'bankrupt':
            params.update({'onlySfact': 'true', 'group': '4'})
        return json.loads(self.s.get(f'https://fedresurs.ru/backend/{type}/{guid}/publications', headers = headers, params = params).text)
        
    def take_message(self, guid):
        headers = self.headers.make(f'https://fedresurs.ru/sfactmessages/{guid}')
        return json.loads(self.s.get(f'https://fedresurs.ru/backend/sfact-messages/{guid}', headers = headers).text)

class Iterator:
    def __init__(self, time_last_parse):
        self.time_last_parse = time_last_parse
        self.parser = Parser()

    def check_is_region_stop(self, comps, type):
        comps.reverse()
        for comp in comps:
            messages = self.parser.take_messages(comp['guid'], type = type, message_type = 'all')
            if messages['found'] == 0:
                continue
            message_date = messages['pageData'][0]['datePublish'].split('.')[0]
            if Date.Converter.to_unix(message_date) < self.time_last_parse:
                return True
            break
        return False
    
    def check_messages(self, messages_short, comp, type):
        data = []
        for message_short in messages_short['pageData']:
            if message_short['isAnnulled'] == True or message_short['isLocked'] == True:
                continue
            info = {
                'guid': message_short['guid'],
                'time': Date.Converter.to_unix(message_short['datePublish'].split('.')[0]),
                'number': message_short['number'],
            }
            if info['time'] < self.time_last_parse:
                continue
            if message_short['type'].startswith('Намерение'):
                message = self.parser.take_message(message_short['guid'])
                if message_short['type'].startswith('Намерение кредитора'):
                    debtor = message['content']['debtor']
                    published, inn = 'creditor', debtor['inn']
                    if type == 'persons':
                        if 'ogrnip' not in debtor:
                            continue
                        name = debtor['fio']
                    else:
                        if len(debtor['inn']) != 10:
                            continue
                        name = debtor['shortName']
                elif message_short['type'].startswith('Намерение должника'):
                    inn, name, published = comp['inn'], comp['name'], 'debtor'
                    if type == 'persons':
                        if 'individualEntrepreneurInfo' not in comp:
                            continue
                        is_debtor = False
                        for participant in message_short['participants']:
                            if participant == message_short['publisher']:
                                is_debtor = True
                        if is_debtor == False:
                            continue
                    else:
                        if message['content']['publisherInfo']['inn'] != inn:
                            continue
                if type == 'persons':
                    company_type = 'ИП'
                else:
                    if comp['name'] == name:
                        company_type = comp['name'].replace('"', ' ').split(' ')[0]
                    else:
                        company_name = self.parser.take_comps(type = 'companies', inn = inn)['pageData'][0]['name']
                        company_type = company_name.replace('"', ' ').split(' ')[0]
                info.update({'inn': inn, 'region': inn[0:2], 'name': name, 'company_type': company_type, 'published': published})
                data.append(info)
        return data
    
    def iterate_companies(self):
        type = 'companies'
        data = []
        regions = self.parser.take_regions()
        k = 0
        for region in regions:
            k += 1
            iterate = True
            offset = 0
            while iterate:
                try:
                    comps = self.parser.take_comps(region_number = region['code'], offset = offset, type = type)
                    for comp in comps['pageData']:
                        messages_short = self.parser.take_messages(comp['guid'], type = type)
                        data += self.check_messages(messages_short, comp, type)
                    if self.check_is_region_stop(comps['pageData'], type = type) or offset + 15 >= 500:
                        iterate = False
                    offset += 15
                except Exception as e:
                    error_send_func(e=e, info_message=f'При парсинге', level='warning')
                    print(region)
                    traceback.print_exc()
                    break
        print(f'{type}. Parsed: {len(data)}')
        return data, regions
    
    def iterate_persons(self):
        data = []
        type = 'persons'
        iterate = True
        offset = 0
        while iterate:
            try:
                persons = self.parser.take_comps(offset = offset, type = type)
                for person in persons['pageData']:
                    messages_short = self.parser.take_messages(person['guid'], type = type)
                    data += self.check_messages(messages_short, person, type)
                if offset + 15 >= 500:
                    iterate = False
                offset += 15
            except Exception as e:
                error_send_func(e=e, info_message=f'При парсинге', level='warning')
                traceback.print_exc()
                break
        print(f'{type}. Parsed: {len(data)}. Offset: {offset}')
        return data
    
class Inserter:
    @staticmethod
    def insert_regions(regions):
        db_regions = DB.Regions.select(fields='code', output_format='array')
        for region in regions:
            if int(region['code']) not in db_regions:
                DB.Regions.insert({'code': region['code'], 'name': region['description'].replace(' - город федерального значения', '')})

    @staticmethod
    def insert_messages(messages):
        for message in messages:
            if DB.Messages.select({'number': message['number']}) == []:
                message['region_id'] = DB.Regions.select({'code': message['region']})[0].id
                del message['region']
                DB.Messages.insert(message)

def main():
    iterator = Iterator(Date.Taker.take_unix() - 60*60*3)
    persons = iterator.iterate_persons()
    Inserter.insert_messages(persons)
    comps, regions = iterator.iterate_companies()
    Inserter.insert_regions(regions)
    Inserter.insert_messages(comps)

if __name__ == '__main__':
    print('started', Date.Taker.take_datetime())
    try:
        main()
    except Exception as e:
        error_send_func(e=e, info_message=f'При парсинге')
        traceback.print_exc()

    

        


