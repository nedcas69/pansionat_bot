import json
import re

import requests
from requests.auth import HTTPBasicAuth
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from datetime import date, timedelta

from data.config import C_USER, C_PASS, C_URI
from keyboards import kb_ru, month, year, pays, cancel, conatct_ru, room, order_commerc1, order_commerc2, \
    pays_commerc
from loader import dp
from state import not_work
from keyboards import lang_btn
from filters import IsPrivate
from utils.db_api import quick_commands as commands


@dp.message_handler(IsPrivate(), content_types=ContentType.DOCUMENT)  # Ловит только фотографии
async def send_photo_file_id(message: Message):
    await message.reply(message.document.file_id)  # Возвращает file_id фотографии с наилучшим разрешением



@dp.message_handler(text='Отменить заказ ❌',
                    state=[not_work.fio, not_work.dates, not_work.orders, not_work.year, not_work.months, not_work.dayru,
                           not_work.paytype])
async def quit(message: Message, state: FSMContext):
    try:
        select_user_orders = await commands.select_ord_room(message.from_user.id)
        day_start = date(2000, 1, 1)
        day_end = date(2000, 1, 1)
        await commands.room_number_quit(message.from_user.id,
                                        111, 0, '---', day_start, day_end)
    except:
        pass
    await state.finish()
    await message.answer('Заказ отменен.', reply_markup=lang_btn)


@dp.message_handler(text='Отменить заказ ❌')
async def quits(message: Message, state: FSMContext):
    try:
        select_user_orders = await commands.select_ord_room(message.from_user.id)
        day_start = date(2000, 1, 1)
        day_end = date(2000, 1, 1)
        await commands.room_number_quit(message.from_user.id,
                                        111, 0, '---', day_start, day_end)
    except:
        pass
    await state.finish()
    await message.answer('Заказ отменен', reply_markup=lang_btn)


@dp.message_handler(IsPrivate(), text='Не работает АО "Узметкомбинат"')
async def not_worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Напишите ФИО по паспорту.", reply_markup=cancel)
    await not_work.fio.set()


@dp.message_handler(IsPrivate(), state=not_work.fio)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    fio = message.text
    if len(fio) > 5:
        await message.answer(f"{fio} Отправьте свой номер! ⬇️", reply_markup=conatct_ru)
        await not_work.tel.set()
    else:
        await message.answer("Напишите правильно ФИО по паспорту.", reply_markup=cancel)
        await not_work.fio.set()


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=not_work.tel)
async def set_fio(message: Message, state: FSMContext):
    tel = message.contact.phone_number
    data = await state.get_data()
    fio = data.get('fio')
    await state.update_data(tel=tel)
    if len(tel) > 7:
        await message.answer('Выберите хотите заказать путевку или\nЗакончите заказ:', reply_markup=order_commerc2)
        await not_work.orders.set()
    else:
        await message.answer(f"{fio} Отправьте свой номер! ⬇️", reply_markup=conatct_ru)
        await not_work.tel.set()


@dp.message_handler(IsPrivate(), state=not_work.orders)
async def set_fio(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        tel = data.get('tel')
        fri = data.get('fri')
        quantity_orders = data.get('quantity_orders')
        order_type = message.text
        if order_type == 'Заказать путевку' or fri and order_type != 'Закончить заказ путевок':
            await state.update_data(fri=True)
            fio = message.text
            if fio != 'Заказать путевку':
                if fio != 'Закончить заказ путевок':
                    await commands.add_order(message.from_user.id, fio, '0', False, tel, commerc_100=100)
            if fio == 'Закончить заказ путевок':
                await state.update_data(fri=False)
            else:
                text = 'Напишите ФИО по паспорту\n или выберите Закончить заказ ⬇️!'
                await message.answer(text, reply_markup=order_commerc1)
        elif order_type == 'Закончить заказ путевок':
            await state.update_data(fri=False)
            await state.update_data(quantity_orders=True)
            order_days = 'Напишите сколько суток хотите отдохнуть, в числовом формате(0-9).'
            await message.answer(order_days)
        elif quantity_orders:
            try:
                order_day = int(message.text)
                await state.update_data(quantity_orders=False)
                await state.update_data(order_day=order_day)
                await message.answer('Выберите текущий или следующий год ⬇️:', reply_markup=year)
                await not_work.year.set()
            except:
                order_days = 'Напишите сколько суток хотите отдохнуть, в <b>числовом формате(0-9)</b>.'
                await message.answer(order_days)
    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()



@dp.message_handler(IsPrivate(), state=not_work.year)
async def set_fio(message: Message, state: FSMContext):
    try:
        year_now = date.today()
        if message.text == f'{year_now.year}' or message.text == f'{int(year_now.year) + 1}':
            await state.update_data(year=message.text)
        else:
            await message.answer('Выберите текущий или следующий год ⬇️:', reply_markup=year)
            await not_work.year.set()

        data = await state.get_data()
        years = data.get("year")
        if years == f'{year_now.year}':
            i = year_now.month
            jan = ''
            feb = ''
            mar = ''
            apr = ''
            may = ''
            jun = ''
            jul = ''
            avg = ''
            sep = ''
            octob = ''
            nov = ''
            dec = ''
            while i < 13:
                if i == 1:
                    jan = 'Январь'
                    i += 1
                if i == 2:
                    feb = 'Февраль'
                    i += 1
                if i == 3:
                    mar = 'Март'
                    i += 1
                if i == 4:
                    apr = 'Апрель'
                    i += 1
                if i == 5:
                    may = 'Май'
                    i += 1
                if i == 6:
                    jun = 'Июнь'
                    i += 1
                if i == 7:
                    jul = 'Июль'
                    i += 1
                if i == 8:
                    avg = 'Август'
                    i += 1
                if i == 9:
                    sep = 'Сентябрь'
                    i += 1
                if i == 10:
                    octob = 'Октябрь'
                    i += 1
                if i == 11:
                    nov = 'Ноябрь'
                    i += 1
                if i == 12:
                    dec = 'Декабрь'
                    i += 1
                break

        else:
            jan = 'Январь'
            feb = 'Февраль'
            mar = 'Март'
            apr = 'Апрель'
            may = 'Май'
            jun = 'Июнь'
            jul = 'Июль'
            avg = 'Август'
            sep = 'Сентябрь'
            octob = 'Октябрь'
            nov = 'Ноябрь'
            dec = 'Декабрь'

        mont = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f'{jan}'),
                    KeyboardButton(text=f'{feb}')
                ],
                [
                    KeyboardButton(text=f'{mar}'),
                    KeyboardButton(text=f'{apr}')
                ],
                [
                    KeyboardButton(text=f'{may}'),
                    KeyboardButton(text=f'{jun}')
                ],
                [
                    KeyboardButton(text=f'{jul}'),
                    KeyboardButton(text=f'{avg}')
                ],
                [
                    KeyboardButton(text=f'{sep}'),
                    KeyboardButton(text=f'{octob}')
                ],
                [
                    KeyboardButton(text=f'{nov}'),
                    KeyboardButton(text=f'{dec}')
                ],
                [
                    KeyboardButton(text='Отменить заказ ❌')
                ],
            ],
            resize_keyboard=True,
        )

        await message.answer('Выберите месяц ⬇️:', reply_markup=mont)
        await not_work.months.set()
    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work.months)
async def set_fio(message: Message, state: FSMContext):
    try:
        if message.text == 'Январь':
            await state.update_data(months=1)
            await state.update_data(months_txt='Январь')
        elif message.text == 'Февраль':
            await state.update_data(months=2)
            await state.update_data(months_txt='Февраль')
        elif message.text == 'Март':
            await state.update_data(months=3)
            await state.update_data(months_txt='Март')
        elif message.text == 'Апрель':
            await state.update_data(months=4)
            await state.update_data(months_txt='Апрель')
        elif message.text == 'Май':
            await state.update_data(months=5)
            await state.update_data(months_txt='Май')
        elif message.text == 'Июнь':
            await state.update_data(months=6)
            await state.update_data(months_txt='Июнь')
        elif message.text == 'Июль':
            await state.update_data(months=7)
            await state.update_data(months_txt='Июль')
        elif message.text == 'Август':
            await state.update_data(months=8)
            await state.update_data(months_txt='Август')
        elif message.text == 'Сентябрь':
            await state.update_data(months=9)
            await state.update_data(months_txt='Сентябрь')
        elif message.text == 'Октябрь':
            await state.update_data(months=10)
            await state.update_data(months_txt='Октябрь')
        elif message.text == 'Ноябрь':
            await state.update_data(months=11)
            await state.update_data(months_txt='Ноябрь')
        elif message.text == 'Декабрь':
            await state.update_data(months=12)
            await state.update_data(months_txt='Декабрь')
        else:
            await message.answer('Такого месяца не существует.\nВыберите правильный месяц ⬇️:', reply_markup=month)
            await not_work.months.set()

        days = []
        data = await state.get_data()
        years = data.get('year')
        monthsx = data.get('months')

        list3 = []
        try:
            for i in range(1, 32):
                year_now = date(int(years), int(monthsx), i)
                if i in days:
                    continue
                list3.append(i)
                day = year_now.day
        except ValueError:
            pass
        kb_list1 = []
        kb_list2 = []
        kb_list3 = []
        kb_list4 = []
        kb_list5 = []
        kb = [kb_list1, kb_list2, kb_list3, kb_list4, kb_list5]
        if list3 == []:
            await message.answer('Все дни в этом месяце заняты.\nВыберите другой месяц ⬇️:', reply_markup=month)
            await not_work.months.set()
        else:
            for it in list3:
                if it <= 6:
                    kb_list1.append(KeyboardButton(text=f'{it}'))
                elif 6 < it <= 12:
                    kb_list2.append(KeyboardButton(text=f'{it}'))
                elif 12 < it <= 18:
                    kb_list3.append(KeyboardButton(text=f'{it}'))
                elif 18 < it <= 24:
                    kb_list4.append(KeyboardButton(text=f'{it}'))
                elif 24 < it <= 31:
                    kb_list5.append(KeyboardButton(text=f'{it}'))

            cancel_kb = [KeyboardButton(text='Отменить заказ ❌')]
            kb.append(cancel_kb)
            canceld = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await state.update_data(day_x=days)
            await message.answer('Выберите день ⬇️:', reply_markup=canceld)
            await not_work.dayru.set()
    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work.dayru)
async def set_day(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(day_x=text)
    days_x = [i for i in range(1, 32)]
    data = await state.get_data()
    day_x = data.get('day_x')

    try:

        if int(text) in days_x:
            await state.update_data(day=True)
            await state.update_data(daysx=message.text)
            data = await state.get_data()
            years = data.get('year')
            months = data.get('months')
            year_nows = date(int(years), int(months), int(day_x))
            year_now = date.today()
            a = year_nows - year_now
            if a.days < 0:
                await state.finish()
                await message.answer('Нельзя заказать прошедшим днём!\nЗаказ отменен.', reply_markup=lang_btn)

            txt = f'Выберите категорию комнат ⬇️:'
            await message.answer(txt, reply_markup=room)
            await not_work.cat_room.set()

    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()
    await state.update_data(o70=True)


@dp.message_handler(IsPrivate(), state=not_work.cat_room)
async def set_day(message: Message, state: FSMContext):
    try:
        if message.text == 'Стандартный':
            await state.update_data(category_rooms='Standart')
        if message.text == 'Люкс':
            await state.update_data(category_rooms='Lyuks')

        data = await state.get_data()
        days = data.get('day_x')
        years = data.get('year')
        months = data.get('months')
        fio = data.get('fio')
        tel = data.get('tel')
        order_day = data.get('order_day')
        category_rooms = data.get('category_rooms')
        day_start = date(int(years), int(months), int(days))
        day_end = day_start + timedelta(days=order_day)
        order = await commands.select_order_by_date(day_start, day_end)
        room_numbers = await commands.select_all_rooms(category_rooms)
        number_lists = []
        user_id = message.from_user.id
        for num in room_numbers:
            o = 0
            while o < num.number_of_seats:
                number_lists.append(num.number)
                o += 1

        bron_room_numbers = []
        for rom in order:
            bron_room_numbers.append(rom.room_number)

        result = [i for i in number_lists if not i in bron_room_numbers or bron_room_numbers.remove(i)]
        setist = list(set(result))
        my_dict = {i: result.count(i) for i in setist}
        list3 = []
        for i in result:
            if i not in list3:
                list3.append(i)

        end_kb = [KeyboardButton(text='Закончить заказ.')]
        cancel_kb = [KeyboardButton(text='Отменить заказ ❌')]
        kb_list1 = []
        kb_list2 = []
        kb_list3 = []
        kb_list4 = []
        kb_list5 = []
        kb_list6 = []
        kb_list7 = []
        kb_list8 = []
        kb_list9 = []
        kb_list10 = []
        kb_list11 = []
        kb_list12 = []
        kb_list13 = []
        kb_list14 = []
        kb_list15 = []
        kb_list16 = []
        kb_list17 = []
        kb_list18 = []
        kb = [kb_list1, kb_list2, kb_list3, kb_list4, kb_list5, kb_list6, kb_list7, kb_list8, kb_list9, kb_list10,
              kb_list11, kb_list12, kb_list13, kb_list14, kb_list15, kb_list16, kb_list17, kb_list18]
        try:
            for it in range(len(list3)):
                if it <= 3:
                    kb_list1.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 3 < it <= 7:
                    kb_list2.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 7 < it <= 11:
                    kb_list3.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 11 < it <= 15:
                    kb_list4.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 15 < it <= 19:
                    kb_list5.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 19 < it <= 23:
                    kb_list6.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 23 < it <= 27:
                    kb_list7.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 27 < it <= 31:
                    kb_list8.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 31 < it <= 35:
                    kb_list9.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 35 < it <= 39:
                    kb_list10.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 39 < it <= 43:
                    kb_list11.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 43 < it <= 47:
                    kb_list12.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 47 < it <= 51:
                    kb_list13.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 51 < it <= 55:
                    kb_list14.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 55 < it <= 59:
                    kb_list15.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 59 < it <= 63:
                    kb_list16.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 63 < it <= 67:
                    kb_list17.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))
                elif 67 < it <= 71:
                    kb_list18.append(KeyboardButton(text=f'{list3[it]}: {my_dict[list3[it]]}'))

            kb.append(end_kb)
            kb.append(cancel_kb)
            rooms = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            client_orders = ''
            select_user_orders = await commands.select_ord_room(user_id)
            o70 = data.get('o70')
            leto = [6, 7, 8]
            day = 0
            summa = 0
            if o70:
                txt = f'Выберите комнатy для {select_user_orders[0].fio}⬇️:'
                await message.answer(txt, reply_markup=rooms)

            try:
                await state.update_data(o70=False)
                room_num = message.text
                mat = re.search('\d\d\d', room_num)
                roomsx = await commands.select_room_name(mat[0])

                while day < order_day:
                    days_end = day_start + timedelta(days=day)
                    if days_end.month in leto:
                        if roomsx.room_category == 'Lyuks':
                            summa += 564000
                        if roomsx.room_category == 'Standart':
                            summa += 376000
                    else:
                        if roomsx.room_category == 'Lyuks':
                            summa += 414000
                        if roomsx.room_category == 'Standart':
                            summa += 276000

                    day += 1

                await commands.room_number(select_user_orders[0].fio, select_user_orders[0].order_id,
                                           roomsx.id, roomsx.number, roomsx.room_category, day_start, day_end, summa)
                client_orders += select_user_orders[0].fio + ', '

                tx = f'Выберите комнатy для {select_user_orders[1].fio}⬇️:'
                await message.answer(tx, reply_markup=rooms)

            except:
                pass

            if await commands.select_ord_room(user_id) == []:
                summa = await commands.summas(user_id)
                txt = f'{fio} вы хотите заказат путевку для {client_orders} на период с {day_start} 12:00 до {day_end} 11:00?\n{tel}-Ваш номер телефона?\nОбщая сумма составляет {summa} сумов\nЕсли вы уверены то выберите тип оплаты.\n*При выборе оплаты наличными забронируется комната тому кто первый произвел оплату \n\nВыберите тип оплаты:'
                await message.answer(txt, reply_markup=pays_commerc)
                await not_work.paytype.set()

        except:
            room_text = 'За выбранный период свободных комнат нет \nВыберите текущий или следующий год ⬇️:'
            await message.answer(room_text, reply_markup=year)
            await not_work.year.set()

    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work.paytype)
async def set_fio(message: Message, state: FSMContext):
    try:
        pays_x = ['Click 💳', 'Payme 💳', 'Наличными 💵']
        if message.text in pays_x:
            await state.update_data(pay_type=message.text)
            data = await state.get_data()
            fio = data.get('fio')
            pay_type = data.get('pay_type')
            user_id = message.from_user.id
            await state.finish()
            select_user_orders = await commands.select_ord_pay(user_id)
            if pay_type == 'Наличными 💵':
                for order in select_user_orders:
                    txt = f'{order.fio} ваш заказ оформлен!\nНомер вашего заказа {order.order_id},\nНомер комнаты: {order.room_number}\nПериод с {order.date_start} 12:00 до {order.date_end} 11:00\nСумма заказ:{order.summa}  \nно для вступления заказа в силу нужно произвезти оплату'
                    await message.answer(txt, reply_markup=lang_btn)
                    await order.update(paytype=pay_type).apply()
            elif pay_type == 'Click 💳':
                pass
            elif pay_type == 'Payme 💳':
                pass
            else:
                await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)

        else:
            await message.answer('Выберите тип оплаты ⬇️:', reply_markup=pays)
            await not_work.paytype.set()
    except:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()
