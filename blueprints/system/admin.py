from flask import request, session, redirect, render_template, Blueprint, send_file, after_this_request
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher, Excel
from config import Config
import uuid

b = Blueprint('admin', __name__)

@b.route('/admin')
@error_handler_flask(request)
def admin():
    is_admin = session.get('is_admin')
    if is_admin:
        return render_template('/admin/main.html')
    else:
        return render_template('/admin/auth.html')

@b.post('/admin_login')
@error_handler_flask(request)
def admin_login():
    is_admin = session.get('is_admin')
    if is_admin:
        return redirect('/admin')
    else:
        if request.form.get('key') == Config.Flask.ADMIN_KEY:
            session['is_admin'] = True
            return redirect('/admin')
        else:
            return render_template('/admin/auth.html')

@b.post('/download_users')
@decorators.admin_required
@error_handler_flask(request)
def download_users():
    def make_users():
        users = []
        for user in DB.Users.select():
            amount_spend = 0
            orders = DB.Orders.select({'user_id': user.id})
            for order in orders:
                amount_spend += order.amount
            users.append([user.email, user.balance, amount_spend, len(orders)])
        return users

    user_filename = f'Пользователи {Date.Taker.take_date()}.xlsx'
    server_filename = f'Пользователи {Date.Taker.take_date()}_{uuid.uuid4()}.xlsx'
    users = make_users()
    cols, rows = ['Почта', 'Баланс', 'Всего пополнений', 'Количество пополнений'], users
    filepath = Excel.make_excel(user_filename, server_filename, rows, cols)

    @after_this_request
    def remove_file_after(response):
        Excel.delete_file(filepath)
        return response
    return send_file(filepath, as_attachment=True, download_name=user_filename)

