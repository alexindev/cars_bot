from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db.models import Base, User

import os


class Database:
    """ Работа с базой данных """
    def __init__(self):
        self.engine = create_engine(os.getenv('SQLALCHEMY_ENGINE'), echo=True)
        Base.metadata.create_all(bind=self.engine)

    def register_user(self, chat_id: int, phone: str) -> bool:
        """ Добавить пользователя """
        user = self.get_user(chat_id)

        if user:
            # Пользователь существует
            return False
        else:
            with Session(self.engine) as session:
                session.add(User(chat_id=chat_id, phone=phone))
                session.commit()
                return True

    def get_user(self, chat_id: int) -> None | tuple:
        """ Пполучить пользователя """
        with Session(self.engine) as session:
            stmt = select(User).where(User.chat_id == chat_id)
            result = session.execute(stmt).fetchone()
            return result
