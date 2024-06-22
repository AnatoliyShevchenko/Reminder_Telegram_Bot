# Aiogram
from aiogram import Router
from aiogram.filters import CommandStart, Command

# Local
from src.bot.mixins import MessageMixin
from src.bot.aiorequests import get_user
from .start.handlers import BeginScenary


main_router = Router(name="Main Router")


@main_router.message(CommandStart())
class StartBot(MessageMixin):
    async def handle(self):
        self.progress_func()
        is_true, body = await get_user(telegram_id=self.chat_id)
        if is_true:
            pass
        else:
            help_func = BeginScenary(event=self.event)
            await help_func.handle()

