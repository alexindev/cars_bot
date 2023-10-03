from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import BigInteger, ForeignKey


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
    park: Mapped['Park'] = relationship(back_populates='user')
    park_id: Mapped[int] = mapped_column(ForeignKey('parks.id'))

    def __repr__(self):
        return (f'full_name: {self.full_name}, chat_id: {self.chat_id}, phone: {self.phone}, '
                f'driver_id: {self.driver_id}, car_id: {self.car_id}, is_staff: {self.is_staff}')


class Park(Base):
    __tablename__ = 'parks'
    id: Mapped[int] = mapped_column(primary_key=True)
    park_id: Mapped[str]
    api_key: Mapped[str]
    client: Mapped[str]
    session_id: Mapped[str]
    name: Mapped[str]
    user: Mapped['User'] = relationship(back_populates='park', uselist=True)

    def __repr__(self):
        return f'park_id: {self.park_id} api_key: {self.api_key}, name: {self.name}'
