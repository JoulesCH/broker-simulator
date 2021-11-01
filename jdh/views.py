# Local packages
from core import app

  
from resources import index

app.route('/')(index.index)
app.route('/login', methods=["GET", "POST"])(index.login)
app.route('/logout', methods=["POST"])(index.logout)
app.route('/crear_simbolo', methods=["POST"])(index.crear_simbolo)
app.route('/tabla')(index.tabla)
app.route('/vender_simbolo', methods=["POST"])(index.vender_simbolo)

from resources import stock_data

app.route('/stock_data', methods=["POST"])(stock_data.get)

from resources import posiciones

app.route('/posiciones')(posiciones.page)
