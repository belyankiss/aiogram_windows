from typing import Union, List, Dict, Type, Optional, Iterable

from aiogram.types import (InlineKeyboardButton,
                           KeyboardButton,
                           ReplyKeyboardRemove,
                           ForceReply,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from core.methods import MessageMethods, CallbackQueryMethods

BUTTON_TYPES = (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardRemove,
    ForceReply
)


class WindowBuilder(
    MessageMethods,
    CallbackQueryMethods
):
    text: str
    photo: str
    sizes: Iterable[int] = (1,)
    repeat: bool = False
    __builder__: Dict[Type, Union[Type[InlineKeyboardBuilder], Type[ReplyKeyboardBuilder]]] = {
        InlineKeyboardButton: InlineKeyboardBuilder,
        KeyboardButton: ReplyKeyboardBuilder
    }
    reply_markup: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None

    def __init_subclass__(cls, **kwargs):
        buttons = [
            v for v in cls.__dict__.values()
            if isinstance(v, BUTTON_TYPES)
        ]
        cls.reply_markup = cls.__build_keyboard(buttons)

    @classmethod
    def __build_keyboard(
            cls,
            buttons: Union[
                List[InlineKeyboardButton],
                List[KeyboardButton],
                ReplyKeyboardRemove,
                ForceReply
            ]) -> Union[
        InlineKeyboardMarkup,
        ReplyKeyboardMarkup,
        ReplyKeyboardRemove,
        ForceReply,
        None
    ]:
        if isinstance(buttons, list):
            if len(buttons) > 0:
                button_type = type(buttons[0])
                builder_cls: Union[
                    Type[InlineKeyboardBuilder],
                    Type[ReplyKeyboardBuilder]] = cls.__builder__.get(button_type)
                if not builder_cls:
                    return None
                builder = builder_cls()
                builder.add(*buttons)
                return builder.adjust(*cls.sizes, repeat=cls.repeat).as_markup(resize_keyboard=True)
            return None
        elif isinstance(buttons, (ReplyKeyboardRemove, ForceReply)):
            return buttons
        return None

