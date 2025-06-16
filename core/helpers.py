from pathlib import Path
from typing import Union

import aiofiles

from aiogram.types import BufferedInputFile

async def format_to_bytes_file(path: str) -> Union[BufferedInputFile, str, None]:
    if path is None:
        return None
    try:
        async with aiofiles.open(file=path, mode="rb") as file:
            filename = Path(path).name
            return BufferedInputFile(file=await file.read(), filename=filename)
    except FileNotFoundError:
        return path