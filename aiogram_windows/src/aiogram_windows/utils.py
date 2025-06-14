import logging
from typing import List, Dict, Type, Union

import aiofiles
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, KeyboardButton, BufferedInputFile, InlineQueryResultsButton, Message, \
    CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .errors import TypeButtonError, ContextError

InlineList = List[InlineKeyboardButton]
ReplyList = List[KeyboardButton]

BUILDERS: Dict[Type, Type[Union[InlineKeyboardBuilder, ReplyKeyboardBuilder]]] = {
    InlineKeyboardButton: InlineKeyboardBuilder,
    KeyboardButton: ReplyKeyboardBuilder
}

ALLOWED_TYPES_INLINE = []
ALLOWED_TYPES_REPLY = []

def check_keyboard(keyboard: Union[InlineList, ReplyList] = None):
    button_type = type(keyboard[0])
    if not all([isinstance(button, button_type) for button in keyboard]):
        raise TypeButtonError("Wrong format button!")
    return button_type

def get_builder(keyboard: Union[InlineList, ReplyList] = None):
    return BUILDERS.get(check_keyboard(keyboard))


def build_keyboard(keyboard: Union[InlineList, ReplyList] = None, *sizes: int):
    if not keyboard:
        return None
    builder = get_builder(keyboard)()
    builder.add(*keyboard)
    return builder.adjust(*sizes).as_markup(resize_keyboard=True)

async def reformat_photo(photo: str):
    async with aiofiles.open(photo, "rb") as photo_rb:
        return BufferedInputFile(await photo_rb.read(), "photo")

async def delete_after_func(event: Union[Message, CallbackQuery], state: FSMContext):
    if not state:
        raise ContextError("The attribute state was not passed.")
    data = await state.get_data()
    delete_list = data.get("delete_list", [])
    if delete_list:
        msg: Union[Message, CallbackQuery] = delete_list.pop(0)
        try:
            if isinstance(msg, Message):
                await msg.delete()
            else:
                await msg.message.delete()
        except TelegramBadRequest as err:
            logging.warning(f"{err.message}")
    delete_list.append(event)
    await state.update_data(delete_list=delete_list)