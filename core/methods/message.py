from typing import Any

from aiogram.types import (Message,
                           MessageEntity,
                           LinkPreviewOptions,
                           ReplyParameters,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           InlineKeyboardButton,
KeyboardButton,
                           ForceReply)

from aiogram.client.default import Default

from core.metacore import DefaultKeyboardBuilder




class MessageMethods(DefaultKeyboardBuilder):

    event: Message

    async def answer(self,
                     text: str = None,
                     parse_mode: str | Default | None = Default("parse_mode"),
                     entities: list[MessageEntity] | None = None,
                     link_preview_options: LinkPreviewOptions | Default | None = Default(
                         "link_preview"
                     ),
                     disable_notification: bool | None = None,
                     protect_content: bool | Default | None = Default("protect_content"),
                     allow_paid_broadcast: bool | None = None,
                     message_effect_id: str | None = None,
                     reply_parameters: ReplyParameters | None = None,
                     reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
                     allow_sending_without_reply: bool | None = None,
                     disable_web_page_preview: bool | Default | None = Default(
                         "link_preview_is_disabled"
                     ),
                     reply_to_message_id: int | None = None,
                     **kwargs: Any
                     ) -> Message:
        return await self.event.answer(
            text=text if text is not None else self.text.format_map(kwargs),
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup else self.reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )



class Hello(MessageMethods):
    text: str = "Hello {username}"
    one: KeyboardButton = InlineKeyboardButton(text="hello {username}", callback_data="call:{but}")

