from datetime import date

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Сотрудник АО "Узметкомбинат"'),
        ],
        [
            KeyboardButton('Пенсионер АО "Узметкомбинат"'),
        ],
        [
            KeyboardButton('Не работает АО "Узметкомбинат"'),
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],

    ],
    resize_keyboard=True
)

conatct_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Отправить свой контакт ☎️', request_contact=True),
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True
)

month = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'Январь'),
            KeyboardButton(text=f'Февраль')
        ],
        [
            KeyboardButton(text=f'Март'),
            KeyboardButton(text=f'Апрель')
        ],
        [
            KeyboardButton(text=f'Май'),
            KeyboardButton(text=f'Июнь')
        ],
        [
            KeyboardButton(text=f'Июль'),
            KeyboardButton(text=f'Август')
        ],
        [
            KeyboardButton(text=f'Сентябрь'),
            KeyboardButton(text=f'Октябрь')
        ],
        [
            KeyboardButton(text=f'Ноябрь'),
            KeyboardButton(text=f'Декабрь')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
)

year_now = date.today()
year = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'{year_now.year}'),
            KeyboardButton(text=f'{int(year_now.year) + 1}'),
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

room = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Стандартный'),
            KeyboardButton(text='Люкс'),
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Себе 35%')
        ],
        [
            KeyboardButton(text='Семье 70%')
        ],
        [
            KeyboardButton(text='Пенсионеру АО "Узметкомбинат" 30%')
        ],
        [
            KeyboardButton(text='Другу 100%')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_selected = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Себе 35%'),
            KeyboardButton(text='Семье 70%')
        ],
        [
            KeyboardButton(text='Пенсионеру АО "Узметкомбинат" 30%'),

        ],
        [
            KeyboardButton(text='Другу 100%'),
        ],
        [
            KeyboardButton(text='Закончить заказ путевок'),
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_commerc1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Закончить заказ путевок')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_commerc2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заказать путевку')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

pays = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Наличными 💵')
        ],
        [
            KeyboardButton(text='За счёт зарплаты 💵')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

pays_commerc = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Наличными 💵')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

ans = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
