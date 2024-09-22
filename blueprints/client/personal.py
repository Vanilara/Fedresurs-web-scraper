from flask import request, session, redirect, render_template, Blueprint
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher

b = Blueprint('personal', __name__)

# DB.BoughtMessages.remake_schema()

@b.route('/')
@error_handler_flask(request)
def index():
    if session.get('logged'):
        return redirect('/personal')
    else:
        return redirect('/demo')

@b.route('/demo')
@error_handler_flask(request)
def demo():
    if session.get('logged'):
        return redirect('/personal')
    messages = {'new': [], 'bought': []}
    regions = DB.Regions.select()
    regions_for_messages = {region.id: region.name for region in regions}
    date_updates = Date.Converter.from_unix(Date.Taker.take_unix_last_noon(), format = 'date_no_year')
    for message in DB.Messages.select({'time': ('<=', Date.Taker.take_unix_last_noon())}, order_by = 'time DESC'):
        region_name = regions_for_messages.get(message.region_id, "Неизвестный регион")
        messages['new'].append({
            'id': message.id,
            'time': Date.Converter.from_unix(message.time, format = 'datetime_no_year'),
            'region': region_name,
            'region_id': message.region_id,
            'company_type': message.company_type
        })
    return render_template('client/demo.html', messages=messages, regions=regions, date_updates = date_updates)

@b.route('/personal')
@error_handler_flask(request)
@decorators.take_user
def personal(user):
    toastr = {'error': session.pop('error', ''), 'success': session.pop('success', '')}
    messages = {'new': [], 'bought': []}
    regions = DB.Regions.select()
    regions_for_messages = {region.id: region.name for region in regions}
    user_messages = DB.BoughtMessages.select({'user_id': user.id}, output_format='array', fields='message_id')
    date_updates = Date.Converter.from_unix(Date.Taker.take_unix_last_noon(), format = 'date_no_year')
    for message in DB.Messages.select({'time': ('<=', Date.Taker.take_unix_last_noon())}, order_by = 'time DESC'):
        if message.id in user_messages:
            continue
        region_name = regions_for_messages.get(message.region_id, "Неизвестный регион")
        messages['new'].append({
            'id': message.id,
            'time': Date.Converter.from_unix(message.time, format = 'datetime_no_year'),
            'region': region_name,
            'region_id': message.region_id,
            'company_type': message.company_type
        })
    for user_message in DB.BoughtMessages.select({'user_id': user.id}, order_by='time DESC'):
        message = DB.Messages.select({'id': user_message.message_id})[0]
        region_name = regions_for_messages.get(message.region_id, "Неизвестный регион")
        messages['bought'].append({
            'id': user_message.id,
            'comp_type': message.company_type,
            'time': Date.Converter.from_unix(message.time, format = 'datetime_no_year'),
            'region': region_name,
            'region_id': message.region_id,
            'link': f'https://fedresurs.ru/sfactmessages/{message.guid}',
            'inn': message.inn,
            'name': message.name,
            'time_bought': Date.Converter.from_unix(user_message.time, format = 'datetime_no_year'),
            'note': user_message.note
        })
    orders = []
    for order in DB.Orders.select({'user_id': user.id}):
        orders.append({
            'time': Date.Converter.from_unix(order.time, format = 'datetime'),
            'card': '**'+order.card,
            'amount': order.amount
        })
    return render_template('client/personal.html', messages=messages, regions=regions, user = user, orders = orders, toastr = toastr,
            date_updates = date_updates)

