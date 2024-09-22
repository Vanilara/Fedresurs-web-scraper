from flask import request, session, redirect, render_template, Blueprint
from flask_logic import decorators
from database import DB
from modules.fails_handler.logging_bot import error_handler_flask
from modules import Randomizer, Date, EmailSender, Hasher

b = Blueprint('auth', __name__)


def handle_auth_route(template_name, additional_conditions=None, **extra_params):
    if session.get('logged'):
        return redirect('/personal')
    message = session.pop('message', '')
    render_params = {'message': message, **extra_params}
    if additional_conditions:
        condition_result = additional_conditions['condition']() if 'condition' in additional_conditions and callable(additional_conditions['condition']) else True
        redirect_path = additional_conditions.get('redirect', '/')
        if not condition_result:
            return redirect(redirect_path)
    return render_template('auth/tmps/' + template_name, **render_params)

@b.route('/login')
@error_handler_flask(request)
def auth_login():
    return handle_auth_route('login.html')

@b.route('/reg')
@error_handler_flask(request)
def auth_reg():
    return handle_auth_route('reg.html')

@b.route('/reset')
@error_handler_flask(request)
def auth_reset():
    return handle_auth_route('reset.html')

@b.route('/code')
@error_handler_flask(request)
def auth_code():
    additional_conditions = {'redirect': '/reg', 'condition': lambda: session.get('email')}
    return handle_auth_route('code.html', additional_conditions=additional_conditions, email = session.get('email'))

@b.route('/passw')
@error_handler_flask(request)
def auth_passw():
    additional_conditions = {'redirect': '/reg', 'condition': lambda: session.get('email')}
    return handle_auth_route('passw.html', additional_conditions=additional_conditions)

#Here logic auth
@b.post('/reg_action')
@error_handler_flask(request)
def auth_action_reg():
    email = request.form.get('email')
    if email == None:
        return redirect('/reg')
    if DB.Users.select({'email': email}) == []:
        code = Randomizer.randint(100000, 999999)
        DB.Requests.delete({'email': email})
        DB.Requests.insert({'email': email, 'code': code, 'time': Date.Taker.take_unix(), 'is_reg': True})
        EmailSender.send_code(code, email)
    session['email'] = email
    return redirect('/code')

@b.post('/code_action')
@error_handler_flask(request)
def auth_action_code():
    if not session.get('email'):
        return redirect('/reg')
    code = request.form.get('code').strip()
    user = DB.Requests.select({'email': session.get('email')})
    if user == []:
        return redirect('/reg')
    if code != user[0].code:
        session['message'] = 'Код не подходит'
        return redirect('/code')
    if Date.Taker.take_unix() - user[0].time > 1*24*60*60:
        session['message'] = 'Прошло более 24 часов с отправки кода'
        return redirect('/code')
    session['code_ok'] = True
    return redirect('/passw')

@b.post('/passw_action')
@error_handler_flask(request)
def auth_action_passw():
    if not session.get('email'):
        return redirect('/reg')
    if session.get('code_ok') is not True:
        return redirect('/code')
    passw_one, passw_two = request.form.get('passw_one'), request.form.get('passw_two')
    if passw_one != passw_two:
        return render_template('auth/tmps/passw.html', message='Пароли не совпадают')
    if len(passw_one) < 8:
        return render_template('auth/tmps/passw.html', message='Пароль должен быть минимум 8 символов')
    user = DB.Requests.select({'email': session.get('email')})[0]
    if user.is_reg == True:
        id = DB.Users.insert({'email': session.get('email'), 'passw': Hasher.hash(passw_one), 'balance': 1000})
    elif user.is_reg == False:
        id = DB.Users.select({'email': user.email})[0].id
        DB.Users.update({'passw': Hasher.hash(passw_one)}, {'id': id})
    DB.Requests.delete({'email': session.get('email')})
    session['logged'] = id
    session.pop('email')
    return redirect('/personal')

@b.post('/login_action')
@error_handler_flask(request)
def auth_action_login():
    email, passw = request.form.get('email'), request.form.get('passw')
    if email == None or passw == None:
        session['message'] = 'Заполните форму'
        return redirect('/login')
    user = DB.Users.select({'email': email})
    if user == []:
        session['message'] = 'Почта или пароль не подходят'
        return redirect('/login')
    if Hasher.check(passw.encode('utf-8'), user[0].passw) == False:
        session['message'] = 'Почта или пароль не подходят'
        return redirect('/login')
    session['logged'] = user[0].id
    return redirect('/personal')

@b.post('/reset_action')
@error_handler_flask(request)
def auth_action_reset():
    email = request.form.get('email')
    if email == None:
        return redirect('/reg')
    if DB.Users.select({'email': email}) != []:
        code = Randomizer.randint(100000, 999999)
        DB.Requests.delete({'email': email})
        DB.Requests.insert({'email': email, 'code': code, 'time': Date.Taker.take_unix(), 'is_reg': False})
        session['email'] = email
        EmailSender.send_code(code, email)
    return redirect('/code')


@b.post('/logout')
@error_handler_flask(request)
def logout():
    session.pop('logged', None)
    return redirect('/login')
