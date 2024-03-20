import asyncio
import json
import re

import qrcode
import requests
from requests.auth import HTTPBasicAuth
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType, InputFile
from datetime import datetime, timedelta, date

from data.config import C_USER, C_PASS, C_URI, C_INPS, C_buh, PINFL
from keyboards import kb_uz, month_uz, years_uz, order_uz, conatct_uz, cancel_uz, pays_uz, order_selected_uz, \
    order_commerc1, order_commerc2, pays_commerc_uz, room_uz
from loader import dp
from state import uz_regis
from keyboards import lang_btn
from filters import IsPrivate
from utils.db_api import quick_commands as commands


@dp.message_handler(text='Буюртмани бекор қилиш ❌',
                    state=[uz_regis.work, uz_regis.fio, uz_regis.dates, uz_regis.orders, uz_regis.year, uz_regis.months,
                           uz_regis.dayru,
                           uz_regis.paytype])
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


@dp.message_handler(IsPrivate(), content_types=ContentType.DOCUMENT)
async def send_photo_file_id(message: Message):
    await message.reply(message.document.file_id)


@dp.message_handler(IsPrivate(), content_types=ContentType.PHOTO)
async def send_photo_file_id(message: Message):
    await message.reply(message.photo[-1].file_id)


@dp.message_handler(IsPrivate(), text='Ўзбекча 🇺🇿')
async def rusk(mess: Message):
    hello_text = "Илтимос,\"Ўзметкомбинат\"АЖ ходими еканлигингизни кўрсатинг ⬇️!"
    await mess.answer(hello_text, reply_markup=kb_uz)


@dp.message_handler(IsPrivate(), text='\"Узметкомбинат\"АЖ ходими')
async def worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Табел рақамингизни ёзинг:", reply_markup=kb_uz)
    await uz_regis.work.set()


@dp.message_handler(IsPrivate(), state=uz_regis.work)
async def reg_fio(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    try:
        await state.update_data(tabel=message.text)
        tabel = message.text
        if message.from_user.id in [562847836, 479467128]:
            auth = HTTPBasicAuth(C_USER, C_PASS)
            r = requests.get(C_URI + tabel, auth=auth)
            html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
            json_data = json.loads(html)
            name = json_data['ishchi']
            tel = json_data['telefon']
            if name != None:
                await state.update_data(fio=name)

                if tel != None:
                    await state.update_data(tel=tel)
                    await message.answer(f"{name} 1C билан текшириш учун контактизни юборинг ⬇️:", reply_markup=conatct_uz)
                    await uz_regis.telx.set()
                else:
                    tel_text = 'Цех табелчисидан тел рақамингизни 1C га қўшишини сўранг!'
                    await message.answer(tel_text, reply_markup=kb_uz)
                    await state.finish()
        else:
            auth = HTTPBasicAuth(C_USER, C_PASS)
            r = requests.get(C_URI + tabel, auth=auth)
            html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
            json_data = json.loads(html)
            name = json_data['ishchi']
            tel = json_data['telefon']
            if name != None:
                await state.update_data(fio=name)

                if tel != None:
                    await state.update_data(tel=tel)
                    await message.answer(f"{name} 1C билан текшириш учун контактизни юборинг ⬇️:", reply_markup=conatct_uz)
                    await uz_regis.telx.set()
                else:
                    tel_text = 'Цех табелчисидан рақамингизни 1C га қўшишини сўранг!'
                    await message.answer(tel_text, reply_markup=kb_uz)
                    await state.finish()
            else:
                work_txt = "Бундай табел рақами йўқ!\" Ўзметкомбинат\" АЖ ходими еканлигингизни кўрсатинг!"
                await message.answer(work_txt, reply_markup=kb_uz)
                await state.finish()
    except:
        work_txt = "Бундай табел рақами йўқ!\" Ўзметкомбинат\" АЖ ходими еканлигингизни кўрсатинг!"
        await message.answer(work_txt, reply_markup=kb_uz)
        await state.finish()


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=uz_regis.telx)
async def contct(message: Message, state: FSMContext):
    try:
        text = message.contact.phone_number
        if message.contact.user_id == message.from_user.id:
            data = await state.get_data()
            tex = data.get('tel')
            name = data.get('fio')
            if text == tex:
                await state.update_data(work=True)
                await message.answer(f"{name} Кимга йўлланма буюртма қилишни танланг ⬇️:", reply_markup=order_uz)
                await uz_regis.orders.set()
            elif text == '+' + tex:
                await state.update_data(work=True)
                await message.answer(f"{name} Кимга йўлланма буюртма қилишни танланг ⬇️:", reply_markup=order_uz)
                await uz_regis.orders.set()
            elif message.from_user.id in [562847836, 479467128]:
                await state.update_data(work=True)
                await message.answer(f"{name} Кимга йўлланма буюртма қилишни танланг ⬇️:", reply_markup=order_uz)
                await uz_regis.orders.set()
            else:
                await message.answer(f'Хато, ўрнатилган рақамни 1C дан текширинг!', reply_markup=kb_uz)
                await state.finish()
        else:
            await message.answer(f'Хато, рақамингизни юборинг!', reply_markup=kb_uz)
            await state.finish()
    except:
        await message.answer(f'Хато, ўрнатилган рақамни 1C дан текширинг!', reply_markup=kb_uz)
        await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.orders)
async def set_fio(message: Message, state: FSMContext):
    # try:
    if True:
        data = await state.get_data()
        work = data.get('work')
        quantity_order = data.get('quantity_order')
        semye = data.get('semye')
        pension = data.get('pension')
        friend = data.get('friend')
        fio = data.get('fio')
        tel = data.get('tel')
        tabel = data.get('tabel')
        o70 = data.get('o70')
        pen = data.get('pen')
        fri = data.get('fri')

        await state.update_data(user_id=message.from_user.id)
        if work:
            await state.update_data(worked=True)
            order_type = message.text
            # try:
            if True:
                if order_type == 'Ўзимга 35%':
                    await state.update_data(pen=False)
                    await state.update_data(fri=False)
                    await state.update_data(o70=False)
                    await state.update_data(sebe=1)
                    await commands.add_order(message.from_user.id, fio, tabel, True, tel, sebe_35=35)
                    text = 'Сиз ўзингиз учун йўлланма танладингиз!\n\nКимга буюртма беришни танланг ёки\nБуюртмани тугатинг:'
                    await message.answer(text, reply_markup=order_selected_uz)

                elif order_type == 'Оилага 70%' or o70:
                    await state.update_data(fri=False)
                    await state.update_data(pen=False)
                    semyas = []
                    auth = HTTPBasicAuth(C_USER, C_PASS)
                    r = requests.get(C_URI + tabel, auth=auth)
                    html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
                    json_data = json.loads(html)
                    oila = json_data['oila']
                    kb_family = []
                    family = []
                    for i in oila:
                        if i["qarindoshlik"] in ["Отец", "Мать", "Жена", "Дочь", "Сын"]:
                            kb_family.append([KeyboardButton(text=f'{i["FIO"]}')])
                            family.append(i["FIO"])

                    canceld = ReplyKeyboardMarkup(
                        keyboard=kb_family,
                        resize_keyboard=True,
                        one_time_keyboard=True
                    )
                    if message.text in family:
                        semya = message.text
                        await commands.add_order(message.from_user.id, semya, tabel, False, tel, semye_70=70)
                        text = 'Кимга буюртма беришни хоҳлаётганингизни танланг ёки \nБуюртмани тугатинг:'
                        await message.answer(text, reply_markup=order_selected_uz)
                        await state.update_data(o70=False)
                    else:
                        await state.update_data(o70=True)
                        if semye == None:
                            semye = 0
                        semex = int(semye) + 1
                        await state.update_data(semye=semex)
                        text = 'Оила аъзоингизни танланг ⬇️:'
                        await message.answer(text, reply_markup=canceld)

                elif order_type == '"Ўзметкомбинат" АЖ пенсионерига 30%' or pen:
                    await state.update_data(o70=False)
                    await state.update_data(fri=False)
                    pensx = []
                    if pen:
                        try:
                            # if True:
                            pinfl = message.text
                            auth = HTTPBasicAuth(C_USER, C_PASS)
                            r = requests.get(C_INPS + pinfl, auth=auth)
                            pen_name = r.text.encode('ISO-8859-1').decode('utf-8-sig')
                            print(pen_name, pinfl)
                            if pen_name != '':
                                await commands.add_order(message.from_user.id, pen_name, tabel, False, tel,
                                                         pension_30=30)
                                text = f'{pen_name} маълумотингиз киритилди\nКимга буюртма беришни хоҳлаётганингизни танланг ёки \nБуюртмани тугатинг:'
                                await message.answer(text, reply_markup=order_selected_uz)
                                await state.update_data(pen=False)
                            await state.update_data(pen=False)
                        except:
                            pass
                    else:
                        await state.update_data(pen=True)
                        if pension == None:
                            pension = 0
                        pensionx = int(pension) + 1
                        await state.update_data(pension=pensionx)
                        text = 'Пенсионернинг паспортидаги жисмоний шахснинг шахсий идентификацион рақами(ПИНФЛ) ёзинг!'
                        await message.answer_photo(PINFL)
                        await message.answer(text, reply_markup=cancel_uz)

                elif order_type == 'Дўстга 100%' or fri:
                    await state.update_data(o70=False)
                    await state.update_data(pen=False)
                    fries = []
                    if fri:
                        friends = message.text
                        if len(message.text) > 7:
                            fries.append(message.text)
                        await commands.add_order(message.from_user.id, friends, tabel, False, tel, commerc_100=100)
                        text = 'Кимга буюртма беришни хоҳлаётганингизни танланг ёки \nБуюртмани тугатинг:'
                        await message.answer(text, reply_markup=order_selected_uz)
                        await state.update_data(fri=False)
                    else:
                        await state.update_data(fri=True)
                        if friend == None:
                            friend = 0
                        friendx = int(friend) + 1
                        await state.update_data(friend=friendx)
                        text = 'Паспорт бўйича дўстингизнинг тўлиқ исмини ёзинг!'
                        await message.answer(text)

                elif order_type == 'Йўлланма буюртма беришни тугатиш':
                    await state.update_data(fri=False)
                    await state.update_data(o70=False)
                    await state.update_data(pen=False)
                    await state.update_data(work=False)
                    await state.update_data(quantity_order=True)
                    order_days = 'Қанча кун дам олишни хоҳлаётганингизни рақамли форматда ёзинг (0-9).'
                    await message.answer(order_days)
                else:
                    await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
                    await state.finish()
            # except:
            #     pass

        elif quantity_order:
            try:
                order_day = int(message.text)
                await state.update_data(quantity_order=False)
                await state.update_data(order_day=order_day)
                await message.answer('Жорий ёки кейинги йилни танланг ⬇️:', reply_markup=years_uz)
                await uz_regis.year.set()
            except:
                order_days = 'Қанча кун дам олишни хоҳлаётганингизни <b>рақамли форматда ёзинг (0-9)</b>.'
                await message.answer(order_days)
    # except:
    #     await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
    #     await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.year)
async def set_fio(message: Message, state: FSMContext):
    try:
        year_now = date.today()
        if message.text == f'{year_now.year}' or message.text == f'{int(year_now.year) + 1}':
            await state.update_data(year=message.text)
        else:
            await message.answer('Жорий ёки кейинги йилни танланг ⬇️:', reply_markup=years_uz)
            await uz_regis.year.set()

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
        await uz_regis.months.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.months)
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
            await uz_regis.months.set()

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
            await uz_regis.months.set()
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
            await message.answer('Кунни танланг ⬇️:', reply_markup=canceld)
            await uz_regis.dayru.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.dayru)
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
                await message.answer('Ўтган кунга буюртма бериб бўлмайди!\nБуюртма бекор қилинди.',
                                     reply_markup=lang_btn)

            txt = f'Хона тоифасини танланг ⬇️:'
            await message.answer(txt, reply_markup=room_uz)
            await uz_regis.cat_room.set()

    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()
    await state.update_data(o80=True)


@dp.message_handler(IsPrivate(), state=uz_regis.cat_room)
async def set_day(message: Message, state: FSMContext):
    try:
        if message.text == 'Стандартный':
            await state.update_data(category_rooms='Standart')
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
        user_id = data.get('user_id')

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

            kb.append(end_kb)
            kb.append(cancel_kb)
            rooms = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            client_orders = ''
            lgots = 0
            select_user_orders = await commands.select_ord_room(user_id)
            o80 = data.get('o80')
            leto = [6, 7, 8]
            day = 0
            summa = 0
            if o80:
                txt = f'{select_user_orders[0].fio} учун хонани танланг⬇️:'
                await message.answer(txt, reply_markup=rooms)

            try:
                await state.update_data(o80=False)
                room_num = message.text
                mat = re.search('\d\d\d', room_num)
                roomsx = await commands.select_room_name(mat[0])
                lgots += select_user_orders[0].sebe_35 + select_user_orders[0].semye_70 + select_user_orders[
                    0].pension_30 + \
                         select_user_orders[0].commerc_100

                while day < order_day:
                    days_end = day_start + timedelta(days=day)
                    if select_user_orders[0].commerc_100:
                        if days_end.month in leto:
                            if roomsx.room_category == 'Lyuks':
                                summa += (lgots / 100) * 564000
                            if roomsx.room_category == 'Standart':
                                summa += (lgots / 100) * 376000
                        else:
                            if roomsx.room_category == 'Lyuks':
                                summa += (lgots / 100) * 414000
                            if roomsx.room_category == 'Standart':
                                summa += (lgots / 100) * 276000
                    else:
                        if roomsx.room_category == 'Lyuks':
                            summa += (lgots / 100) * 414000
                        if roomsx.room_category == 'Standart':
                            summa += (lgots / 100) * 276000
                    day += 1

                await commands.room_number(select_user_orders[0].fio, select_user_orders[0].order_id,
                                           roomsx.id, roomsx.number, roomsx.room_category, day_start, day_end, summa)
                client_orders += select_user_orders[0].fio + ', '
                tx = f'{select_user_orders[1].fio} учун хонани танланг⬇️:'
                await message.answer(tx, reply_markup=rooms)

            except:
                pass

            if await commands.select_ord_room(user_id) == []:
                summa = await commands.summas(user_id)
                txt = f'{fio} сиз йўлланмани {day_start} 12:00 дан {day_end} 11:00 муддатга буюртма қилмоқчимисиз?\nСизнинг тел-рақамингиз - {tel} шуми?\nЖами {summa} сўм\nАгар ишончингиз комил бўлса, унда тўлов турини танланг.\n*Агар сиз нақд пул билан тўлашни танласангиз, биринчи бўлиб тўловни амалга оширган шахс учун хона ажратилади \n\nТўлов турини танланг ⬇️:'
                await message.answer(txt, reply_markup=pays_uz)
                await uz_regis.paytype.set()

        except:
            room_text = 'Танланган давр учун мавжуд хоналар мавжуд емас \nЖорий ёки кейинги йилни танланг ⬇️:'
            await message.answer(room_text, reply_markup=years_uz)
            await uz_regis.year.set()

    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.paytype)
async def set_fio(message: Message, state: FSMContext):
    pays_x = ['Click 💳', 'Payme 💳', 'Нақт пулга 💵', 'Иш ҳақи ҳисобидан 💵']
    try:
    # if True:
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
            elif pay_type == 'Иш ҳақи ҳисобидан 💵':
                roomType = 0
                for order in select_user_orders:
                    if order.room_class == 'Standart':
                        roomType = 1
                    if order.room_class == 'Lyuks':
                        roomType = 2

                    paymentType = 0
                    if order.sebe_35 != 0:
                        paymentType = 1
                    if order.pension_30 != 0:
                        paymentType = 4
                    if order.semye_70 != 0:
                        paymentType = 2
                    if order.commerc_100 != 0:
                        paymentType = 3
                    start = str(order.date_start.strftime('%Y%m%d'))
                    end = str(order.date_end.strftime('%Y%m%d'))
                    data = {
                        "tabNomer": order.tabel,
                        "period1": start,
                        "period2": end,
                        "roomType": roomType,
                        "paymentType": paymentType,
                        "vacationer": order.fio
                    }
                    print(data)
                    auth = HTTPBasicAuth(C_USER, C_PASS)
                    r = requests.post(C_buh, auth=auth, json=data)
                    if r.status_code == 201:
                        await order.update(paytype=pay_type).apply()
                        await order.update(pay_status=True).apply()
                        order_id = int(order.order_id)
                        orders = await commands.select_ord(order_id)
                        txt_QRcode = f'Буюртма рақамингиз: {order.order_id}\nФИО: {order.fio}\nХона рақами: {order.room_number}\nМуддат: {order.date_start} 12:00 дан {order.date_end} 11:00гача\nТел: {order.tel}\nТўлов холати {order.pay_status}\nТўлов тури: {order.paytype}\nТўлов нархи: {order.summa}'
                        data = txt_QRcode
                        filename = "site.png"
                        img = qrcode.make(data)
                        img.save(filename)
                        if orders.pay_status:
                            await asyncio.sleep(2)
                            imgs = InputFile(path_or_bytesio=filename)
                            await message.answer_document(document=imgs)

                        txt = f'{order.fio} сизнинг буюртмангиз тайёрланди! Буюртма нархи уч ой давомида ойликдан ушлаб қолинади.\nБуюртма рақамингиз {order.order_id},\nХона рақами: {order.room_number}\nМуддат {order.date_start} 12:00 дан {order.date_end} 11:00гача\nБуюртма нархи:{order.summa} '
                        await message.answer(txt, reply_markup=lang_btn)
                    else:
                        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
                        await state.finish()

            elif pay_type == 'Payme 💳':
                pass
            else:
                await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)

        else:
            await message.answer('Выберите тип оплаты ⬇️:', reply_markup=pays_uz)
            await uz_regis.paytype.set()
    except:
        await message.answer('Буюртма бекор қилинди. Хатолик юз берди!', reply_markup=lang_btn)
        await state.finish()
