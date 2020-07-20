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
