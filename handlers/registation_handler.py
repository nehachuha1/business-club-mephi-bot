from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
import regex
import asyncio

from lexicon.lexicon import LEXICON_RU
from filters.states import RegistrationForm
from keyboards.registration_keyboard import check_data_kb
from database.postgres import Database

registration_router = Router()

@registration_router.message(Command(commands='start'), StateFilter(default_state))
async def process_start_cmd(message: Message, is_registered: bool, bot: Bot):
    if is_registered:
        out = await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['welcome_registered']
        )
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id, message_id=out.message_id)

        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['main_menu_text']
        )
    elif not is_registered:
        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['welcome_not_registered']
        )

@registration_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_without_state(message: Message, state: FSMContext):
    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['cancel_registrations_without_state']
    )
    await state.clear()

@registration_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_with_state(message: Message, state: FSMContext):
    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['cancel_registrations_with_state']
    )
    await state.clear()

@registration_router.message(Command(commands='register'), StateFilter(default_state))
async def process_register_cmd_1(message: Message, state: FSMContext):
    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['registration_step_1']
    )
    await state.set_state(RegistrationForm.username)
    await state.update_data(username=str(message.from_user.id))
    await state.set_state(RegistrationForm.full_name)

@registration_router.message(Command(commands='register'), ~StateFilter(default_state))
async def process_register_cmd_2(message: Message, state: FSMContext):
    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['already_filling']
    )

@registration_router.message(StateFilter(RegistrationForm.full_name), F.text)
async def process_register_cmd_3(message: Message, state: FSMContext):
    await state.update_data(name_surname=message.text)
    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['registration_step_2']
    )
    await state.set_state(RegistrationForm.study_group)

@registration_router.message(StateFilter(RegistrationForm.study_group))
async def process_register_cmd_final(message: Message, state: FSMContext):
    match = regex.fullmatch(r'[АБМС]{1}[1-9]{2}-[0-9]{3}', message.text)
    if match:
        await state.update_data(study_group=message.text)
        result = await state.get_data()
        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['registration_step_3'].format(
                telegram_username=result['username'],
                name_surname=result['name_surname'],
                study_group=result['study_group']
            ),
            reply_markup=check_data_kb
        )
    else:
        await message.answer(
            parse_mode='HTML',
            text=LEXICON_RU['invalid_study_group'],
        )

@registration_router.callback_query(F.data=='CONFIRM_REGISTRATION_DATA', StateFilter(RegistrationForm.study_group))
async def process_register_cmd_confirm_reg(callback: CallbackQuery, state: FSMContext, db: Database, bot: Bot):
    await callback.answer('')

    result = await state.get_data()
    db.register_new_user(
        telegram_username=result['username'],
        name_surname=result['name_surname'],
        study_group=result['study_group']
    )
    out = await callback.message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['finish_registration']
    )

    await asyncio.sleep(3)
    await bot.delete_message(chat_id=out.chat.id, message_id=out.message_id)

    await callback.message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['main_menu_text']
    )
    await state.clear()


@registration_router.callback_query(F.data=='DECLINE_REGISTRATION_DATA', StateFilter(RegistrationForm.study_group))
async def process_register_cmd_decline_reg(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer('')

    await callback.message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['cancel_registrations_with_state']
    )

@registration_router.message(StateFilter(default_state))
async def process_register_random_text(message: Message):
    await message.answer(
        parse_mode='HTML',
        text='Неизвестная команда. Введите /register для регистрации'
    )