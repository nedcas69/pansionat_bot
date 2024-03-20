from asyncpg import UniqueViolationError
from datetime import date, timedelta

from utils.db_api.schemas.orders import Order, Room as Room


async def add_orders(user_id: int, room_id: int, fio: str, room_number: str, room_class: str, date_start, date_end,
                     tabel: str, work: bool, tel: str, sebe_35=0, pension_30=0, semye_70=0, commerc_100=0):
    try:
        room = await select_room(room_id)
        seats = room.number_of_seats
        rooms = await select_order_by_date(date_start, date_end)
        i = 0
        for rom in rooms:
            if rom.room_id == room_id:
                i += 1
        if seats > i:
            order = Order(user_id=user_id, room_id=room_id, fio=fio, work=work, room_number=room_number,
                          room_class=room_class, date_start=date_start, date_end=date_end,
                          tabel=tabel, tel=tel)
            await order.create()
            print("Заказ создан!")
        else:
            return False, print('komnata zaneta')
    except UniqueViolationError:
        print("Заказ не создан!")


async def add_order(user_id: int, fio: str, tabel: str, work: bool, tel: str, sebe_35=0, pension_30=0,
                    semye_70=0,
                    commerc_100=0):
    order = Order(user_id=user_id, fio=fio, work=work, tabel=tabel, tel=tel,
                  sebe_35=sebe_35, pension_30=pension_30, semye_70=semye_70, commerc_100=commerc_100)
    await order.create()
    print("Заказ создан!")


async def select_room(room_id):
    room = await Room.query.where(Room.id == room_id).gino.first()
    return room


async def select_room_name(number):
    room = await Room.query.where(Room.number == number).gino.first()
    return room


async def select_all_orders():
    orders = await Order.query.gino.all()
    return orders


async def select_all_rooms(category_rooms):
    rooms = await Room.query.where(Room.room_category == category_rooms).gino.all()
    return rooms


#
# async def select_all_dates():
#     dates = await Order.query(orders.dates).gino.all()
#     return dates


async def select_order(room_id):
    order = await Order.query.where(Order.room_id == room_id).gino.all()
    return order


async def select_ord(order_id):
    order = await Order.query.where((Order.order_id == order_id) & (Order.summa > 0)).gino.first()
    return order


async def select_ord_room(user_id):
    order = await Order.query.where(
        (Order.user_id == user_id) & (Order.room_number == None)).gino.all()
    return order


async def summas(user_id):
    orders = await Order.query.where(
        (Order.user_id == user_id) & (Order.pay_status == False)).gino.all()
    summa = 0
    for order in orders:
        summa += order.summa

    return summa


async def select_ord_pay(user_id):
    order = await Order.query.where(
        (Order.user_id == user_id) & (Order.pay_status == False) & (Order.room_number != 0)).gino.all()
    return order


async def select_order_by_date(date_start, date_end):
    days_end = date_start + timedelta(days=1)
    days_start = date_end - timedelta(days=1)
    try:
        order = await Order.query.where(
            (Order.date_start <= date_start) & (Order.date_end >= days_end) & (Order.pay_status == True) |
            (Order.date_start <= days_start) & (Order.date_end >= date_end) & (Order.pay_status == True)).gino.all()
        return order
    except:
        order = await Order.query.where(
            (Order.date_start <= date_start) & (Order.date_end >= days_end) & (Order.pay_status == True) | (
                    Order.date_start <= days_start) &
            (Order.date_end >= date_end) & (Order.pay_status == True)).gino.all()
        return order


async def select_order_by_date_admin(year, month):
    try:
        # if True:
        dates = []
        for i in range(1, 32):
            year_now = date(int(year), int(month), i)
            dates.append(year_now)
            day = year_now.day
    except:
        pass
    date_start = dates[0]
    date_end = dates[-1]
    order = []
    try:
        orders = await Order.query.where((Order.pay_status == True) & (Order.summa > 0)).gino.all()
        for ord in orders:
            if ord.date_start in dates or ord.date_end in dates:
                order.append(ord)
        return order
    except:
        orders = await Order.query.where((Order.pay_status == True) & (Order.summa > 0)).gino.all()
        for ord in orders:
            if ord.date_start in dates or ord.date_end in dates:
                order.append(ord)
        return order


async def select_order_by_date_room(date_start, date_end):
    days_end = date_start + timedelta(days=1)
    days_start = date_end - timedelta(days=1)
    try:
        order = await Order.query.where(
            (Order.date_start <= date_start) & (Order.date_end >= days_end) |
            (Order.date_start <= days_start) & (Order.date_end >= date_end)).gino.all()
        return order
    except:
        order = await Order.query.where(
            (Order.date_start <= date_start) & (Order.date_end >= days_end) | (
                    Order.date_start <= days_start) &
            (Order.date_end >= date_end)).gino.all()
        return order


async def select_order_id(fio, order_id):
    order = await Order.query.where((Order.fio == fio) & (Order.order_id == order_id)).gino.first()
    return order


async def select_orderid(user_id):
    order = await Order.query.where((Order.user_id == user_id) & (Order.pay_status == False) &
                                    (Order.room_number == None)).gino.all()
    return order


async def select_date(order_id, date_start, date_end):
    order = await Order.query.where(Order.order_id == order_id).gino.all()
    for i in order:
        await i.update(date_start=date_start).apply()
        await i.update(date_end=date_end).apply()


async def paid(order_id):
    try:
        orders = await select_ord(order_id)
        room = await select_room(orders.room_id)
        seats = room.number_of_seats
        rooms = await select_order_by_date(orders.date_start, orders.date_end)
        i = 0
        for rom in rooms:
            if rom.room_id == orders.room_id:
                i += 1
        if seats > i:
            order = await select_ord(order_id)
            await order.update(pay_status=True).apply()
            print("Заказ оплачен!")
        else:
            return False, print('komnata zaneta')
    except UniqueViolationError:
        print("Заказ не оплачен!")


async def room_number(fio, order_id, room_id, room_numbers, room_class, date_start, date_end, summa):
    try:
        room = await select_room(room_id)
        seats = room.number_of_seats
        rooms = await select_order_by_date_room(date_start, date_end)
        i = 0
        order = await select_order_id(fio, order_id)
        # for rom in rooms:
        #     if rom.room_id == room_id:
        #         i += 1
        # if seats > i:
        await order.update(room_id=room_id).apply()
        await order.update(room_number=int(room_numbers)).apply()
        await order.update(room_class=room_class).apply()
        await order.update(date_start=date_start).apply()
        await order.update(date_end=date_end).apply()
        await order.update(summa=summa).apply()
        print("Заказ обновлен!")
    # else:
    #     return False, print('komnata zaneta')

    except UniqueViolationError:
        print("Заказ не обновлен!")


async def room_number_quit(user_id, room_id, room_number, room_class, date_start, date_end):
    try:
        room = await select_room(room_id)
        i = 0
        orders = await select_orderid(user_id)
        for order in orders:
            await order.update(room_id=room_id).apply()
            await order.update(pay_status=True).apply()
            await order.update(room_number=room_number).apply()
            await order.update(room_class=room_class).apply()
            await order.update(date_start=date_start).apply()
            await order.update(date_end=date_end).apply()
            print("Заказ обновлен!")

    except UniqueViolationError:
        print("Заказ не обновлен!")


async def unpaid(order_id):
    order = await select_ord(order_id)
    await order.update(pay_status=False).apply()


async def change_day(order_id, dates):
    order = await select_ord(order_id)
    await order.update(dates=dates).apply()


async def change_pay(order_id, summa):
    order = await select_ord(order_id)
    await order.update(summa=summa).apply()
