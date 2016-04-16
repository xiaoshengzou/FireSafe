
import os
from app import create_app, db
from app.models import User, Role, MainStation, SonModel
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.getDataThread import WriteThread

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate  = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role,MainStation=MainStation,SonModel=SonModel)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command 
def depoly():
        """Run deployment tasks."""
        from flask.ext.migrate import upgrade
        from app.models import Role, User
        #migrate database to latest revision
        #upgrade()
        db.drop_all()
        db.create_all()
        Role.insert_roles()
        MainStation.insert_com()
        u = User(email='kobe@www.com',username='kobe',password='cat')
        z = User(email='zou@www.com',username='zou',password='cat')
        x = SonModel(name='7d',slaveaddress=1,location='7d',sensorsNumber=3)
        db.session.add_all([u, z, x])
        db.session.commit()


if __name__ == '__main__':

        # task1 = WriteThread(app, 3)
        # task1.start()
        #app.run(debug=True)
        
        manager.run()
