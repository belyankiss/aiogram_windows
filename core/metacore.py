from typing import Optional, Union, List, Tuple, Self

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    InlineKeyboardButton,
    KeyboardButton
    )
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from pydantic import BaseModel, Field


TYPE_KEYBOARDS = (InlineKeyboardButton, KeyboardButton)
TYPE_ONCE_KEYBOARDS = (ReplyKeyboardRemove, ForceReply)
BUILDERS = {
    InlineKeyboardButton: InlineKeyboardBuilder,
    KeyboardButton: ReplyKeyboardBuilder
}

class DefaultKeyboardBuilder(BaseModel):
    buttons: Optional[Union[List[InlineKeyboardButton], List[KeyboardButton]]] = Field(default_factory=list)
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
    sizes: Tuple[int, ...] = 1,
    repeat: bool = False

    def model_post_init(self, __context, **kwargs) -> Self:
        for key, value in self.__class__.model_fields.items():
            if isinstance(value.default, TYPE_KEYBOARDS):
                new_button = self._format_buttons(value.default, **kwargs)
                self.buttons.append(new_button)
            elif isinstance(value.default, TYPE_ONCE_KEYBOARDS):
                self.reply_markup = value.default
                return self
        return self._build_keyboard(*self.buttons, **kwargs)

    @staticmethod
    def _format_buttons(obj: Union[InlineKeyboardButton, KeyboardButton], **kwargs) -> Union[InlineKeyboardButton, KeyboardButton]:
        try:
            if isinstance(obj, KeyboardButton):
                obj = KeyboardButton(text=obj.text.format_map(kwargs))
            else:
                obj = InlineKeyboardButton(
                    text=obj.text.format_map(kwargs),
                    callback_data=obj.callback_data.format_map(kwargs)
                )
            return obj
        except KeyError:
            return obj

    def _build_keyboard(self, *buttons, **kwargs):
        builder = None
        if buttons:
            builder = BUILDERS.get(type(buttons[0]), None)
        if builder:
            instance_builder = builder()
            instance_builder.add(*buttons)
            self.reply_markup = instance_builder.adjust(*self.sizes, repeat=self.repeat).as_markup(**kwargs)
        return self

    def add_buttons(
            self,
            *buttons: Union[InlineKeyboardButton, KeyboardButton],
            replace: bool = False,
            **kwargs
    ):
        self.reply_markup = None
        if replace and buttons:
            return self._build_keyboard(*buttons, **kwargs)
        self.buttons.clear()
        self.buttons.extend(buttons)
        return self.model_post_init(None, **kwargs)









