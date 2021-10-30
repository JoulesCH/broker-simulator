# Installed packages
from flask_sqlalchemy import SQLAlchemy
# Local packages
from . import app


db = SQLAlchemy(app)

from models import *