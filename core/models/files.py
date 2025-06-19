from pathlib import Path
from typing import Optional, Union

from aiogram.types import BufferedInputFile
from pydantic import BaseModel
import aiofiles

class FileForm(BaseModel):
    file: Optional[str] = None
    photo: Optional[str] = None
    video: Optional[str] = None

    @staticmethod
    async def format_file(path_file: str) -> Union[BufferedInputFile, str, None]:
        if path_file is None:
            return None
        try:
            async with aiofiles.open(file=path_file, mode="rb") as file:
                filename = Path(path_file).name
                return BufferedInputFile(file=await file.read(), filename=filename)
        except FileNotFoundError:
            return path_file