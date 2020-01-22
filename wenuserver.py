#!/usr/bin/env python
'''Main script and WSGI module to run the server.bin
Normally this module may be loaded from a WSGI server.import
In maintainance mode it can be used as a script to cleanup the
database with the argument --reset-database or to set a new
admin password with --set-admin.
It can be run with the --disable-auth parameter to do local
tests without authentication or to reset the admin password.'''
import argparse
import getpass
import sys
import wenuapi.core
from wenuapi.models.common import Base
from wenuapi.models.user import User

def build_parser():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('-s', '--serve', action='store_true', default=True)
    mode.add_argument('--reset-database', action='store_true')
    mode.add_argument('--set-admin', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--disable-auth', action='store_true')
    parser.add_argument('-a', '--addr', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=8080)
    return parser


def main(args, session=None):
    app = wenuapi.core.build_app(disable_auth=args.disable_auth)
    if args.reset_database:
        # --reset-database drops all tables and creates them again.
        Base.metadata.drop_all(app.data.driver.engine)
        Base.metadata.create_all(app.data.driver.engine)
    elif args.set_admin:
        # --set-admin sets a password (asked interactively) for the admin user,
        # if the admin user doesn't exist it is created.
        session = app.data.driver.session if session is None else session
        passwd = getpass.getpass('Password:')
        User.set_admin(passwd, session=session)
    elif args.serve:
        # Starts a standalone server for development purposes.
        app.run(host=args.addr, port=args.port, debug=args.debug)

# Run with settings provided on command line if this is a script, otherwise
# create an app instance for a WSGI server.
if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    main(args)
else:
    app = wenuapi.core.build_app()

