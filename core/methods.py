from typing import Any

from aiogram.types import (ReplyKeyboardRemove,
                           ForceReply,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           Message,
                           CallbackQuery,
                           MessageEntity,
                           ReplyParameters,
                           LinkPreviewOptions,
                           InputFile)

from aiogram.client.default import Default

from core.cache import use_cache
from core.helpers import format_to_bytes_file


class MessageMethods:
    @classmethod
    async def answer(
            cls,
            event: Message,
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
        return await event.answer(
            text=text if text is not None else cls.text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup else cls.reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )

    @classmethod
    async def answer_photo(
            cls,
            event: Message,
            photo: str | InputFile = None,
            caption: str | None = None,
            parse_mode: str | Default | None = Default("parse_mode"),
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool | Default | None = Default(
                "show_caption_above_media"
            ),
            has_spoiler: bool | None = None,
            disable_notification: bool | None = None,
            protect_content: bool | Default | None = Default("protect_content"),
            allow_paid_broadcast: bool | None = None,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
            allow_sending_without_reply: bool | None = None,
            reply_to_message_id: int | None = None,
            **kwargs: Any
    ) -> Message:
        file_id = None
        formatted_photo = None
        path_photo = photo if photo is not None else cls.photo
        if not path_photo:
            raise AttributeError("Photo can't be empty!")
        cached_file_id = use_cache(path_photo)
        if not cached_file_id:
            formatted_photo = await format_to_bytes_file(path_photo)
        else:
            file_id = cached_file_id

        try:
            text = getattr(cls, "text")
        except AttributeError:
            text = None
        message = await event.answer_photo(
            photo=file_id if file_id else formatted_photo,
            caption=caption if caption is not None else text,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup else cls.reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )
        if file_id is None:
            use_cache(path_photo, message.photo[0].file_id)
        return message

class CallbackQueryMethods:
    @classmethod
    async def answer_callback(
            cls,
            event: CallbackQuery,
            text: str | None = None,
            show_alert: bool | None = None,
            url: str | None = None,
            cache_time: int | None = None,
            **kwargs: Any
    ) -> bool:
        return await event.answer(
            text=text if text else cls.text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
            **kwargs
        )
