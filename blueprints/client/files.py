from flask import request, session, redirect, render_template, Blueprint, send_file
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher

b = Blueprint('files', __name__)

@b.route('/user_accept')
@error_handler_flask(request)
def user_accept():
    return send_file('static/files/user_accept.pdf')

@b.route('/pers_data')
@error_handler_flask(request)
def pers_data():
    return send_file('static/files/pers_data.pdf')

