import random

import pytest

import file_server


@pytest.fixture
def test_app():
    return file_server.create_app()


@pytest.fixture
def app_client(test_app, loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(test_app))


@pytest.fixture
async def uploaded_file(app_client):
    contents = bytes([random.getrandbits(8) for _ in range(0, 100)])    # 100 random bytes
    res = await app_client.post('/files/', data={'file': contents})
    data = await res.json()
    return {'hash': data['hash'], 'contents': contents}
