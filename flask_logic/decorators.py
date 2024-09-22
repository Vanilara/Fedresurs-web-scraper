from functools import wraps
from flask import session, redirect, render_template
from database import DB


def take_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = DB.Users.select({'id': session.get('logged')})
        if user == []:
            return redirect('/')
        kwargs['user'] = user[0]
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') != True:
            return render_template('/admin/auth.html')
        return f(*args, **kwargs)
    return decorated_function