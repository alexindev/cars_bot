from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[str]
    driver_id: Mapped[str]
    car_id: Mapped[str]
    is_staff: Mapped[bool]
    full_name: Mapped[str]

    def __repr__(self):
        return (f'full_name: {self.full_name}, chat_id: {self.chat_id}, phone: {self.phone}, '
                f'driver_id: {self.driver_id}, car_id: {self.car_id}, is_staff: {self.is_staff}')

