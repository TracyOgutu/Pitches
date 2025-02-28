from app import create_app,db
from flask_script import Manager,Server
from app.model import User,Role,Pitch,Comment,Upvote,Downvote
from flask_migrate import Migrate,MigrateCommand

#creating app instance
app = create_app('development')
# app = create_app('test')

manager=Manager(app)

manager.add_command('server',Server)
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Pitch=Pitch,Comment=Comment,Upvote=Upvote,Downvote=Downvote)



if __name__ == '__main__':
    manager.run()