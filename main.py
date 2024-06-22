# Aiogram
import asyncio

# Local
from src.settings.base import bot, dp, logger
from src.settings.config import MENU, DESCRIPTION
from src.bot.routers import ROUTERS


async def main():
    """
    This function starts the bot in polling mode. 
    It initializes the scheduler, sets the bot's commands and description,
    includes routers, starts the polling, and logs the start of the bot.
    """
    await bot.set_my_commands(commands=MENU)
    await bot.set_my_description(description=DESCRIPTION)
    dp.include_routers(*ROUTERS)
    logger.info(msg="START BOT")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


