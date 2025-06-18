from typing import Any, Optional, Union

from aiogram.types import (Message,
                           CallbackQuery,
                           MessageEntity,
                           LinkPreviewOptions,
                           ReplyParameters,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           ForceReply,
                           InlineKeyboardButton
                           )

from aiogram.client.default import Default

from core.metacore import DefaultKeyboardBuilder

class TextForms(DefaultKeyboardBuilder):
    text: Optional[str] = None
    photo: Optional[str] = None
    file: Optional[str] = None

class MessageMethods(TextForms):

    event: Union[Message, CallbackQuery]
    show_alert: bool = False

    def _get_method(self) -> Message:
        if isinstance(self.event, CallbackQuery):
            return self.event.message
        return self.event

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
                     url: str | None = None,
                     cache_time: int | None = None,
                     **kwargs: Any
                     ) -> Message:
        if self.show_alert:
            return await self.alert(
                text=text if text is not None else self.text.format_map(kwargs),
                show_alert=self.show_alert,
                url=url,
                cache_time=cache_time,
                **kwargs
            )
        event = self._get_method()
        return await event.answer(
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

    async def alert(
            self,
            text: str | None = None,
            show_alert: bool | None = None,
            url: str | None = None,
            cache_time: int | None = None,
            **kwargs: Any
    ) -> Message:
        return await self.event.answer(
            text=text if text is not None else self.text.format_map(kwargs),
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
            **kwargs
        )

    async def edit_text(
            self,
            text: Optional[str] = None,
            inline_message_id: str | None = None,
            parse_mode: str | Default | None = Default("parse_mode"),
            entities: list[MessageEntity] | None = None,
            link_preview_options: LinkPreviewOptions | Default | None = Default(
                "link_preview"
            ),
            reply_markup: InlineKeyboardMarkup | None = None,
            disable_web_page_preview: bool | Default | None = Default(
                "link_preview_is_disabled"
            ),
            **kwargs: Any
    ):
        if isinstance(self.event, Message):
            raise AttributeError(f"event must be Message type")
        event = self._get_method()
        return await event.edit_text(
            text=text if text is not None else self.text.format_map(kwargs),
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup if reply_markup else self.reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            **kwargs
        )






class Hello(MessageMethods):
    text: str = "Hello {username}"
    one: InlineKeyboardButton = InlineKeyboardButton(text="Hello", callback_data="fee")

