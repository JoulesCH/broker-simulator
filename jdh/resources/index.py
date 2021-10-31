# Installed packages
from operator import pos
from flask import render_template, request, redirect, make_response, jsonify

# Local packages
from utils import debug
import models as m
from . import login_required, not_login_required
from datetime import date
from . import stock_data


@not_login_required
def login():
    if request.method == 'GET': 
        return render_template('login.html')

    next_ = request.args.get('next')
    if str(next_) != 'None':
        response = make_response(redirect(next_))
    else:
        response = make_response(redirect('/'))
    data = request.form
    Equipo = m.Equipo.query.filter(m.Equipo.nombre==data['nombre'], m.Equipo.password==data['password']).first()
    if Equipo:
        cuenta = m.Cuenta.query.filter(m.Cuenta.equipo_id==Equipo.id).first()
        response.set_cookie('token', cuenta.token)
        return response

    return render_template('login.html', error='Código o contraseña inválidos')

@login_required
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('token', '', expires=0)
    return response

@login_required
def index(): 
    cuenta = m.Cuenta.query.filter(m.Cuenta.token==request.cookies.get('token')).first()
    close_values = []
    graficos = []
    for grafico in cuenta.graficos:
        data = stock_data.get(grafico.simbolo)
        close_values.append(data)
        g = grafico.__dict__.copy()
        del g['_sa_instance_state']
        posiciones = []
        for posicion in grafico.posiciones.all():
            posicion = posicion.__dict__.copy()
            del posicion['_sa_instance_state']
            posiciones.append(posicion)
        g['posiciones'] = posiciones
        graficos.append(g)

    return render_template('index.html', cuenta=cuenta, close_values=close_values, graficos=graficos)

@login_required
def tabla():
    cuenta = m.Cuenta.query.filter(m.Cuenta.token==request.cookies.get('token')).first()
    posiciones = []
    for grafico in cuenta.graficos:
        for posicion in grafico.posiciones:
            posiciones.append(posicion)
    return render_template('tabla.html', cuenta=cuenta, posiciones = posiciones)

@login_required
def crear_simbolo():
    data = request.form
    print(data, flush=True)
    # 1 Obtener la cuenta por el token
    cuenta = m.Cuenta.query.filter(m.Cuenta.token==request.cookies.get('token'))  # .first()
    # TODO: VALIDAR VOLUMEN
    for grafico in cuenta.first().graficos:
        if grafico.simbolo == data['simbolo']:
            break
    else:
        # 2 Crear un nuevo grafico
        grafico = m.Grafico(data['simbolo'], cuenta.first())
        m.db.session.add(grafico)
    # 4 Crear la posición
    dia = str(date.today()).replace(' 00:00:00', '')
    posicion = m.Posicion(grafico, data['volumen'], dia, data['valor'], data['comentario_compra'], data['interes'])
    
    # 5 Restar patrimonio
    total = float(data['total'])
    cuenta.update(dict(patrimonio=cuenta.first().patrimonio-total))

    m.db.session.add(posicion)

    m.db.session.commit()
    
    return redirect('/')

