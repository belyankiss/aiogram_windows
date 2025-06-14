import logging
from typing import List, Union, Optional, Literal

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardButton,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           CallbackQuery,
                           Message,
                           )
from pydantic.v1.class_validators import all_kwargs

from .errors import ContextError
from .utils import build_keyboard, reformat_photo, delete_after_func


class WindowBuilder:

    text: str = None
    """text - Message for window in telegram (Required parameter)"""

    photo: Optional[str] = None
    """photo - Pointer to send a photo. String value. Can be a path to a photo file or a unique identifier in Telegram. 
    Optional parameter"""

    _keyboard: List[Union[InlineKeyboardButton, KeyboardButton]] = None
    _reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None

    def __init_subclass__(cls, **kwargs):
        if cls.text is None:
            raise AttributeError("Text can't be empty!")

        cls._sizes = kwargs.get("sizes", (1, ))
        if isinstance(cls._sizes, int):
            cls._sizes = (cls._sizes, )

        cls._keyboard = []
        cls._user_keyboard = None
        for key, value in cls.__dict__.items():
            if isinstance(value, InlineKeyboardButton):
                cls._keyboard.append(value)
            elif isinstance(value, KeyboardButton):
                cls._keyboard.append(value)
        if cls._keyboard:
            cls._reply_markup = build_keyboard(cls._keyboard, *cls._sizes)

    @classmethod
    async def answer(
            cls,
            event: Message,
            delete: bool = False,
            delete_after: bool = False,
            state: Optional[FSMContext] = None
    ) -> Message:
        if delete:
            await event.delete()
        message =  await event.answer(text=cls.text, reply_markup=cls._reply_markup)
        if delete_after:
            await delete_after_func(message, state)
        return message

    @classmethod
    async def answer_photo(cls, event: Message, delete: bool = False) -> Message:
        if delete:
            await event.delete()
        if cls.photo is None:
            raise AttributeError("Photo can't be empty!")
        try:
            photo = await reformat_photo(cls.photo)
        except Exception:
            photo = cls.photo
        return await event.answer_photo(caption=cls.text, reply_markup=cls._reply_markup, photo=photo)

    @classmethod
    async def reply(
            cls, event: Message,
            delete: bool = False,
            delete_after: bool = False,
            state: Optional[FSMContext] = None
    ) -> Message:
        if delete:
            await event.delete()
        message = await event.reply(text=cls.text, reply_markup=cls._reply_markup)
        if delete_after:
            await delete_after_func(event, state)
        return message

    @classmethod
    async def answer_callback_query(
            cls,
            event: CallbackQuery,
            delete: bool = False,
            delete_after: bool = False,
            state: Optional[FSMContext] = None
    ) -> Message:
        if delete:
            await event.message.delete()
        message = await event.message.answer(text=cls.text, reply_markup=cls._reply_markup)
        if delete_after:
            await delete_after_func(event, state)
        return message

    @classmethod
    async def edit_text(cls, event: CallbackQuery) -> Message:
        return await event.message.edit_text(text=cls.text, reply_markup=cls._reply_markup)

    @classmethod
    async def edit_caption(cls, event: CallbackQuery) -> Message:
        return await event.message.edit_caption(caption=cls.text, reply_markup=cls._reply_markup)

    @classmethod
    async def reply_callback_query(
            cls,
            event: CallbackQuery,
            delete: bool = False,
            delete_after: bool = False,
            state: Optional[FSMContext] = None
    ) -> Message:
        if delete:
            await event.message.delete()
        message = await event.message.reply(text=cls.text, reply_markup=cls._reply_markup)
        if delete_after:
            await delete_after_func(event, state)
        return message

    @classmethod
    async def show_alert(cls, event: CallbackQuery, show_alert: bool = True) -> bool:
        return await event.answer(text=cls.text, show_alert=show_alert)

    @classmethod
    async def send(
            cls,
            event: Union[Message, CallbackQuery],
            mode: Literal[
                "answer",
                "edit",
                "reply"
            ] = "answer",
            delete: bool = False,
            delete_after: bool = False,
            state: Optional[FSMContext] = None
    ):
        if isinstance(event, Message):
            match mode:
                case "answer":
                    if cls.photo:
                        return await cls.answer_photo(event, delete)
                    return await cls.answer(event, delete, delete_after, state)
                case "reply":
                    return await cls.reply(event, False, delete_after, state)
                case "edit":
                    return await cls.answer(event, delete, delete_after, state)

        else:
            match mode:
                case "answer":
                    return await cls.answer_callback_query(event, delete, delete_after, state)
                case "reply":
                    return await cls.reply_callback_query(event, False, delete_after, state)
                case "edit":
                    if event.message.caption:
                        return await cls.edit_caption(event)
                    return await cls.edit_text(event)

        return None


    @classmethod
    def add_buttons(cls, *buttons: Union[InlineKeyboardButton, KeyboardButton]):
        for button in buttons:
            if button not in cls._keyboard:
                cls._keyboard.append(button)
        cls._reply_markup = build_keyboard(cls._keyboard, *cls._sizes)






