import aiohttp.web
from aiohttp.web import json_response

from file_server import file_manager

routes = aiohttp.web.RouteTableDef()


@routes.post('/files/')
async def file_upload(request):
    if not request.can_read_body:
        return json_response({'error': "Can't read body"}, status=400)
    if request.content_type.split('/')[0] != 'multipart':
        return json_response({'error': "Only multipart content is supported"}, status=400)

    multipart_reader = await request.multipart()
    try:
        f_hash = await file_manager.save_incoming_file(multipart_reader)
    except file_manager.EmptyFileError:
        return json_response({'error': "File is empty"}, status=400)

    return json_response({'hash': f_hash}, status=200)


@routes.get('/files/{hash}')
async def file_download(request):
    raise NotImplementedError


@routes.delete('/files/{hash}')
async def file_delete(request):
    raise NotImplementedError
