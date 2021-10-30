# Installed packages
from flask import Flask

# Built-in packages
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Database config for psgl
DATABASE_URL = os.getenv('DATABASE_URL')
if 'postgresql' not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

import views
from . import database