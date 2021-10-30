
# Builtin packages
import string
import random
from models import *

letters = string.ascii_lowercase  + string.digits

prefix = 'Equipo '

def random_str(n):
    return ''.join(random.choice(letters) for i in range(n))

for i in range(1, 15):
    equipo = Equipo(prefix+str(i), random_str(3), random_str(4))
    cuenta = Cuenta(random_str(10), equipo, 1000000)
    db.session.add(equipo)
    db.session.add(cuenta)
    db.session.commit()

equipo = Equipo('root', '123as', 'dd')
cuenta = Cuenta(random_str(10), equipo, 1000000)
db.session.add(equipo)
db.session.add(cuenta)
db.session.commit()

