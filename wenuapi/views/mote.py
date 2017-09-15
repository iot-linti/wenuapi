from flask import (
    current_app as app,
    render_template,
    Response,
    send_file,
    request,
    redirect,
    url_for,
)

from ..models.mote import Mote
from ..models.forms.mote import MoteForm

def get_mote_list():
    session = app.data.driver.session
    all_mote = session.query(Mote).all()
    return render_template('all_motes.html', all_mote=all_mote)  

def mote_add():
    session = app.data.driver.session
    form = MoteForm(request.form)
    if request.method == 'POST' and form.validate():
        mote = Mote()
        mote.level_id = form.level_id.data
        mote.mote_id = form.mote_id.data
        mote.resolution = form.resolution.data
        mote.x = form.x.data
        mote.y = form.y.data
        session.add(mote)
        session.commit()
        return redirect(url_for('get_mote_list'))
    return render_template('add_mote.html', form=form)
        

def mote_update(mote_id):
    session = app.data.driver.session
    mote = session.query(Mote).get(mote_id)
    form = MoteForm(obj=mote)
    if request.method == 'POST' and form.validate():
        form = MoteForm(request.form)
        mote.level_id = form.level_id.data
        mote.mote_id = form.mote_id.data
        mote.resolution = form.resolution.data
        mote.x = form.x.data
        mote.y = form.y.data
        session.commit()
        return redirect(url_for('get_mote_list'))
    return render_template('add_mote.html', form=form)

def mote_delete(mote_id):
    session = app.data.driver.session
    mote = session.query(Mote).get(mote_id)
    if request.method == 'POST':
        session.delete(mote)
        session.commit()
        return redirect(url_for('get_mote_list'))
    return render_template('delete_mote.html')


def init_mote_app(app):
    app.route('/mote/list', methods=['GET'])(get_mote_list)
    app.route('/mote/add', methods=['GET','POST'])(mote_add)
    app.route('/mote/update/<string:mote_id>', methods=['GET','POST'])(mote_update)
    app.route('/mote/delete/<string:mote_id>', methods=['GET','POST'])(mote_delete)
