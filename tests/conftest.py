import pytest

import app


@pytest.fixture
def test_app():
    return app.create_app()


@pytest.fixture
def app_client(test_app, loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(test_app))
