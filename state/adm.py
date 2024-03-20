from aiogram.dispatcher.filters.state import StatesGroup, State


class admin(StatesGroup):
    year_admin = State()
    months_admin = State()
    year_admin_change = State()
    months_admin_change = State()
    day_change = State()
    result_adm = State()
    order_number = State()
    order_change = State()
    pay = State()