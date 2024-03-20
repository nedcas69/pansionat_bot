from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsPrivate, IsAdm
from keyboards import lang_btn, kb_admin  # Импортируем нашу клавиатуру
from loader import dp


@dp.message_handler(Command("start"), IsAdm())  # Создаём message handler который ловит команду /menu
async def menu(message: types.Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Admin!", reply_markup=kb_admin)
    await state.finish()



@dp.message_handler(Command("start"), IsPrivate())  # Создаём message handler который ловит команду /menu
async def menu(message: types.Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Выберите язык!", reply_markup=lang_btn)
    doc_uz = 'BQACAgIAAxkBAAIWQGT_8XH1dtxyQDE_ufaeJyLT1910AAJnMwAC5XkBSPDco_JmfQIlMAQ'
    await message.answer_document(doc_uz)
    await state.finish()
