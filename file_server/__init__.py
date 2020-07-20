import aiohttp.web

from file_server.routes import routes


def create_app():
    app = aiohttp.web.Application()
    app.add_routes(routes)
    return app
