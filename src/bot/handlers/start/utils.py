# Aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_language_keyboard():
    rus = InlineKeyboardButton(text="Русский", callback_data="ru")
    eng = InlineKeyboardButton(text="English", callback_data="en")
    markup = InlineKeyboardMarkup(inline_keyboard=[[rus],[eng]])
    return markup

def utc_keyboard():
    """Keyboard for select timezone."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="- 1", callback_data="UTC_MINUS"),
            InlineKeyboardButton(text="+ 1", callback_data="UTC_PLUS")
        ],
        [InlineKeyboardButton(text="Подтвердить", callback_data="OK")]
    ])

def confirm_keyboard(language: str):
    eng = ("RIGHT", "WRONG")
    rus = ("ПРАВИЛЬНО", "НЕПРАВИЛЬНО")
    right_button = InlineKeyboardButton(
        text=rus[0] if language == "ru" else eng[0],
        callback_data=eng[0]
    )
    wrong_button = InlineKeyboardButton(
        text=rus[1] if language == "ru" else eng[1],
        callback_data=eng[1]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[right_button, wrong_button]]
    )

texts = {
    "choose_language":"Пожалуйста выберите язык\nPlease choose the language",
    "choose_timezone":{
        "ru":"Пожалуйста выберите ваш часовой пояс",
        "en":"Please choose your timezone"
    },
    "selected_timezone":{
        "ru":"Выбранный часовой пояс: UTC",
        "en":"Selected timezone: UTC"
    },
    "change_timezone_from_positive":{
        "ru":"Выбранный часовой пояс: UTC+{tz}",
        "en":"Selected timezone: UTC+{tz}"
    },
    "change_timezone_from_negative":{
        "ru":"Выбранный часовой пояс: UTC{tz}",
        "en":"Selected timezone: UTC{tz}"
    },
    "request_for_confirm":{
        "ru":"""Вы выбрали русский язык и ваш часовой пояс "UTC{s}{tz}", верно?""",
        "en":"""You have selected English and your time zone is "UTC{s}{tz}", right?"""
    },
    "wrong":{
        "ru":"Очень жаль, пожалуйста используйте команду /start чтобы начать заново",
        "en":"I'm really sorry about that, please use the command /start for try again"
    },
    "right":{
        "ru":"Спасибо за предоставленную информацию, теперь вы можете использовать другие команды из меню!",
        "en":"thanks for the information provided, now you can use other commands from menu!"
    },
    "error":{
        "ru":"Произошла непредвиденная ошибка, пожалуйста попробуйте заново!",
        "en":"An unexpected error has occurred, please, try again!"
    }
}

