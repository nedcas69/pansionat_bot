import asyncio
from datetime import date, timedelta
import re

# from data import config
from utils.db_api import quick_commands as commands
from utils.db_api.db_gino import db


async def db_test():
    # await db.set_bind(config.POSTGRES_URI)
    await db.set_bind('postgresql://postgres:12369@localhost/trades')
    # await db.gino.drop_all()
    # await db.gino.create_all()
    day_start = date(2023, 10, 17)
    day_end = day_start + timedelta(days=10)
    room = await commands.select_room(11)
    category = room.room_category
    # seats = room.number_of_seats
    # orders = await commands.select_all_orders()
    # orders_by_id = await commands.select_ord(1)
    orders_name = []
    # await commands.add_order(562847836, 'semya', 'tabel', False, 'tel', semye_70=70)
    # select_user_orders = await commands.select_ord_room(562847836)
    # await commands.room_number(select_user_orders[0].fio, select_user_orders[0].order_id,
    #                            room.id, room.number, room.room_category, day_start, day_end)
    # mont = date.today().month
    # print(select_user_orders[0].fio,)
    # room_number_update = await commands.room_number(sebe.fio, sebe.order_id, '211')
    # room_number_update = await commands.room_number(semye.fio, semye.order_id, '211')
    # room_number_update = await commands.room_number(fri.fio, fri.order_id, '211')
    # admin = await commands.select_order_by_date_admin(2023,11)
    # for i in admin:
    #     print(i.fio, i.room_number, i.room_class)
    # print(admin)
    order = await commands.select_order_by_date(day_start, day_end)
    room_numbers = await commands.select_all_rooms(category)
    number_lists = []
    mat = re.search('\d\d\d', '213:2')
    print(mat[0])
    roomsx = await commands.select_room_name(mat[0])
    print(roomsx.id)
    for num in room_numbers:
        o = 0
        while o < num.number_of_seats:
            number_lists.append(num.number)
            o += 1
    bron_room_numbers = []
    for rom in order:
        print(rom.room_number)
        bron_room_numbers.append(rom.room_number)
    orders = await commands.select_all_orders()
    # last_order = orders.pop()
    # print(last_order.order_id)
    order = []
    # order = await commands.select_order_by_date(2023, 11)
    # for ord in orders:
    #     if ord.noxor == False:
    #         order.append(ord.dates.day)
    order_id = []
    # result = [i for i in number_lists if not i in bron_room_numbers or bron_room_numbers.remove(i)]
    # await commands.add_orders(14, room.id, 'Djuraev Shaxboz', room.number, category, day_start, day_end, '57394', True,
    #                            '+998901282852',)
    # setList = list(set(result))
    # my_dict = {i: result.count(i) for i in setList}
    # print(my_dict, result, sep='\n\n')
    # # print(bron_room_numbers)
    # for i in result:
    #     if i not in order_id:
    #         order_id.append(i)
    # print(order_id)
    # # print(order)
    # if '211' in result:
    #     print('211 bo\'sh')
    # try:
    #     for i in range(1, 32):
    #         year_now = date(2023, 5, i)
    #         if i in order:
    #             continue
    #         print(year_now)
    # except ValueError:
    #     pass
    #
    # work_update = await commands.update_work(14)
    # order = await commands.select_order(14)
    # await order.update(noxor=True).apply()


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
