import argparse

import aiohttp.web

routes = aiohttp.web.RouteTableDef()


@routes.post('/files')
async def file_upload(request):
    raise NotImplementedError


@routes.get('/files/{hash}')
async def file_download(request):
    raise NotImplementedError


@routes.delete('/files/{hash}')
async def file_delete(request):
    raise NotImplementedError


def create_app():
    app = aiohttp.web.Application()
    app.add_routes(routes)
    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-P', '--port', default=8080, type=int)
    args = parser.parse_args()

    aiohttp.web.run_app(create_app(), host=args.host, port=args.port)


if __name__ == '__main__':
    main()

