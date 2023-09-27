import os

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
        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/reports-api/v2/summary/drivers/list',
                headers=self.headers,
                cookies=self.cookies,
                json=data
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
            logger.exception(e)
            return None

    def get_driver_data(self, phone: str) -> tuple | None:
        """
        Получить driver_id, car_id, full_name

        :param phone:str:  Номер телефона
        :return: Идентификатор водителя, машины, полное имя
        """
        page = 1
        while True:
            try:
                response = requests.post(
                    url='https://fleet.yandex.ru/api/v1/drivers/list',
                    headers=self.headers,
                    cookies=self.cookies,
                    json={
                        "page": page,
                        "limit": 100
                    }

                ).json()
                for i in response['driver_profiles']:
                    driver_id = i['driver_profile'].get('id')
                    car_id = i.get('car', {}).get('id')
                    driver_phone = i['driver_profile'].get('phones')[0]
                    first_name = i['driver_profile'].get('first_name')
                    last_name = i['driver_profile'].get('last_name')
                    if phone == driver_phone:
                        full_name = f'{first_name} {last_name}'
                        return driver_id, car_id, full_name

                if len(response['driver_profiles']) < 100:
                    logger.info('Нет совпадений по номеру телефона')
                    return None
                page += 1
            except Exception as e:
                logger.exception(e)
                return None

    def get_status(self, driver_id: str, interval: str) -> dict | None:
        """
        Статистика заказов для водителя

        :param driver_id: Идентификатор водителя
        :param interval: Интервал
        :return: Словарь со статистикой водителя
        """

        data = {
            "driver_id": driver_id,
            "date_from": datetime.now().strftime(f'%Y-%m-{interval}T00:00:00.000+03:00'),
            "date_to": datetime.now().strftime('%Y-%m-%dT23:59:59.000+03:00')
        }

        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cards/driver/income',
                headers=self.headers,
                cookies=self.cookies,
                json=data

            ).json()
            return response

        except Exception as e:
            logger.exception(e)

    def get_canceled_trip(self, driver_id: str, date_from: str, date_to: str) -> list:
        """
        Получить статистику по самолетам и отмены

        :param date_from: Начало периода
        :param date_to: Конец периода
        :param driver_id: Идентификатор водителя
        :return:
        """
        try:
            data = {
                "driver_id": driver_id,
                "date_type": "booked_at",
                "date_from": f"{date_from}T00:00:00.000+03:00",
                "date_to": f"{date_to}T23:59:00.000+03:00",
            }
            result = []
            while True:
                response = requests.post(
                    url='https://fleet.yandex.ru/api/reports-api/v1/orders/list',
                    headers=self.headers,
                    cookies=self.cookies,
                    json=data
                ).json()

                if not response.get('orders'):
                    return []

                data['cursor'] = response.get('cursor')

                for i in response['orders']:
                    if i.get('status') == 'cancelled':
                        result.append(i.get('cancellation_description'))
                if len(response.get('orders')) < 40:
                    return result

        except Exception as e:
            logger.exception(e)

    def get_quality(self, driver_id: str) -> dict | None:
        """
        Получить информацию по качеству

        :param driver_id: Идентификатор водителя
        :return: Словарь с показателями качества водителя
        """
        monday_1, sunday_1, monday_2, sunday_2 = get_last_monday_sunday()
        page = 1
        last = True
        date_from = monday_1
        date_to = sunday_1
        lap = 1
        while True:
            data = self.data_for_get_quality(date_from, date_to, page=page)
            try:
                if not last:
                    date_from = monday_2
                    date_to = sunday_2
                    data = self.data_for_get_quality(date_from, date_to, page=page)

                response = requests.post(
                    url='https://fleet.yandex.ru/api/reports-api/v1/quality/list',
                    headers=self.headers,
                    cookies=self.cookies,
                    json=data
                ).json()
                if not response.get('report'):
                    if lap == 2:
                        return
                    page = 1
                    lap += 1
                    last = False
                    logger.info('Данные для отчета за прошлую неделю еще не сформированы')
                    continue

                report_data = {}
                page += 1

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
                        report_data['date_from'] = date_from
                        report_data['date_to'] = date_to
                        return report_data
                    if not response.get('report'):
                        logger.info('Данные для определения качества не найдены')
            except Exception as e:
                logger.exception(e)
                return

    @staticmethod
    def data_for_get_quality(date_from: str, date_to: str, page: int) -> dict:
        data = {
            "period":
                {
                    "from": f"{date_from} 00:00",
                    "to": f"{date_to} 23:59"
                },
            "limit": 100,
            "page": page
        }
        return data

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
                json={"car_id": f"{car_id}"}
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
            if 'chairs' in response['car']:
                state_data['chairs'] = response['car'].get('chairs')
            return state_data
        except Exception as e:
            logger.exception(e)

    def update_category(self, car_id: str, state: dict) -> bool:
        """
        Менеджер услуг

        :param car_id: Идентификатор автомобиля
        :param state: Актуальное состояние
        :return: True в случае успешной операции
        """
        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cars/update',
                params={'carId': car_id},
                headers=self.headers,
                cookies=self.cookies,
                json=state
            )
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logger.exception(e)

    def set_payment(self, driver_id: str, limit: str) -> bool:
        """
        Установить лимит водителя

        :param limit: '0' - наличный расчет, '150000' - безналичный расчет
        :param driver_id: Идентификатор водителя
        :return:
        """
        data = self.get_driver_profile_data(driver_id)
        if not data:
            return False

        data['account']['balance_limit'] = limit
        try:
            response = requests.put(
                url='https://fleet-api.taxi.yandex.net/v2/parks/contractors/driver-profile',
                headers={
                    'X-Client-ID': os.getenv('X_CLIENT_ID'),
                    'X-Api-Key': os.getenv('X_API_KEY'),
                    'X-Park-ID': os.getenv('PARK_ID')
                },
                json=data,
                params={
                    'contractor_profile_id': driver_id
                }
            )
            if response.status_code == 200:
                return True
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get_driver_profile_data(driver_id: str) -> dict:
        """
        Получить информацию о водителе

        :param driver_id: Идентификатор водителя
        :return: Словарь с параметрами для обновления данных
        """
        try:
            response = requests.get(
                url=f'https://fleet-api.taxi.yandex.net/v2/parks/contractors/driver-profile',
                headers={
                    'X-Client-ID': os.getenv('X_CLIENT_ID'),
                    'X-Api-Key': os.getenv('X_API_KEY'),
                    'X-Park-ID': os.getenv('PARK_ID')
                },
                params={
                    'contractor_profile_id': driver_id
                }
            ).json()
            return response
        except Exception as e:
            logger.exception(e)

    def get_current_order_status(self, driver_id: str) -> dict:
        """
        Получить текщее состояние заказа

        :param driver_id: Идентификатор водителя
        :return: Словарь с текущим состоянием заказа
        """
        try:
            response = requests.get(
                url='https://fleet.yandex.ru/api/fleet/map/v1/drivers/item',
                headers=self.headers,
                cookies=self.cookies,
                params={'driver_id': driver_id}
            ).json()
            return response
        except Exception as e:
            logger.exception(e)

