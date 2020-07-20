import hashlib
import uuid
import pathlib

import aiofiles
import aiofiles.os
import aiohttp.multipart


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent / 'store'
TMP_DIR = BASE_DIR / 'tmp'

# Make both dirs
TMP_DIR.mkdir(parents=True, exist_ok=True)


class EmptyFileError(ValueError):
    """
    Raised when a file shouldn't be empty, yet it is
    """
    pass


async def save_incoming_file(stream: aiohttp.multipart.MultipartReader):
    """
    Saves the file coming in the stream

    :param stream: the multipart request stream to read from
    :return: str: hex digest of sha256 hash of the received file

    :raises EmptyFileError: the stream contained an empty (0 byte) file
    """

    # Create a path to temporary file with a unique name
    tmp_file_path = TMP_DIR / ('uuid' + str(uuid.uuid4()))

    async with aiofiles.open(tmp_file_path, 'wb') as tmp_file:
        file_hash = hashlib.sha256()
        bytes_written = 0
        while True:
            # Get the next part of multipart request body
            req_part = await stream.next()
            if req_part is None:
                # Reached EOF
                break
            # Read that part's bytes, write them to the temp file and update the hash
            file_part = await req_part.read()
            bytes_written += await tmp_file.write(file_part)
            file_hash.update(file_part)

    if bytes_written == 0:
        await aiofiles.os.remove(tmp_file_path)
        raise EmptyFileError

    new_file_dir = BASE_DIR / file_hash.hexdigest()[:2]
    # Make a dir from the first two chars of the hash, skip if it already exists
    try:
        await aiofiles.os.mkdir(new_file_dir)
    except FileExistsError:
        pass

    # On Windows this will raise FileExistsError if a file with the same hash exists
    # Unix-like systems will silently replace existing files (which is arguably the desired behavior)
    await aiofiles.os.rename(tmp_file_path, new_file_dir / file_hash.hexdigest())

    return file_hash.hexdigest()


async def get_file_gen(file_hash):
    """
    Return a coroutine that creates an async generator that yields chunks from a file with a given hash

    :param file_hash: hash of the file to find
    :return: None if file wasn't found, Coroutine -> AsyncGenerator if file was found
    """
    file_path = BASE_DIR / file_hash[:2] / file_hash
    if not file_path.exists():
        return None

    async def file_gen(chunk_size=65536):
        """
        Async generator of chunks from file at file_path

        :param chunk_size: max size of a chunk to return
        :return: AsyncGenerator that yields chunks of data from the file
        """
        async with aiofiles.open(file_path, 'rb') as file:
            while True:
                data = await file.read(chunk_size)
                if not data:
                    break
                yield data
    return file_gen


async def delete_file(file_hash):
    pass
