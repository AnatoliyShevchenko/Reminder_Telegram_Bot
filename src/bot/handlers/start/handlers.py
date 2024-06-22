# Aiogram
from aiogram import Router, F
from aiogram.filters import StateFilter

# Local
from src.bot.mixins import CallbackMixin, MessageMixin
from src.bot.states import StartBotStates
from .utils import utc_keyboard, choose_language_keyboard, texts, confirm_keyboard
from src.bot.aiorequests import create_user


start_router = Router(name="Start Router")


class BeginScenary(MessageMixin):
    async def handle(self):
        self.progress_func()
        await self.fsm.set_state(
            state=StartBotStates.choose_language
        )
        await self.make_response_for_edit(
            text=texts.get("choose_language"), 
            markup=choose_language_keyboard()
        )

@start_router.callback_query(StateFilter(
    StartBotStates.choose_language), F.data.in_(["ru", "en"])
)
class ChooseLanguage(CallbackMixin):
    async def handle(self):
        self.progress_func()
        await self.answer_to_callback()
        tz = 0
        await self.fsm.set_data(data={
            "language":self.event.data,
            "timezone":tz
        })
        await self.fsm.set_state(state=StartBotStates.wait_timezone)
        text = f"""{texts["choose_timezone"][self.event.data]}\n
{texts["selected_timezone"][self.event.data]}"""
        await self.edit_response(
            text=text, markup=utc_keyboard()
        )


@start_router.callback_query(StateFilter(
    StartBotStates.wait_timezone), F.data == "UTC_MINUS"
)
class UtcMinus(CallbackMixin):
    async def return_text(self, tz: int, language: str):
        await self.answer_to_callback()
        if tz > -11 and tz <= 0:
            tz -= 1
            text = texts["change_timezone_from_negative"][language].format(tz=tz)
        elif tz > 1:
            tz -= 1
            text = texts["change_timezone_from_positive"][language].format(tz=tz)
        elif tz == 1:
            tz -= 1
            text = texts["selected_timezone"][language]
        await self.fsm.update_data(data={"timezone":tz})
        return text
        
    async def handle(self):
        self.progress_func()
        data = await self.fsm.get_data()
        tz = data.get("timezone")
        language = data.get("language")
        if tz > -11:
            text = await self.return_text(tz=tz, language=language)
            await self.edit_response(
                text=text, markup=utc_keyboard()
            )


@start_router.callback_query(StateFilter(
    StartBotStates.wait_timezone), F.data == "UTC_PLUS"
)
class UtcPlus(CallbackMixin):
    async def return_text(self, tz: int, language: str):
        await self.answer_to_callback()
        if 0 <= tz < 13:
            tz += 1
            text = texts["change_timezone_from_positive"][language].format(tz=tz)
        elif tz < -1:
            tz += 1
            text = texts["change_timezone_from_negative"][language].format(tz=tz)
        elif tz == -1:
            tz += 1
            text = texts["selected_timezone"][language]
        await self.fsm.update_data(data={"timezone":tz})
        return text

    async def handle(self):
        self.progress_func()
        data = await self.fsm.get_data()
        tz = data.get("timezone")
        language = data.get("language")
        if tz < 13:
            text = await self.return_text(tz=tz, language=language)
            await self.edit_response(
                text=text, markup=utc_keyboard()
            )

        
@start_router.callback_query(StateFilter(
    StartBotStates.wait_timezone), F.data == "OK"
)
class ConfirmTimezone(CallbackMixin):
    async def handle(self):
        self.progress_func()
        await self.answer_to_callback()
        data = await self.fsm.get_data()
        tz = data.get("timezone")
        language = data.get("language")
        s = "+" if tz > 0 else ""
        tz = "" if tz == 0 else tz
        await self.fsm.set_state(
            state=StartBotStates.request_for_confirm
        )
        await self.edit_response(
            text=texts["request_for_confirm"][language].format(s=s, tz=tz),
            markup=confirm_keyboard(language=language)
        )


@start_router.callback_query(StateFilter(
    StartBotStates.request_for_confirm), F.data == "WRONG"
)
class WrongRequest(CallbackMixin):
    async def handle(self):
        self.progress_func()
        await self.answer_to_callback()
        data = await self.fsm.get_data()
        language = data.get("language")
        await self.edit_response(text=texts["wrong"][language])
        await self.fsm.clear()


@start_router.callback_query(StateFilter(
    StartBotStates.request_for_confirm), F.data == "RIGHT"
)
class RightRequest(CallbackMixin):
    async def handle(self):
        self.progress_func()
        await self.answer_to_callback()
        data = await self.fsm.get_data()
        tz = data.get("timezone")
        language = data.get("language")
        created, data = await create_user(
            chat_id=self.chat_id, timezone=tz, language=language
        )
        if created:
            await self.edit_response(text=texts["right"][language])
        else:
            await self.edit_response(text=texts["error"][language])
        await self.fsm.clear()

