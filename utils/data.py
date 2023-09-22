import requests
from datetime import datetime
from utils.config import headers, cookies
from logs.config import logger


class Data:
    def __init__(self):
        self.headers = headers
        self.cookies = cookies

    def get_leaders(self) -> list | None:
        """
        Таблица лидеров

        :return: Список лидеров list или None если ошибка
        """
        data = self.data_for_liders()

        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/reports-api/v2/summary/drivers/list',
                headers=self.headers,
                cookies=self.cookies,
                data=data
            ).json()

            liders = []

            for i in response['items']:
                orders = i.get('count_orders_completed')
                first_name = i['driver'].get('first_name')
                last_name = i['driver'].get('last_name')
                lider = first_name + ' ' + last_name + ' ' + str(orders)
                liders.append(lider)
            return liders
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def data_for_liders() -> str:
        """
        Payload для get_leaders

        :return: str: Форматированная строка
        """
        date = datetime.today()
        date_to = date.strftime('%Y-%m-%d')
        date_from = date.replace(day=1).strftime('%Y-%m-%d')
        data = {
            "date_from": f"{date_from}",
            "date_to": f"{date_to}",
            "sort": {
                "field": "count_orders_completed",
                "direction": "desc"
            }
        }
        return str(data).replace("'", '"')

    def get_driver_id_by_phone(self, phone: str) -> str | None:
        """
        Получить идентификатор водителя с помощью телефона

        :param phone:str:  Номер телефона
        :return: Идентификатор водителя (str) или None, если не найден
        """

        page = 1
        while True:
            try:
                data = self.data_for_get_user(page)
                response = requests.post(
                    url='https://fleet.yandex.ru/api/v1/drivers/list',
                    headers=self.headers,
                    cookies=self.cookies,
                    data=data

                ).json()

                for i in response['driver_profiles']:
                    driver_id = i['driver_profile'].get('id')
                    driver_phone = i['driver_profile'].get('phones')[0]

                    if phone == driver_phone:
                        return driver_id

                if len(response['driver_profiles']) < 100:
                    logger.error('Нет совпадений по номеру телефона')
                    return None
                page += 1
            except Exception as e:
                logger.error(e)
                return None

    @staticmethod
    def data_for_get_user(page: int) -> str:
        """
        Payload для метода get_driver_id_by_phone

        :param page: int: Номер страницы
        :return: Форматированная строка
        """

        data = {
            "page": page,
            "limit": 100
        }
        return str(data).replace("'", '"')

