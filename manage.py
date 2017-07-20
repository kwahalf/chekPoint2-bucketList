# manage.py

import os
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
import unittest

from app import create_app
from app.bucketlist_api import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, models.db)  # initialize migrate with your app and database
manager = Manager(app)  # script manager

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def db_reset():
    models.db.drop_all()
    models.db.create_all()



if __name__ == '__main__':
    manager.run()  # starting the script manager
