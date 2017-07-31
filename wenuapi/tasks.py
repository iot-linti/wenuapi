from eve import Eve
from flask import abort
from models.user import User
from models.role import Role
from flask import current_app as app
from sqlalchemy.orm.exc import NoResultFound

def add_token(docs):
    for doc in docs:
        username = doc['username']
        token = User.generate_token(username)
        doc['token'] = token


def add_role(docs):

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

    app.on_insert_user += add_token
    app.on_inserted_user += add_role

