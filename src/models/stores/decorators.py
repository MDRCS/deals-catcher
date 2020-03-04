from functools import wraps

from flask import session,render_template

from src.config import ADMINS

def requires_admin_permission(func):
    @wraps(func)
    def decorator_function(*args,**kwargs):
        if session['email'] not in ADMINS:
            return render_template('home.html')
        return func(*args,**kwargs)
    return decorator_function
