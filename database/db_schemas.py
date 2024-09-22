from database.db_helper import Field as F, DataType as dt
from database.db_funcs import SchemaBase


class Web:
    class Requests(SchemaBase):
        TABLE_NAME = 'requests'
        FIELDS = [
            F('email', dt.var),
            F('code', dt.var),
            F('time', dt.int),
            F('is_reg', dt.bool)
        ]

    class Users(SchemaBase):
        TABLE_NAME = 'users'
        FIELDS = [
            F('email', dt.var),
            F('passw', dt.var),
            F('balance', dt.int),
        ]

    class BoughtMessages(SchemaBase):
        TABLE_NAME = 'boughtmessages'
        FIELDS = [
            F('user_id', dt.int),
            F('message_id', dt.int),
            F('time', dt.int),
            F('note', dt.var)
        ]

class Payments:
    class Orders(SchemaBase):
        TABLE_NAME = 'orders'
        FIELDS = [
            F('user_id', dt.int),
            F('time', dt.int),
            F('amount', dt.int),
            F('card', dt.var)
        ]

class Data:
    class Messages(SchemaBase):
        TABLE_NAME = 'messages'
        FIELDS = [
            F('time', dt.int),
            F('guid', dt.var),
            F('number', dt.int),
            F('inn', dt.int),
            F('region_id', dt.int),
            F('name', dt.var),
            F('company_type', dt.var),
            F('published', dt.var),
        ]

    class Regions(SchemaBase):
        TABLE_NAME = 'regions'
        FIELDS = [
            F('code', dt.int),
            F('name', dt.var)
        ]


class DB:
    @staticmethod
    def get_all_schemas():
        return [getattr(DB, attr) for attr in dir(DB) if isinstance(getattr(DB, attr), type) and issubclass(getattr(DB, attr), SchemaBase)]
    
    Requests = Web.Requests
    Users = Web.Users
    BoughtMessages = Web.BoughtMessages
    Orders = Payments.Orders
    Messages = Data.Messages
    Regions = Data.Regions
