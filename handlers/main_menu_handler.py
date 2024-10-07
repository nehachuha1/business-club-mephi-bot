from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from lexicon.lexicon import LEXICON_RU

main_menu_router = Router()


@main_menu_router.message(Command(commands='menu'), StateFilter(default_state))
async def process_main_menu(message: Message, is_registered: bool):
    if is_registered:
        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['main_menu_text']
        )
    else:
        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['need_register']
        )
