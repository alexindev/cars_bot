import os

from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import Session

from db.models import Base, User, Park
from logs.config import logger


class Database:
    """ Работа с базой данных """

    def __init__(self):
        self.engine = create_engine(os.getenv('SQLALCHEMY_ENGINE'))
        Base.metadata.create_all(bind=self.engine)

    def register_user(self, chat_id: int, phone: str, driver_id: str, car_id: str, full_name: str, park_id: int,
                      is_staff: bool = False) -> bool:
        """
        Добавить пользователя

        :param chat_id: ChatID телеграм
        :param phone: Номер телефона
        :param driver_id: Идентификатор водителя
        :param car_id: Идентификатор автомобиля
        :param is_staff: Доступ к админке
        :param full_name: Полное имя водителя
        :return: True при успешном добавлении, False если пользователь не найден
        :param park_id: Идентификатор парка в таблице
        """
        user = self.get_user(phone=phone)

        if user:
            # Пользователь существует
            return False
        else:
            with Session(self.engine) as session:
                session.add(User(
                    chat_id=chat_id, phone=phone, driver_id=driver_id, car_id=car_id, is_staff=is_staff,
                    full_name=full_name, park_id=park_id
                ))
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
                    'car_id': user.car_id,
                    'is_staff': user.is_staff,
                    'full_name': user.full_name,
                    'park_id': user.park.park_id,
                    'session_id': user.park.session_id,
                    'api_key': user.park.api_key,
                    'client': user.park.client,
                    'name': user.park.name
                }

    def get_staff_driver(self):
        """ Получить всех водителей с приоритетом """
        with Session(self.engine) as session:
            stmt = select(User).where(User.is_staff)
            result = session.execute(stmt).fetchall()
            return result

    def update_driver_status(self, phone: str, status: bool) -> bool:
        """ Установить приоритет для водителя """
        with Session(self.engine) as session:
            try:
                stmt = update(User).where(User.phone == phone).values(is_staff=status)
                session.execute(stmt)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.exception(e)

    def get_drivers_count(self):
        """ Получить количество зарегистрированных водителей в боте """
        with Session(self.engine) as session:
            try:
                result = session.query(func.count(User.driver_id)).scalar()
                return result
            except Exception as e:
                logger.exception(e)

    def new_park(self, api_key: str, client: str, park_id: str, session_id: str, name: str):
        """
        Добавить новый парк

        :param api_key: API Key
        :param client: Client Key
        :param park_id: Park ID
        :param session_id: Session_ID
        :param name: Название города
        :return:
        """
        with Session(self.engine) as session:
            try:
                park = session.query(Park).filter_by(api_key=api_key).first()
                if not park:
                    stmt = Park(park_id=park_id, api_key=api_key, client=client, session_id=session_id, name=name)
                    session.add(stmt)
                    session.commit()
            except Exception as e:
                logger.exception(e)
                session.rollback()

    def get_parks(self) -> list:
        """ Получить все парки """
        with Session(self.engine) as session:
            result = session.execute(select(Park)).fetchall()
            data = []
            for park in result:
                park_data = {
                    'id': park[0].id,
                    'park_id': park[0].park_id,
                    'api_key': park[0].api_key,
                    'client': park[0].client,
                    'session_id': park[0].session_id,
                    'name': park[0].name
                }
                data.append(park_data)
            return data

