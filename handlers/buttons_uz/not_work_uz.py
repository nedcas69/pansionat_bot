import json
import re

import requests
from requests.auth import HTTPBasicAuth
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from datetime import date, timedelta

from data.config import C_USER, C_PASS, C_URI
from keyboards import kb_uz, month_uz, years_uz, conatct_uz, cancel_uz, pays_uz,room_uz, order_commerc1_uz,\
     order_commerc2_uz, pays_commerc_uz
from loader import dp
from state import not_work_uz
from keyboards import lang_btn
from filters import IsPrivate
from utils.db_api import quick_commands as commands


@dp.message_handler(text='Буюртмани бекор қилиш ❌',
                    state=[not_work_uz.fio, not_work_uz.dates, not_work_uz.orders, not_work_uz.year, not_work_uz.months, not_work_uz.dayru,
                           not_work_uz.paytype])
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
    await message.answer('Буюртма бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(text='Буюртмани бекор қилиш ❌')
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
    await message.answer('Буюртма бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(IsPrivate(), text="\"Узметкомбинат\"АЖ ходими эмасман")
async def not_work_uzed(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("ФИШ паспорт бўйича ёзинг.", reply_markup=cancel_uz)
    await not_work_uz.fio.set()


@dp.message_handler(IsPrivate(), state=not_work_uz.fio)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    fio = message.text
    if len(fio) > 5:
        await message.answer(f"{fio} телефон рақамингизни юборинг! ⬇️", reply_markup=conatct_uz)
        await not_work_uz.tel.set()
    else:
        await message.answer("ФИШ паспорт бўйича тўғри ёзинг.", reply_markup=cancel_uz)
        await not_work_uz.fio.set()


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=not_work_uz.tel)
async def set_fio(message: Message, state: FSMContext):
    tel = message.contact.phone_number
    data = await state.get_data()
    fio = data.get('fio')
    await state.update_data(tel=tel)
    if len(tel) > 7:
        await message.answer('Йўлланма буюртма бериш ёки\nБуюртмани бекор қилишни танланг ⬇️:', reply_markup=order_commerc2_uz)
        await not_work_uz.orders.set()
    else:
        await message.answer(f"{fio} телефон рақамингизни юборинг! ⬇️", reply_markup=conatct_uz)
        await not_work_uz.tel.set()


@dp.message_handler(IsPrivate(), state=not_work_uz.orders)
async def set_fio(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        tel = data.get('tel')
        fri = data.get('fri')
        quantity_orders = data.get('quantity_orders')
        order_type = message.text
        if order_type == 'Йўлланма буюртма бериш' or fri and order_type != 'Йўлланма буюртма беришни тугатиш':
            await state.update_data(fri=True)
            fio = message.text
            if fio != 'Йўлланма буюртма бериш':
                if fio != 'Йўлланма буюртма беришни тугатиш':
                    await commands.add_order(message.from_user.id, fio, '0', False, tel, commerc_100=100)
            if fio == 'Йўлланма буюртма беришни тугатиш':
                await state.update_data(fri=False)
            else:
                text = 'ФИШ паспорт бўйича ёзинг\n ёки Йўлланма буюртма беришни тугатиш танланг⬇️!'
                await message.answer(text, reply_markup=order_commerc1_uz)
        elif order_type == 'Йўлланма буюртма беришни тугатиш':
            await state.update_data(fri=False)
            await state.update_data(quantity_orders=True)
            order_days = 'Қанча кун дам олишни хоҳлаётганингизни рақамли форматда ёзинг (0-9).'
            await message.answer(order_days)
        elif quantity_orders:
            try:
                order_day = int(message.text)
                await state.update_data(quantity_orders=False)
                await state.update_data(order_day=order_day)
                await message.answer('Жорий ёки кейинги йилни танланг ⬇️:', reply_markup=years_uz)
                await not_work_uz.year.set()
            except:
                order_days = 'Қанча кун дам олишни хоҳлаётганингизни <b>рақамли форматда ёзинг (0-9)</b>.'
                await message.answer(order_days)
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work_uz.year)
async def set_fio(message: Message, state: FSMContext):
    try:
        year_now = date.today()
        if message.text == f'{year_now.year}' or message.text == f'{int(year_now.year) + 1}':
            await state.update_data(year=message.text)
        else:
            await message.answer('Жорий ёки кейинги йилни танланг ⬇️:', reply_markup=years_uz)
            await not_work_uz.year.set()

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
                    jan = 'Январ'
                    i += 1
                if i == 2:
                    feb = 'Феврал'
                    i += 1
                if i == 3:
                    mar = 'Март'
                    i += 1
                if i == 4:
                    apr = 'Апрел'
                    i += 1
                if i == 5:
                    may = 'Май'
                    i += 1
                if i == 6:
                    jun = 'Июн'
                    i += 1
                if i == 7:
                    jul = 'Июл'
                    i += 1
                if i == 8:
                    avg = 'Август'
                    i += 1
                if i == 9:
                    sep = 'Сентябр'
                    i += 1
                if i == 10:
                    octob = 'Октябр'
                    i += 1
                if i == 11:
                    nov = 'Ноябр'
                    i += 1
                if i == 12:
                    dec = 'Декабр'
                    i += 1
                break

        else:
            jan = 'Январ'
            feb = 'Феврал'
            mar = 'Март'
            apr = 'Апрел'
            may = 'Май'
            jun = 'Июн'
            jul = 'Июл'
            avg = 'Август'
            sep = 'Сентябр'
            octob = 'Октябр'
            nov = 'Ноябр'
            dec = 'Декабр'

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
                    KeyboardButton(text='Буюртмани бекор қилиш ❌')
                ],
            ],
            resize_keyboard=True,
        )

        await message.answer('Oйни танланг ⬇️:', reply_markup=mont)
        await not_work_uz.months.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work_uz.months)
async def set_fio(message: Message, state: FSMContext):
    try:
        if message.text == 'Январ':
            await state.update_data(months=1)
            await state.update_data(months_txt='Январ')
        elif message.text == 'Феврал':
            await state.update_data(months=2)
            await state.update_data(months_txt='Феврал')
        elif message.text == 'Март':
            await state.update_data(months=3)
            await state.update_data(months_txt='Март')
        elif message.text == 'Апрел':
            await state.update_data(months=4)
            await state.update_data(months_txt='Апрел')
        elif message.text == 'Май':
            await state.update_data(months=5)
            await state.update_data(months_txt='Май')
        elif message.text == 'Июн':
            await state.update_data(months=6)
            await state.update_data(months_txt='Июн')
        elif message.text == 'Июл':
            await state.update_data(months=7)
            await state.update_data(months_txt='Июл')
        elif message.text == 'Август':
            await state.update_data(months=8)
            await state.update_data(months_txt='Август')
        elif message.text == 'Сентябр':
            await state.update_data(months=9)
            await state.update_data(months_txt='Сентябр')
        elif message.text == 'Октябр':
            await state.update_data(months=10)
            await state.update_data(months_txt='Октябр')
        elif message.text == 'Ноябр':
            await state.update_data(months=11)
            await state.update_data(months_txt='Ноябр')
        elif message.text == 'Декабр':
            await state.update_data(months=12)
            await state.update_data(months_txt='Декабр')
        else:
            await message.answer('Бундай ой йўқ.\nТўғри ойни танланг ⬇️:', reply_markup=month_uz)
            await not_work_uz.months.set()

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
            await message.answer('Бу ойда барча кунлар банд.\nБошқа ойни танланг ⬇️:', reply_markup=month_uz)
            await not_work_uz.months.set()
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

            cancel_kb = [KeyboardButton(text='Буюртмани бекор қилиш ❌')]
            kb.append(cancel_kb)
            canceld = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await state.update_data(day_x=days)
            await message.answer('Kунни танланг ⬇️:', reply_markup=canceld)
            await not_work_uz.dayru.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work_uz.dayru)
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
                await message.answer('Ўтган кунга буюртма бериб бўлмайди\nБуюртма бекор қилинди.', reply_markup=lang_btn)

            txt = f'Хона тоифасини танланг ⬇️:'
            await message.answer(txt, reply_markup=room_uz)
            await not_work_uz.cat_room.set()

    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()
    await state.update_data(o70=True)


@dp.message_handler(IsPrivate(), state=not_work_uz.cat_room)
async def set_day(message: Message, state: FSMContext):
    try:
    # if True:
        if message.text == 'Стандарт':
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

        end_kb = [KeyboardButton(text='Буюртмани тугатинг.')]
        cancel_kb = [KeyboardButton(text='Буюртмани бекор қилиш ❌')]
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

            # kb.append(end_kb)
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
                txt = f'{select_user_orders[0].fio} учун хона танланг ⬇️:'
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

                tx = f'{select_user_orders[1].fio} учун хона танланг ⬇️:'
                await message.answer(tx, reply_markup=rooms)

            except:
                pass

            if await commands.select_ord_room(user_id) == []:
                summa = await commands.summas(user_id)
                txt = f'{fio} сиз йўлланмани {client_orders}, {day_start} 12:00 дан {day_end} 11:00 муддатга буюртма қилмоқчимисиз?\nСизнинг тел-рақамингиз - {tel} шуми?\nЖами {summa} сўм\nАгар ишончингиз комил бўлса, унда тўлов турини танланг.\n*Агар сиз нақд пул билан тўлашни танласангиз, биринчи бўлиб тўловни амалга оширган шахс учун хона ажратилади \n\nТўлов турини танланг ⬇️:'
                await message.answer(txt, reply_markup=pays_commerc_uz)
                await not_work_uz.paytype.set()

        except:
            room_text = 'Танланган давр учун мавжуд хоналар мавжуд емас \nЖорий ёки кейинги йилни танланг ⬇️:'
            await message.answer(room_text, reply_markup=years_uz)
            await not_work_uz.year.set()

    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=not_work_uz.paytype)
async def set_fio(message: Message, state: FSMContext):
    try:
        pays_x = ['Click 💳', 'Payme 💳', 'Нақт пулга 💵']
        if message.text in pays_x:
            await state.update_data(pay_type=message.text)
            data = await state.get_data()
            fio = data.get('fio')
            pay_type = data.get('pay_type')
            user_id = message.from_user.id
            await state.finish()
            select_user_orders = await commands.select_ord_pay(user_id)
            if pay_type == 'Нақт пулга 💵':
                for order in select_user_orders:
                    txt = f'{order.fio} сизнинг буюртмангиз тайёрланди!\nБуюртма рақамингиз {order.order_id},\nХона рақами: {order.room_number}\nМуддат {order.date_start} 12:00 дан {order.date_end} 11:00гача\nБуюртма нархи:{order.summa}  \nаммо буюртма кучга кириши учун сиз тўловни амалга оширишингиз керак'
                    await message.answer(txt, reply_markup=lang_btn)
                    await order.update(paytype=pay_type).apply()
            elif pay_type == 'Click 💳':
                pass
            elif pay_type == 'Payme 💳':
                pass
            else:
                await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)

        else:
            await message.answer('Тўлов турини танланг ⬇️:', reply_markup=pays_uz)
            await not_work_uz.paytype.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()
