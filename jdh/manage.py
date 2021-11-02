from core import app, database
#from core.database import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os


migrate = Migrate(app, database.db, directory=os.getenv('MIGRATE_FOLDER', 'migrations_prod/'))
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()