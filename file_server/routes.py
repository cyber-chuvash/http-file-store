import aiohttp.web
from aiohttp.web import json_response, StreamResponse, Response

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


@routes.get('/files/{hash:[A-Fa-f0-9]{64}}')
async def file_download(request):
    file_hash = request.match_info['hash'].lower()

    try:
        # Get an async generator coroutine with file data
        file_data_generator = await file_manager.get_file_gen(file_hash)
    except FileNotFoundError:
        return json_response({'error': "File not found"}, status=404)

    headers = {
        "Content-disposition": f"attachment; filename={file_hash[:16]}"
    }
    res = StreamResponse(status=200, headers=headers)
    res.enable_chunked_encoding()
    await res.prepare(request)

    # Get file chunks from the generator and send them in a response
    async for chunk in file_data_generator():
        await res.write(chunk)

    # Write the last, empty chunk
    await res.write_eof()
    return res


@routes.delete('/files/{hash:[A-Fa-f0-9]{64}}')
async def file_delete(request):
    file_hash = request.match_info['hash'].lower()
    try:
        await file_manager.delete_file(file_hash)
    except FileNotFoundError:
        return json_response({'error': "File not found"}, status=404)

    return Response(status=200, reason='OK')
