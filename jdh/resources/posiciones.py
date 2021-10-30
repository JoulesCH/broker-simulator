# Installed packages
from flask import render_template, request, redirect, make_response

# Local packages
from utils import debug
import models as m
from . import login_required, not_login_required
from datetime import date
from . import stock_data


def page():
    if 'token' in request.cookies:
        cuenta = m.Cuenta.query.filter(m.Cuenta.token==request.cookies.get('token')).first()
    else:
        cuenta = None
    cuentas = m.Cuenta.query.order_by(m.Cuenta.patrimonio.desc()).all()
    return render_template('posiciones.html', cuentass=cuentas, cuenta=cuenta)
