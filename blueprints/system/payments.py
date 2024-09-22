from flask import request, session, redirect, render_template, Blueprint
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher
from config import Config

b = Blueprint('payments', __name__)

@b.post('/add_balance')
@error_handler_flask(request)
@decorators.take_user
def personal(user):
    amount = request.form.get('amount')
    return render_template('/payment.html', amount = amount, user_id = user.id, email = user.email, cloud_token = Config.Cloud.TOKEN)

@b.post('/hook_paid')
@error_handler_flask(request)
def hook_paid():
    data = request.form.to_dict()
    user_id, amount = int(data['AccountId']), int(float(data['Amount']))
    user = DB.Users.select({'id': user_id})[0]
    DB.Users.update({'balance': user.balance + amount}, {'id': user.id})
    DB.Orders.insert({'user_id': user.id, 'time': Date.Taker.take_unix(), 'amount': amount, 'card': data['CardLastFour']})
    return {'code': 0}

