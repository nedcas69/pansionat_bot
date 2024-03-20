from sqlalchemy import Column, BigInteger, String, sql, Date, Boolean, Integer, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class Order(TimedBaseModel):
    __tablename__ = 'order'
    order_id = Column(Integer(), primary_key=True)
    room_id = Column(Integer())
    user_id = Column(BigInteger())
    fio = Column(String(255))
    tel = Column(String(25))
    room_number = Column(Integer())
    room_class = Column(String(25))
    work = Column(Boolean(), default=False)
    date_start = Column(Date())
    date_end = Column(Date())
    tabel = Column(String(15))
    paytype = Column(String(150))
    pay_status = Column(Boolean(), default=False)
    sebe_35 = Column(Integer(), default=0)
    pension_30 = Column(Integer(), default=0)
    semye_70 = Column(Integer(), default=0)
    commerc_100 = Column(Integer(), default=0)
    summa = Column(Integer(), default=0)

    query: sql.select


class Room(TimedBaseModel):
    __tablename__ = 'room'
    id = Column(Integer(), primary_key=True)
    number = Column(String(15))
    number_of_seats = Column(Integer())
    room_category = Column(String(25))

    query: sql.select
