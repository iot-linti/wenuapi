from eve import Eve
from flask import abort
from models.user import User
from models.role import Role
from flask import current_app as app
from sqlalchemy.orm.exc import NoResultFound

def add_token(docs):
    '''
    Respuesta al evento que se dispara al agregar un nuevo usuario.
    Se usa para evitar que el token se agregue como un campo vacio
    '''
    for doc in docs:
        username = doc['username']
        token = User.generate_token(username)
        doc['token'] = token


def add_role(docs):
    '''
    Respuesta al evento que se dispara despues de agregar un nuevo usuario.
    Verifica que exista el rol User y se lo agrega al usuario.
    '''
    session = app.data.driver.session
    role = Role.set_Role('user',session)

    for doc in docs:
        username = doc['username']
        try:
            user = session.query(User).filter(User.username == username).one()
        except NoResultFound:
            print 'No esta'
        else:
            user.roles.append(role)
            session.commit()


def set_on_insert_account_token(app):
    '''
    Se llama desde core, agrega las respuestas a los eventos.
    Usa EVE event hooks.
    '''
    app.on_insert_user += add_token
    app.on_inserted_user += add_role

