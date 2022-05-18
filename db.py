from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import application, db

migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()