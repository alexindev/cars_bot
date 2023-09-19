from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[str]
    user_id: Mapped[str | None]

    def __repr__(self):
        return f'chat_id: {self.chat_id}, phone: {self.phone}, user_id: {self.user_id}'

