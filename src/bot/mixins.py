# Aiogram
from aiogram.handlers import (
    MessageHandler, CallbackQueryHandler, BaseHandler
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
import aiogram.types as tp

# Third-Party
from aiogram_calendar import SimpleCalendar
from aiogram_calendar import SimpleCalendarCallback

# Python
from datetime import datetime
from typing import Any, Union

# Local
from src.settings.base import logger, bot, LOCALE, storage
from .redis_utils import RedisUtils


class BaseMixin(BaseHandler, RedisUtils):
    """Base mixin for Messages and CallbackQueries."""

    def __init__(
        self, event: Union[tp.Message,tp.CallbackQuery], **kwargs: Any
    ) -> None:
        if isinstance(event, tp.Message):
            self.chat_id = event.chat.id
        elif isinstance(event, tp.CallbackQuery):
            self.chat_id = event.message.chat.id
        self.storage = storage
        self.key = StorageKey(
            bot_id=bot.id, chat_id=self.chat_id, user_id=self.chat_id
        )
        self.fsm = FSMContext(
            storage=self.storage, key=self.key
        )
        self.event = event

    def progress_func(self):
        """It's for tracing performing handlers."""
        name = self.__class__.__name__
        logger.info("-"*50)
        logger.info(f"{name} In Progress For {self.chat_id}")
        logger.info("-"*50)

    async def remove_messages(self):
        messages: list = await self.get_list_from_redis(
            chat_id=self.chat_id, key="to_remove"
        )
        edit = await self.get_object_from_redis(
            chat_id=self.chat_id, key="to_edit"
        )
        messages.append(edit)
        for i in messages:
            try:
                await bot.delete_message(
                    chat_id=self.chat_id, message_id=int(i)
                )
            except:
                pass

    async def make_response(
        self, text: str, markup: Union[
            tp.ReplyKeyboardRemove, tp.ReplyKeyboardMarkup, 
            tp.InlineKeyboardMarkup, InlineKeyboardBuilder
        ] = tp.ReplyKeyboardRemove()
    ):
        temp = await bot.send_message(
            chat_id=self.chat_id, text=text, reply_markup=markup
        )
        await self.values_to_list_in_redis(
            temp.message_id, chat_id=self.chat_id, key="to_remove"
        )

    async def make_response_for_edit(
        self, text: str, markup: Union[
            tp.ReplyKeyboardRemove, tp.ReplyKeyboardMarkup, 
            tp.InlineKeyboardMarkup, InlineKeyboardBuilder
        ] = None
    ):
        temp = await bot.send_message(
            chat_id=self.chat_id, text=text, reply_markup=markup
        )
        await self.set_object_to_redis(
            obj=temp.message_id, chat_id=self.chat_id, key="to_edit"
        )

    async def edit_response(
        self, text: str, markup: Union[
            tp.ReplyKeyboardRemove, tp.ReplyKeyboardMarkup, 
            tp.InlineKeyboardMarkup, InlineKeyboardBuilder
        ] = None
    ):
        edit = await self.get_object_from_redis(
            chat_id=self.chat_id, key="to_edit"
        )
        await bot.edit_message_text(
            text=text, chat_id=self.chat_id, 
            reply_markup=markup, message_id=edit
        )

    def get_calendar(self):
        return SimpleCalendar(locale=LOCALE)

    async def response_with_calendar(self, text: str):
        calendar = self.get_calendar()
        markup = await calendar.start_calendar()
        await bot.send_message(
            chat_id=self.chat_id, text=text, reply_markup=markup
        )


class MessageMixin(MessageHandler, BaseMixin):
    """Mixin for Message Handlers."""

    def __init__(self, event: tp.Message, **kwargs: Any) -> None:
        super().__init__(event, **kwargs)

    async def mark_event_to_delete(self):
        await self.values_to_list_in_redis(
            self.event.message_id, chat_id=self.chat_id, key="to_remove"
        )


class CallbackMixin(CallbackQueryHandler, BaseMixin):
    """Mixin for Callback Query Handlers."""

    def __init__(self, event: tp.CallbackQuery, **kwargs: Any) -> None:
        super().__init__(event, **kwargs)

    async def answer_to_callback(self):
        try:
            await self.event.answer()
            # await self.event.message.delete_reply_markup()
        except:
            pass

    async def get_date_from_calendar(self):
        """Func for get data from inline-calendar."""
        await self.event.answer()
        calendar = self.get_calendar()
        if "IGNORE" in self.callback_data:
            return None
        elif "CANCEL" in self.callback_data:
            await self.event.message.delete_reply_markup()
            await self.fsm.clear()
            await self.make_response(
                text="Операция отменена пользователем!"
            )
            return None
        elif "TODAY" in self.callback_data:
            date = datetime.now()
            await self.event.message.delete_reply_markup()
            return date
        try:
            data = self.callback_data.split(":")
            simple = SimpleCalendarCallback(
                act=data[1], year=data[2], month=data[3], day=data[4]
            )
            selected, date = await calendar.process_selection(
                query=self.event, data=simple
            )
            if date:
                return date
        except Exception as e:
            logger.error(msg=e, stack_info=True)
            return str(e)

