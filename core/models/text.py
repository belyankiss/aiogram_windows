from typing import Optional

from .keyboard_builder import DefaultKeyboardBuilder
from .files import FileForm


class TextForms(DefaultKeyboardBuilder, FileForm):
    text: Optional[str] = None
