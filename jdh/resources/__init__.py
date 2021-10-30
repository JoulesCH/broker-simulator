# Installed packages
from flask import  request, redirect


def login_required(function):
    def check_login(*args, **kwargs):
        if 'token' not in request.cookies:
            return redirect(f'/login?next={request.path}')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_login.__name__ = function.__name__
    return check_login


def not_login_required(function):
    def check_not_login(*args, **kwargs):
        if 'loggedIn' in request.cookies or 'token' in request.cookies:
            return redirect('/')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_not_login.__name__ = function.__name__
    return check_not_login
