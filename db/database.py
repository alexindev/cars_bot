from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db.models import Base, User

import os


class Database:
    """ Работа с базой данных """
    def __init__(self):
        self.engine = create_engine(os.getenv('SQLALCHEMY_ENGINE'), echo=True)
        Base.metadata.create_all(bind=self.engine)

    def register_user(self, chat_id: int, phone: str, driver_id: str) -> bool:
        """
        Добавить пользователя

        :param chat_id: ChatID телеграм
        :param phone: Номер телефона
        :param driver_id: Идентификатор водителя
        :return: True при успешном добавлении, False если пользователь не найден
        """
        user = self.get_user(phone)

        if user:
            # Пользователь существует
            return False
        else:
            with Session(self.engine) as session:
                session.add(User(chat_id=chat_id, phone=phone, driver_id=driver_id))
                session.commit()
                return True

    def get_user(self, phone: str) -> dict | None:
        """
        Получить пользователя

        :param phone: Телефон
        :return: Словарь с данными пользователя или None
        """
        with Session(self.engine) as session:
            stmt = select(User).where(User.phone == phone)
            result = session.execute(stmt).fetchone()
            if result:
                user = result[0]
                return {
                    'chat_id': user.chat_id,
                    'phone': user.phone,
                    'driver_id': user.driver_id,
                }
