import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)  # it is used to keep original name and documentation of function as decorator overrides
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in for this page.', 'danger')
            return redirect(url_for('users.login_user'))  # redirect to users.login_user function instead of HTML
        return f(*args, **kwargs)
    return decorated_function  # without () = to return the decorator function itself, not the execution


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function
