import asyncio
from datetime import date
import qrcode
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile

from keyboards import kb_admin, years_adm, month_adm, res, pay_change, lang_btn
from state import admin
from loader import dp
from filters import IsAdm
from utils.db_api import quick_commands as commands


@dp.message_handler(text='Бекор қилиш ❌',
                    state=[admin.year_admin, admin.months_admin, admin.year_admin_change, admin.months_admin_change,
                           admin.day_change, admin.result_adm, admin.order_change, admin.pay, admin.order_number])
async def quit(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(text='Бекор қилиш ❌')
async def quits(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(IsAdm(), text='Пансионат бандлигини кўриш.')
async def admins(message: Message):
    txt = 'Йилни танланг:'
    await message.answer(txt, reply_markup=years_adm)
    await admin.year_admin.set()


@dp.message_handler(IsAdm(), state=admin.year_admin)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(year_admin=message.text)
    txt = 'Ойни танланг:'
    await message.answer(txt, reply_markup=month_adm)
    await admin.months_admin.set()


@dp.message_handler(IsAdm(), state=admin.months_admin)
async def year_adm(message: Message, state: FSMContext):
    if message.text == 'Январ':
        await state.update_data(mont_admin=1)
        await state.update_data(months_txt_adm='Январ')
    elif message.text == 'Феврал':
        await state.update_data(mont_admin=2)
        await state.update_data(months_txt_adm='Феврал')
    elif message.text == 'Март':
        await state.update_data(mont_admin=3)
        await state.update_data(months_txt_adm='Март')
    elif message.text == 'Апрел':
        await state.update_data(mont_admin=4)
        await state.update_data(months_txt_adm='Апрел')
    elif message.text == 'Май':
        await state.update_data(mont_admin=5)
        await state.update_data(months_txt_adm='Май')
    elif message.text == 'Июн':
        await state.update_data(mont_admin=6)
        await state.update_data(months_txt_adm='Июн')
    elif message.text == 'Июл':
        await state.update_data(mont_admin=7)
        await state.update_data(months_txt_adm='Июл')
    elif message.text == 'Август':
        await state.update_data(mont_admin=8)
        await state.update_data(months_txt_adm='Август')
    elif message.text == 'Сентябр':
        await state.update_data(mont_admin=9)
        await state.update_data(months_txt_adm='Сентябр')
    elif message.text == 'Октябр':
        await state.update_data(mont_admin=10)
        await state.update_data(months_txt_adm='Октябр')
    elif message.text == 'Ноябр':
        await state.update_data(mont_admin=11)
        await state.update_data(months_txt_adm='Ноябр')
    elif message.text == 'Декабр':
        await state.update_data(mont_admin=12)
        await state.update_data(months_txt_adm='Декабр')

    data = await state.get_data()
    try:
    # if True:
        year = int(data.get('year_admin'))
        mont_admin = int(data.get('mont_admin'))
        order = await commands.select_order_by_date_admin(year, mont_admin)
        if not order:
            await message.answer('Бу ойда буюртма қилинмаган', reply_markup=kb_admin)
        else:
            for i in order:
                orders = await commands.select_ord(i.order_id)
                txtx = f'| Буюртма № {i.order_id} | Куни: {orders.date_start} 12:00 дан {orders.date_end} 11:00 гача | ФИО: {orders.fio} | Хона рақами: {orders.room_number} | Хона тури: {orders.room_class} | Тел: <code>{orders.tel}</code> | Тўлов тури: {orders.paytype} | Тўлов суммаси: {orders.summa}'

                await message.answer(txtx)
            await message.answer('Буюртмалар тугади', reply_markup=kb_admin)
    except Exception:
        await state.finish()
        await message.answer('Хатолик', reply_markup=kb_admin)

    await state.finish()


@dp.message_handler(IsAdm(), text='Буюртмани рақами бўйича текшириш.')
async def admins(message: Message):
    txt = 'Буюртмани рақамини ёзинг'
    await message.answer(txt)
    await admin.order_number.set()


@dp.message_handler(IsAdm(), state=admin.order_number)
async def order_adm(message: Message, state: FSMContext):
    await state.update_data(order_id_adm=message.text)
    data = await state.get_data()
    try:
        order_id_adm = int(data.get('order_id_adm'))
        orders = await commands.select_ord(order_id_adm)
        pays = orders.summa
        txt_or = ''
        if orders.pay_status:
            pay = " Тўлов қилинган ✅ "
        else:
            pay = " Тўлов қилинмаган ❌"
        txt_or += f'| Буюртма № <code>{order_id_adm}</code> | Куни: {orders.date_start} 12:00 дан {orders.date_end} 11:00 гача | ФИО: {orders.fio} | Хона рақами: {orders.room_number} | Хона тури: {orders.room_class} | Тел: <code>{orders.tel}</code> | Тўлов холати {pay}| Тўлов тури: {orders.paytype} | Тўлов суммаси: {pays}'

        await message.answer(txt_or, reply_markup=kb_admin)

    except Exception:
        await message.answer('Хатолик', reply_markup=kb_admin)
        await state.finish()
    await state.finish()


@dp.message_handler(IsAdm(), text='Буюртмани рақами бўйича ўзгартириш.')
async def admins(message: Message):
    txt = 'Буюртмани рақамини ёзинг'
    await message.answer(txt)
    await admin.order_change.set()


@dp.message_handler(IsAdm(), state=admin.order_change)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(order_change_id=message.text)
    data = await state.get_data()
    global order_change_id
    order_change_id = data.get('order_change_id')
    txt = 'Ўзгартириш турини танланг:'
    await message.answer(txt, reply_markup=res)
    await state.finish()


@dp.message_handler(IsAdm(), text='Тўлов холатини ўзгартириш.')
async def year_adm(message: Message, state: FSMContext):
    txt = 'Ўзгартиришни танланг:'
    await message.answer(txt, reply_markup=pay_change)


@dp.message_handler(IsAdm(), text='Тўлов қилиш.')
async def year_adm(message: Message, state: FSMContext):
    txt = 'Суммани киритинг:'
    order = await commands.select_ord(int(order_change_id))
    summa = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f'{order.summa}')]
        ],
        resize_keyboard=True,
    )
    await message.answer(txt, reply_markup=summa)
    await admin.pay.set()


@dp.message_handler(IsAdm(), state=admin.pay)
async def year_adm(message: Message, state: FSMContext):
    try:
    # if True:
        pay_int = int(message.text)
        order_id = int(order_change_id)
        orders = await commands.select_ord(order_id)
        pays = pay_int
        await commands.change_pay(order_id, pays)
        await commands.paid(order_id)
        txt_or = ''
        pay = "Тўлов қилинди ✅ "
        txt_or += f'| Буюртма №: <code>{order_id}</code> | Куни: {orders.date_start} 12:00 дан {orders.date_end} 11:00 гача | ФИО: {orders.fio} | Хона рақами: {orders.room_number} | Хона тури: {orders.room_class} | Тел: <code>{orders.tel}</code> | Тўлов холати: {pay}| Тўлов тури: {orders.paytype} | Тўлов суммаси: {pays}'
        txt_cr_code = f'| Буюртма № {order_id}| ФИО: {orders.fio} | Хона рақами {orders.room_number} | Хона тури {orders.room_class} | Куни: {orders.date_start} 12:00 дан {orders.date_end} 11:00 гача | Тел: {orders.tel} | Тўлов холати {pay}| Тўлов тури: {orders.paytype} | Тўлов суммаси: {pays}'
        data = txt_cr_code
        filename = "site.png"
        img = qrcode.make(data)
        img.save(filename)
        # await message.answer_document(document=filename)
        order_id = int(order_change_id)
        orders = await commands.select_ord(order_id)
        if orders.pay_status:
            await asyncio.sleep(2)
            imgs = InputFile(path_or_bytesio=filename)
            await message.answer_document(document=imgs)
            await message.answer(txt_or, reply_markup=kb_admin)
        else:
            txt_canc = 'Хона банд.'
            await message.answer(txt_canc, reply_markup=kb_admin)
    except Exception:
        await message.answer('Хатолик', reply_markup=kb_admin)
        await state.finish()

    await state.finish()


@dp.message_handler(IsAdm(), text='Янги буюртма қилиш.')
async def langu(message: Message):
    await message.answer("Тилни танланг!", reply_markup=lang_btn)


@dp.message_handler(IsAdm(), text='ok')
async def ok(message: Message):
    await message.answer('ok', reply_markup=kb_admin)
