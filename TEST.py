import os
from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import redirect
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail
from flask.ext.mail import Message

basedir = os.path.abspath(os.path.dirname(__file__))

app =  Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['PICKLE_MAIL_SUBJECT_PREFIX'] = '[PicklePY]'
app.config['PICKLE_MAIL_SENDER'] = 'Pickle Admin <admin@picklepy.com>'
app.config['PICKLE_ADMIN'] = os.environ.get('PICKLE_ADMIN')


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['PICKLE_MAIL_SUBJECT_PREFIX'] + subject,
                    sender= app.config['PICKLE_MAIL_SENDER'], recipients =[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.body = render_template(template + '.html', **kwargs)
    mail.send(msg)


moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
   
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('What is your name?', validators = [Required()])
    feel = StringField('How are you feeling today?')
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

@app.route('/', methods=['GET', 'POST'])
def index():    
    name = None
    feel = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash('you have added a new user.')
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            
            if app.config['PICKLE_ADMIN']:
                send_email(app.config['PICKLE_ADMIN'], 'New User',
                            'mail/new_user', user=user)

        else:
            session['known'] = True
        
        old_name =  session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        session['feel'] = form.feel.data
        form.feel.data = ''
        return redirect(url_for('index'))

    return render_template('index.html', 
        form=form, name=session.get('name'),
        feel=session.get('feel'), current_time=datetime.utcnow(),
        known = session.get('known', False))


@app.route('/whoami')
def whoami():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your Brouser is %s</p>' % user_agent 

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#@app.errorhandler(500)
#def internal_server_error(e):
 #   return render_template('500.html'), 500

  

if __name__ == '__main__':
    db.create_all()
#    app.run(debug=True)
    manager.run()
#    app.run(port='5004')
#if __name__ == '__main__':
#    db.create_all()
#    app.run(host='0.0.0.0')
#if __name__ == '__main__':
#    db.create_all()
#    manager.run()




