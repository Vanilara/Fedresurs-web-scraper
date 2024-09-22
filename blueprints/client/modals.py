from flask import request, session, redirect, render_template, Blueprint
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher

b = Blueprint('modals', __name__)

@b.post('/buy_message')
@error_handler_flask(request)
@decorators.take_user
def buy_message(user):
    message_id = request.form.get('message_id')
    if user.balance < 150:
        session['error'] = 'Недостаточный баналс'
        return redirect('/personal')
    DB.BoughtMessages.insert({'user_id': user.id, 'message_id': message_id, 'time': Date.Taker.take_unix(), 'note': ''})
    DB.Users.update({'balance': user.balance - 150}, {'id': user.id})
    session['success'] = 'Объявление куплено'
    return redirect('/personal')

@b.post('/set_note')
@error_handler_flask(request)
@decorators.take_user
def set_note(user):
    message_id, note = request.form.get('message_id'), request.form.get('note')
    DB.BoughtMessages.update({'note': note}, {'id': message_id})
    return redirect('/personal')

