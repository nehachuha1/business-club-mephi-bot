from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON_RU

check_data_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON_RU['confirm_data_registration'], callback_data='CONFIRM_REGISTRATION_DATA'),
            InlineKeyboardButton(text=LEXICON_RU['decline_data_registration'], callback_data='DECLINE_REGISTRATION_DATA'),
        ]
    ]
)