#!/usr/bin/env python

import os
from app import create_app, db
from app.models import User , Role
from flask.ext.script import Manager, Shell
from flask.ext.script import Migrate, MigrateCommand

app= create_app(oa.getenv('FLASK_CONFIG') or 'default')
manager = Manger(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)