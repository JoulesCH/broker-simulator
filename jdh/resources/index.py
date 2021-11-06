# Installed packages
from operator import pos
from flask import render_template, request, redirect, make_response, jsonify

# Local packages
from utils import debug
import models as m
from . import login_required, not_login_required
# from datetime import date
from . import stock_data
from utils.symbols import symbols
from resources import datenow


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
    Equipo = m.Equipo.query.filter(m.Equipo.nombre == data['nombre'], m.Equipo.password == data['password']).first()
    if Equipo:
        cuenta = m.Cuenta.query.filter(m.Cuenta.equipo_id == Equipo.id).first()
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
    cuenta_u = m.Cuenta.query.filter(m.Cuenta.token == request.cookies.get('token'))  # .first()
    cuenta = cuenta_u.first()
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

    dia_semana_actual = datenow.day_of_week()
    if dia_semana_actual != cuenta.ult_movimiento and cuenta.ult_movimiento != -1:
        cuenta_u.update({'mov_disponibles': max(0,cuenta.mov_disponibles - 1), 'ult_movimiento': -1})
        m.db.session.commit()
    
    # Validar que sea entre semana y en el horario fuera de 6am a 4pm
    hora_actual = int(datenow.hour())
    puede_hora = False

    if hora_actual < 6 or hora_actual > 15 or dia_semana_actual == 6 or dia_semana_actual == 7:
        puede_hora = True

    return render_template('index.html', 
        cuenta=cuenta, close_values=close_values, 
        graficos=graficos, symbols=symbols,
        puede_hora=puede_hora, currency=stock_data.currency()
    )


@login_required
def tabla():
    cuenta = m.Cuenta.query.filter(m.Cuenta.token == request.cookies.get('token')).first()
    posiciones = []
    for grafico in cuenta.graficos:
        for posicion in grafico.posiciones:
            posiciones.append(posicion)
    return render_template('tabla.html', cuenta=cuenta, posiciones=posiciones)


@login_required
def vender_simbolo():
    data = request.form
    # 1 0btener la cuenta por el token
    cuenta_u = m.Cuenta.query.filter(m.Cuenta.token == request.cookies.get('token'))  # .first()
    cuenta = cuenta_u.first()
    # 2 Buscar la posicion
    posicion_u = m.Posicion.query.filter(m.Posicion.id == data['operacion_id'])
    posicion = posicion_u.first()
    # 3 Actualizar valores de:
    # dia_venta
    # valor_venta
    # comentario_venta
    # interes_venta
    # balance
    # cerrado
    valores_actualiar = dict(
        dia_venta=datenow.today(),
        valor_venta=data['valor_venta'],
        comentario_venta=data['comentario_venta'],
        interes_venta=data['interes_venta'],
        balance=data['beneficio'],
        cerrado=True
    )
    posicion_u.update(valores_actualiar)
    # 4 Actualizar valores de patrimonio
    valores_actualiar = dict(
        patrimonio=cuenta.patrimonio - float(data['interes_venta']) + posicion.volumen * float(data['valor_venta']),
        ult_movimiento=datenow.day_of_week(),
        no_movimientos=cuenta.no_movimientos + 1,
        beneficio_total=cuenta.beneficio_total + posicion.volumen*(float(data['valor_venta']) - posicion.valor_compra),
        balance = cuenta.balance - posicion.volumen*float(data['valor_venta']),
        beneficio = cuenta.beneficio - posicion.volumen*(float(data['valor_venta']) - posicion.valor_compra)
    )
    cuenta_u.update(valores_actualiar)
    m.db.session.commit()
    return redirect('/')


@login_required
def crear_simbolo():
    data = request.form
    print(data, flush=True)
    # 1 Obtener la cuenta por el token
    cuenta_u = m.Cuenta.query.filter(m.Cuenta.token == request.cookies.get('token'))  # .first()
    cuenta = cuenta_u.first()
    # TODO: VALIDAR VOLUMEN
    for grafico in cuenta.graficos:
        if grafico.simbolo == data['simbolo']:
            break
    else:
        # 2 Crear un nuevo grafico
        grafico = m.Grafico(data['simbolo'], cuenta)
        m.db.session.add(grafico)
    # 4 Crear la posición
    dia = datenow.today()
    posicion = m.Posicion(grafico, data['volumen'], dia, data['valor'], data['comentario_compra'], data['interes'])

    # 5 Restar patrimonio
    total = float(data['total'])
    cuenta_u.update(
        dict(
            no_movimientos=cuenta.no_movimientos + 1, 
            patrimonio=cuenta.patrimonio - total,
            ult_movimiento=datenow.day_of_week(),
            balance=cuenta.balance + float(data['volumen'])*float(data['valor'])
        )
    )

    m.db.session.add(posicion)

    m.db.session.commit()

    return redirect('/')
