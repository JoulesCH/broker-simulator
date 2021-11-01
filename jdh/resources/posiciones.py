# Installed packages
from flask import render_template, request

# Local packages
import models as m


def page():
    if 'token' in request.cookies:
        cuenta = m.Cuenta.query.filter(m.Cuenta.token==request.cookies.get('token')).first()
    else:
        cuenta = None
    cuentas = m.Cuenta.query.order_by(m.Cuenta.patrimonio.desc()).all()
    return render_template('posiciones.html', cuentass=cuentas, cuenta=cuenta)
