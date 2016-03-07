from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import Flask, render_template, session, redirect, url_for
app =  Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

class NameForm(Form):
    name = StringField('What is your name?', validators = [Required()])
    feel = StringField('How are you feeling today?')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():    
    name = None
    feel = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
       # form.name.data = ''
        session['feel'] = form.feel.data
       # form.feel.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),feel=session.get('feel'), current_time=datetime.utcnow())

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
    app.run(debug=True)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')



