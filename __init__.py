import sqlalchemy


def testdb():
    engine = sqlalchemy.create_engine('sqlite:///')
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    return (engine, session)
