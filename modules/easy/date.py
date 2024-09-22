import time
from datetime import datetime, timedelta


class Date:
    class Taker:
        @staticmethod
        def take_unix():
            return int(time.time())
        
        @staticmethod
        def take_datetime():
            return datetime.now()
        
        @staticmethod
        def take_date():
            return datetime.today().strftime('%d-%m-%y')
        
        @staticmethod
        def take_unix_last_noon():
            now = datetime.now()
            noon_today = now.replace(hour=12, minute=0, second=0, microsecond=0)
            if now >= noon_today:
                return int(noon_today.timestamp())
            else:
                noon_yesterday = noon_today - timedelta(days=1)
                return int(noon_yesterday.timestamp())
        
    class Converter:
        def to_unix(time_str, format = 'full'):
            """format: full"""
            if format == 'full':
                return int(datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S").timestamp())
            
        def from_unix(time_unix, format):
            if format == 'datetime':
                return datetime.fromtimestamp(time_unix).strftime("%Y-%m-%d %H:%M")
            elif format == 'datetime_no_year':
                return datetime.fromtimestamp(time_unix).strftime("%H:%M %d.%m")
            elif format == 'date_no_year':
                return datetime.fromtimestamp(time_unix).strftime("%d.%m")