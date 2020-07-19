import aiohttp.web


def test_create_app(test_app):
    assert isinstance(test_app, aiohttp.web.Application)


async def test_upload_file(app_client):
    res = await app_client.post('/files', data={'file': open('tests/conftest.py', 'rb')})
    assert res.status == 500
