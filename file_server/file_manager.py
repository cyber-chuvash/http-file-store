import hashlib
import uuid
import pathlib

import aiofiles
import aiofiles.os
import aiohttp.multipart


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent / 'store'
TMP_DIR = BASE_DIR / 'tmp/'
TMP_DIR.mkdir(parents=True, exist_ok=True)


async def save_incoming_file(stream: aiohttp.multipart.MultipartReader):
    tmp_file_name = TMP_DIR / ('uuid' + str(uuid.uuid4()))
    tmp_file = await aiofiles.open(tmp_file_name, 'wb')
    f_hash = hashlib.sha256()

    while True:
        req_part = await stream.next()
        if req_part is None:
            break

        file_part = await req_part.read()
        await tmp_file.write(file_part)
        f_hash.update(file_part)

    await tmp_file.close()

    f_hash_hex = f_hash.hexdigest()
    new_file_dir = BASE_DIR / f_hash_hex[:2]

    try:
        await aiofiles.os.mkdir(new_file_dir)
    except FileExistsError:
        pass

    await aiofiles.os.rename(tmp_file_name, new_file_dir / f_hash_hex)

    return f_hash_hex


async def get_file(hash_sum):
    pass


async def delete_file(hash_sum):
    pass
