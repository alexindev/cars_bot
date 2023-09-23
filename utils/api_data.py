import requests
from datetime import datetime
from utils.config import headers, cookies
from logs.config import logger
from utils.helpers import get_last_monday_sunday


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
        today = datetime.today()
        date_to = today.strftime('%Y-%m-%d')
        date_from = today.replace(day=1).strftime('%Y-%m-%d')
        data = {
            "date_from": f"{date_from}",
            "date_to": f"{date_to}",
            "sort": {
                "field": "count_orders_completed",
                "direction": "desc"
            }
        }
        return str(data).replace("'", '"')

    def get_driver_id_and_car_id(self, phone: str) -> tuple | None:
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
                    car_id = i.get('car', {}).get('id')
                    driver_phone = i['driver_profile'].get('phones')[0]
                    if phone == driver_phone:
                        return driver_id, car_id

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
        Payload для метода get_driver_id_and_car_id

        :param page: int: Номер страницы
        :return: Форматированная строка
        """

        data = {
            "page": page,
            "limit": 100
        }
        return str(data).replace("'", '"')

    def get_status(self, driver_id: str, interval: str) -> dict | None:
        """
        Статистика заказов для водителя

        :param driver_id: Идентификатор водителя
        :param interval: Интервал
        :return: Словарь со статистикой водителя
        """

        data = self.data_for_get_status(driver_id, interval)

        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cards/driver/income',
                headers=self.headers,
                cookies=self.cookies,
                data=data

            ).json()
            return response

        except Exception as e:
            logger.error(e)

    @staticmethod
    def data_for_get_status(driver_id: str, interval: str) -> str:
        data = {
            "driver_id": driver_id,
            "date_from": datetime.now().strftime(f'%Y-%m-{interval}T00:00:00.000+03:00'),
            "date_to": datetime.now().strftime('%Y-%m-%dT23:59:59.000+03:00')
        }
        return str(data).replace("'", '"')

    def get_quality(self, driver_id: str) -> dict | None:
        """
        Получить информацию по качеству

        :param driver_id: Идентивикатор водителя
        :return: Словарь с показателями качества водителя
        """
        date_from, date_to = get_last_monday_sunday()

        page = 1
        while True:
            data = self.data_for_get_quality(date_from, date_to, page)
            page += 1
            try:
                response = requests.post(
                    url='https://fleet.yandex.ru/api/reports-api/v1/quality/list',
                    headers=self.headers,
                    cookies=self.cookies,
                    data=data
                ).json()
                report_data = {}
                for i in response['report']:
                    current_driver_id = i['driver'].get('id')
                    if driver_id == current_driver_id:
                        report_data['orders'] = i.get('orders')
                        report_data['trips'] = i.get('trips')
                        report_data['perfect_trips'] = i.get('perfect_trips')
                        report_data['cancel_orders'] = i.get('cancel_orders')
                        report_data['our_observation'] = i.get('our_observation')
                        report_data['main_complaints'] = i.get('main_complaints')
                        report_data['bad_rated_trips'] = i.get('bad_rated_trips')
                        report_data['rating_start'] = i.get('rating_start')
                        report_data['rating_end'] = i.get('rating_end')
                        return report_data
                    if len(response['report']) < 100:
                        logger.info('Данные для определения качества не найдены')
                        return None
            except Exception as e:
                logger.error(e)
                return None

    @staticmethod
    def data_for_get_quality(date_from: str, date_to: str, page: int) -> str:
        data = {
            "period":
                {
                    "from": f"{date_from} 00:00",
                    "to": f"{date_to} 23:59"
                },
            "limit": 100,
            "page": page
        }
        return str(data).replace("'", '"')

    def get_current_state(self, car_id: str) -> dict | None:
        """
        Получить текущее состояние водителя

        :param car_id: Идентификатор автомобиля
        :return: Словарь с информацией о тарифах и услугах
        """
        state_data = {}
        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cards/car/details',
                headers=self.headers,
                cookies=self.cookies,
                data=self.data_for_current_state(car_id)
            ).json()
            state_data['brand'] = response['car'].get('brand')
            state_data['model'] = response['car'].get('model')
            state_data['color'] = response['car'].get('color')
            state_data['color'] = response['car'].get('color')
            state_data['year'] = response['car'].get('year')
            state_data['number'] = response['car'].get('number')
            state_data['callsign'] = response['car'].get('callsign')
            state_data['vin'] = response['car'].get('vin')
            state_data['booster_count'] = response['car'].get('booster_count')
            state_data['registration_cert'] = response['car'].get('registration_cert')
            state_data['status'] = response['car'].get('status')
            state_data['transmission'] = response['car'].get('transmission')
            state_data['categories'] = response['car'].get('categories')
            state_data['amenities'] = response['car'].get('amenities')
            state_data['tariffs'] = response['car'].get('tariffs')
            state_data['mileage'] = response['car'].get('mileage')
            return state_data
        except Exception as e:
            logger.error(e)

    @staticmethod
    def data_for_current_state(car_id: str):
        data = {
            "car_id": f"{car_id}"
        }
        return str(data).replace("'", '"')
