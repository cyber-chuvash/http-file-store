import hashlib

import aiohttp.web


def test_create_app(test_app):
    assert isinstance(test_app, aiohttp.web.Application)


async def test_uploaded_file_hash(app_client):
    res = await app_client.post('/files/', data={'file': open('tests/conftest.py', 'rb')})
    assert res.status == 200

    file = open('tests/conftest.py', 'rb')
    f_hash = hashlib.sha256()
    f_hash.update(file.read())

    data = await res.json()
    assert data.get('hash') == f_hash.hexdigest()


async def test_upload_file_bad_content_type(app_client):
    res = await app_client.post('/files/', json={'this': 'should not work'})
    assert res.status == 400


async def test_upload_empty_file(app_client):
    res = await app_client.post('/files/', data={'file': b''})
    assert res.status == 400


async def test_get_file(app_client, uploaded_file):
    res = await app_client.get(f'/files/{uploaded_file["hash"]}')
    assert res.status == 200

    got_file = await res.read()

    f_hash = hashlib.sha256()
    f_hash.update(got_file)

    assert f_hash.hexdigest() == uploaded_file['hash']


async def test_get_nonexitstent_file(app_client):
    res = await app_client.get('/files/1234567890987654321521bc6955deadbeef31e11aaaaaaaaaaaaaaaaaaaaa3f')
    assert res.status == 404
