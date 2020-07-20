import hashlib

import aiohttp.web


def test_create_app(test_app):
    assert isinstance(test_app, aiohttp.web.Application)


async def test_uploaded_file_hash(app_client):
    file = open('tests/conftest.py', 'rb')
    f_hash = hashlib.sha256()
    f_hash.update(file.read())

    res = await app_client.post('/files', data={'file': file})
    assert res.status == 200

    data = await res.json()
    assert data.get('hash') == f_hash.hexdigest()


async def test_upload_file_bad_content_type(app_client):
    res = await app_client.post('/files', json={'this': 'should not work'})
    assert res.status == 400


async def test_upload_empty_file(app_client):
    res = await app_client.post('/files', data={'file': b''})
    assert res.status == 400
