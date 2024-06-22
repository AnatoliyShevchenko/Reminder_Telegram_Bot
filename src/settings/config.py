# Aiogram
from aiogram.types.bot_command import BotCommand


start = BotCommand(
    command="start",
    description="Первый запуск"
)
create = BotCommand(
    command="create",
    description="создать событие"
)
change = BotCommand(
    command="change",
    description="изменить/удалить событие"
)

MENU = [start, create, change]
DESCRIPTION = """Бот напоминалка (тестовая версия), 
\nпри первом запуске необходимо использовать команду /start
\nСписок команд и их описание можете увидеть в меню.
\n\nReminder Bot (test version)
\n for first launch you need to use a command /start
\n Topic of commands you can see in menu."""

