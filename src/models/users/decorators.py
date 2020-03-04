from functools import wraps

from flask import session, redirect, url_for, request


def requires_login(func):
    @wraps(func)
    def decorator_func(*args,**kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.user_login', next=request.path))
        return func(*args,**kwargs)
    return decorator_func

