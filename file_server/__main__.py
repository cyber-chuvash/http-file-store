import argparse

import aiohttp.web

from file_server import create_app


parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', default='127.0.0.1')
parser.add_argument('-P', '--port', default=8080, type=int)
args = parser.parse_args()

aiohttp.web.run_app(create_app(), host=args.host, port=args.port)
