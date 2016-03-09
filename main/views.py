from datetime import datetime
from flask import render_template, session, url_for
from . import main
from .forms import Nameform
from .. import db
from ..models import User

@main.route('/', methords=['GET', 'POST'])
def index():
    form = Nameform()
    if form.validate_on_submit():
        #...
        return redirect(url_for('.index'))
    return render_template('index.html',
                            form=form, name=session.get('name'),
                            known=session.get('known',False),
                            current_time=datetime.utcnow())
    
