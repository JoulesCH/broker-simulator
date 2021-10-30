from core.database import db

class Equipo(db.Model):
    __tablename__ = 'equipos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    nombre = db.Column(db.String, nullable=False)
    codigo = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, nombre, codigo, password):
        self.nombre = nombre
        self.codigo = codigo
        self.password = password


class Cuenta(db.Model):
    __tablename__ = 'cuentas'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    token = db.Column(db.String, nullable=True)

    equipo_id = db.Column(db.BigInteger, db.ForeignKey('equipos.id'))
    equipo = db.relationship("Equipo")

    patrimonio = db.Column(db.Float, nullable=True)
    balance = db.Column(db.Float, nullable=True)
    beneficio = db.Column(db.Float, nullable=True)
    mov_disponibles = db.Column(db.Integer, nullable = True)

    graficos =  db.relationship("Grafico", backref="cuenta_grafico", lazy='dynamic')

    def __init__(self, token, equipo, patrimonio):
        self.token = token
        self.equipo = equipo
        self.patrimonio = patrimonio
        self.balance = 0
        self.beneficio = 0
        self.mov_disponibles = 2

class Grafico(db.Model):
    __tablename__ = 'graficos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    cuenta_id = db.Column(db.BigInteger, db.ForeignKey('cuentas.id'))
    cuenta = db.relationship("Cuenta")

    simbolo = db.Column(db.String)
    mov_disponibles = db.Column(db.Integer, nullable = True)

    posiciones =  db.relationship("Posicion", backref="grafico_posicion", lazy='dynamic')

    def __init__(self, simbolo, cuenta):
        self.simbolo = simbolo
        self.cuenta = cuenta
        self.cuenta_id = cuenta.id

class Posicion(db.Model):
    __tablename__ = 'posiciones'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    grafico_id = db.Column(db.BigInteger, db.ForeignKey('graficos.id'))
    grafico = db.relationship("Grafico")

    volumen = db.Column(db.Float)

    # Compra
    dia_compra = db.Column(db.String)
    valor_compra = db.Column(db.Float)
    comentario_compra = db.Column(db.String)
    interes_compra = db.Column(db.Float)

    # Venta
    dia_venta = db.Column(db.String)
    valor_venta = db.Column(db.Float)
    comentario_venta = db.Column(db.String)
    interes_venta = db.Column(db.Float)

    balance = db.Column(db.Float)
    cerrado = db.Column(db.Boolean)

    def __init__(self, grafico, volumen, dia, valor, comentario, interes):
        self.grafico = grafico
        self.grafico_id = grafico.id
        self.volumen = volumen
        self.dia_compra = dia
        self.valor_compra = valor
        self.comentario_compra = comentario
        self.interes_compra = interes
        self.balance = 0
        self.cerrado = False
        