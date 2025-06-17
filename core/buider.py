# from typing import Union, List, Dict, Type, Optional, Iterable, Self
#
# from aiogram.types import (InlineKeyboardButton,
#                            KeyboardButton,
#                            ReplyKeyboardRemove,
#                            ForceReply,
#                            InlineKeyboardMarkup,
#                            ReplyKeyboardMarkup)
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
#
# from core.methods import CallbackQueryMethods
#
# BUTTON_TYPES = (
#     InlineKeyboardButton,
#     KeyboardButton,
#     ReplyKeyboardRemove,
#     ForceReply
# )
#
#
# class WindowBuilder(
#     CallbackQueryMethods
# ):
#     text: str
#     photo: str
#     file: str
#     sizes: Iterable[int] = (1,)
#     repeat: bool = False
#     __builder__: Dict[Type, Union[Type[InlineKeyboardBuilder], Type[ReplyKeyboardBuilder]]] = {
#         InlineKeyboardButton: InlineKeyboardBuilder,
#         KeyboardButton: ReplyKeyboardBuilder
#     }
#     reply_markup: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
#
#     def __init__(self):
#         self.buttons: Union[List[InlineKeyboardButton], List[KeyboardButton]] = []
#         self.sizes: Iterable[int] = (1, )
#
#     def __init_subclass__(cls, **kwargs):
#         buttons = cls._get_buttons()
#         cls.reply_markup = cls.__build_keyboard(buttons)
#         super().__init_subclass__(**kwargs)
#
#     @classmethod
#     def __build_keyboard(
#             cls,
#             buttons: List[
#                 Union[InlineKeyboardButton,
#                 KeyboardButton,
#                 ReplyKeyboardRemove,
#                 ForceReply
#                 ]
#             ]) -> Union[
#         InlineKeyboardMarkup,
#         ReplyKeyboardMarkup,
#         ReplyKeyboardRemove,
#         ForceReply,
#         None
#     ]:
#
#         if buttons:
#             button_type = type(buttons[0])
#             if isinstance(buttons[0], (ReplyKeyboardRemove, ForceReply)):
#                 return buttons[0]
#             builder_cls: Union[
#                 Type[InlineKeyboardBuilder],
#                 Type[ReplyKeyboardBuilder]] = cls.__builder__.get(button_type)
#             if not builder_cls:
#                 return None
#             builder = builder_cls()
#             builder.add(*buttons)
#             return builder.adjust(*cls.sizes, repeat=cls.repeat).as_markup(resize_keyboard=True)
#         return None
#
#     @classmethod
#     def _get_buttons(cls):
#         return [
#             v for v in cls.__dict__.values()
#             if isinstance(v, BUTTON_TYPES)
#         ]
#
#
#     def add_buttons(
#             self,
#             *buttons: Union[InlineKeyboardButton,
#                             KeyboardButton,
#                             ReplyKeyboardRemove,
#                             ForceReply],
#             save_keyboard: bool = True) -> Self:
#
#         _buttons = []
#         if save_keyboard:
#             _buttons = self._get_buttons()
#             _buttons.extend(buttons)
#         self.buttons.extend(_buttons)
#         self.reply_markup = self.__build_keyboard(self.buttons)
#         return self
#
#
#
#
#
#
#
#
