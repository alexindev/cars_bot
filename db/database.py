from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db.models import Base, User

import os


class Database:
    """ Работа с базой данных """
    def __init__(self):
        self.engine = create_engine(os.getenv('SQLALCHEMY_ENGINE'), echo=True)
        Base.metadata.create_all(bind=self.engine)

    def register_user(self, chat_id: int, phone: str, driver_id: str, car_id: str) -> bool:
        """
        Добавить пользователя

        :param chat_id: ChatID телеграм
        :param phone: Номер телефона
        :param driver_id: Идентификатор водителя
        :param car_id: Идентификатор автомобиля
        :return: True при успешном добавлении, False если пользователь не найден
        """
        user = self.get_user(phone=phone)

        if user:
            # Пользователь существует
            return False
        else:
            with Session(self.engine) as session:
                session.add(User(chat_id=chat_id, phone=phone, driver_id=driver_id, car_id=car_id))
                session.commit()
                return True

    def get_user(self, chat_id: int = None, phone: str = None) -> dict | None:
        """
        Получить данные пользователя

        :param chat_id: ChatID телеграм
        :param phone: Номер телефона
        :return: Словарь с данными пользователя
        """
        with Session(self.engine) as session:
            if chat_id:
                stmt = select(User).where(User.chat_id == chat_id)
            else:
                stmt = select(User).where(User.phone == phone)
            result = session.execute(stmt).fetchone()
            if result:
                user = result[0]
                return {
                    'chat_id': user.chat_id,
                    'phone': user.phone,
                    'driver_id': user.driver_id,
                    'car_id': user.car_id
                }
