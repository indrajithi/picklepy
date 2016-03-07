from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
app =  Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'`

moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():    
    return render_template('index.html', current_time=datetime.utcnow())

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



