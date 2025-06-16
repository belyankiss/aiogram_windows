from typing import Any, Optional, Union

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
        _text: str = getattr(cls, "text", None)
        _reply_markup = getattr(cls, "reply_markup", None)
        return await event.answer(
            text=text if text is not None else _text.format_map(kwargs),
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup else _reply_markup,
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
        path_photo = photo if photo is not None else getattr(cls, "photo", None)
        if not path_photo:
            raise AttributeError("Photo can't be empty!")
        cached_file_id = use_cache(path_photo)
        if not cached_file_id:
            formatted_photo = await format_to_bytes_file(path_photo)
        else:
            file_id = cached_file_id
        _text: str = getattr(cls, "text", None)
        _reply_markup = getattr(cls, "reply_markup", None)
        message = await event.answer_photo(
            photo=file_id if file_id else formatted_photo,
            caption=caption if caption is not None else _text.format_map(kwargs),
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup else _reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )
        if file_id is None:
            use_cache(path_photo, message.photo[0].file_id)
        return message

    @classmethod
    async def answer_document(
            cls,
            event: Message,
            document: Union[str, InputFile, None] = None,
            thumbnail: InputFile | None = None,
            caption: str | None = None,
            parse_mode: str | Default | None = Default("parse_mode"),
            caption_entities: list[MessageEntity] | None = None,
            disable_content_type_detection: bool | None = None,
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
        document_id = None
        formatted_document = None
        path_document = document if document else getattr(cls, "file", None)
        if not path_document:
            raise AttributeError("Document can't be empty!")
        cached_document_id = use_cache(path_document)
        if not cached_document_id:
            formatted_document = await format_to_bytes_file(path_document)
        else:
            document_id = cached_document_id
        _caption: str = getattr(cls, "text", None)
        _reply_markup = getattr(cls, "reply_markup", None)
        message = await event.answer_document(
            document=document_id if document_id else formatted_document.format_map(kwargs),
            thumbnail=thumbnail,
            caption=caption if caption is not None else _caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup if reply_markup is not None else _reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )
        if document_id is None:
            use_cache(path_document, document_id)
        return message

    @classmethod
    async def _edit_text(
            cls,
            event: Message,
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
    ) -> Message:
        _text: str = getattr(cls, "text", None)
        _reply_markup = getattr(cls, "reply_markup", None)
        return await event.edit_text(
            text=text if text is not None else _text.format_map(kwargs),
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup if reply_markup is not None else _reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            **kwargs
        )

    @classmethod
    async def _edit_caption(
            cls,
            event: Message,
            inline_message_id: str | None = None,
            caption: str | None = None,
            parse_mode: str | Default | None = Default("parse_mode"),
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool | Default | None = Default(
                "show_caption_above_media"
            ),
            reply_markup: InlineKeyboardMarkup | None = None,
            **kwargs: Any
    ):
        _caption: str = getattr(cls, "text", None)
        _reply_markup = getattr(cls, "reply_markup", None)
        return await event.edit_caption(
            inline_message_id=inline_message_id,
            caption=caption if caption is not None else _caption.format_map(kwargs),
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup if reply_markup is not None else _reply_markup,
            **kwargs
        )

class CallbackQueryMethods(MessageMethods):
    @classmethod
    async def show_alert(
            cls,
            event: CallbackQuery,
            text: str | None = None,
            show_alert: bool | None = None,
            url: str | None = None,
            cache_time: int | None = None,
            **kwargs: Any
    ) -> bool:
        _text = getattr(cls, "text", None)
        return await event.answer(
            text=text if text else _text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
            **kwargs
        )

    @classmethod
    async def answer_callback(
            cls,
            event: CallbackQuery,
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
        return await cls.answer(
            event=event.message,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )

    @classmethod
    async def edit_text(
            cls,
            event: CallbackQuery,
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
    ) -> Message:
        return await cls._edit_text(
            event=event.message,
            text=text,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            **kwargs
        )

    @classmethod
    async def edit_caption(
            cls,
            event: CallbackQuery,
            inline_message_id: str | None = None,
            caption: str | None = None,
            parse_mode: str | Default | None = Default("parse_mode"),
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool | Default | None = Default(
                "show_caption_above_media"
            ),
            reply_markup: InlineKeyboardMarkup | None = None,
            **kwargs: Any
    ):
        return await cls._edit_caption(
            event=event.message,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
            **kwargs
        )

