from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot

class RegistrationForm(StatesGroup):
    username = State()
    full_name = State()
    study_group = State()