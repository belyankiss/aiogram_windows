from typing import Optional

from core.metacore import DefaultKeyboardBuilder
from core.models.files import FileForm


class TextForms(DefaultKeyboardBuilder, FileForm):
    text: Optional[str] = None
