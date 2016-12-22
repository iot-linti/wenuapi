#!/usr/bin/env python
import argparse
import sys
import wenuapi.core
from wenuapi.models.common import Base

def build_parser():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('-s', '--serve', action='store_true', default=True)
    mode.add_argument('--reset-database', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--disable-auth', action='store_true')
    parser.add_argument('--set-admin', action='store_true')
    return parser


def main(args):
    app = wenuapi.core.build_app(disable_auth=args.disable_auth)
    if args.reset_database:
        Base.metadata.drop_all(app.data.driver.engine)
        Base.metadata.create_all(app.data.driver.engine)

    if args.serve:
        app.run(debug=args.debug)

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    main(args)