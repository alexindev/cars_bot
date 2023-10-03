import requests
from datetime import datetime, timedelta
from utils.config import headers, cookies
from logs.config import logger
from utils.helpers import get_last_monday_sunday


class Data:
    @staticmethod
    def get_leaders(park_id: str, session_id: str) -> list | None:
        """
        Таблица лидеров

        :param session_id: Сессия парка
        :param park_id: идентификатор парка
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
                headers=headers(park_id=park_id),
                cookies=cookies(session_id=session_id),
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

    @staticmethod
    def get_driver_data(phone: str, session_id: str, park_id: str) -> tuple | None:
        """
        Получить driver_id, car_id, full_name

        :param session_id: Сессия парка
        :param park_id: идентификатор парка
        :param phone:str:  Номер телефона
        :return: Идентификатор водителя, машины, полное имя
        """
        page = 1
        while True:
            try:
                response = requests.post(
                    url='https://fleet.yandex.ru/api/v1/drivers/list',
                    headers=headers(park_id=park_id),
                    cookies=cookies(session_id=session_id),
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

    @staticmethod
    def get_status(driver_id: str, interval: str, park_id: str, session_id: str) -> dict | None:
        """
        Статистика заказов для водителя

        :param session_id: Сессия парка
        :param park_id: идентификатор парка
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
                headers=headers(park_id=park_id),
                cookies=cookies(session_id=session_id),
                json=data
            ).json()
            return response
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get_canceled_trip(driver_id: str, date_from: str, date_to: str, park_id: str, session_id: str) -> list:
        """
        Получить статистику по самолетам и отмены

        :param session_id: Сессия парка
        :param park_id: идентификатор парка
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
                    headers=headers(park_id=park_id),
                    cookies=cookies(session_id=session_id),
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

    def get_quality(self, driver_id: str, park_id: str, session_id: str) -> dict | None:
        """
        Получить информацию по качеству

        :param session_id: Сессия парка
        :param park_id: Идентификатор парка
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
                    headers=headers(park_id=park_id),
                    cookies=cookies(session_id=session_id),
                    json=data
                ).json()
                if not response.get('report'):
                    if lap == 2:
                        return
                    page = 1
                    lap += 1
                    last = False
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

    @staticmethod
    def get_current_state(car_id: str, park_id: str, session_id: str) -> dict | None:
        """
        Получить текущее состояние водителя

        :param session_id: Сессия парка
        :param park_id: Идентификатор парка
        :param car_id: Идентификатор автомобиля
        :return: Словарь с информацией о тарифах и услугах
        """
        state_data = {}
        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cards/car/details',
                headers=headers(park_id=park_id),
                cookies=cookies(session_id=session_id),
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

    @staticmethod
    def update_category(car_id: str, state: dict, park_id: str, session_id: str) -> bool:
        """
        Менеджер услуг

        :param session_id: Сессия парка
        :param park_id: Идентификатор парка
        :param car_id: Идентификатор автомобиля
        :param state: Актуальное состояние
        :return: True в случае успешной операции
        """
        try:
            response = requests.post(
                url='https://fleet.yandex.ru/api/v1/cars/update',
                params={'carId': car_id},
                headers=headers(park_id=park_id),
                cookies=cookies(session_id=session_id),
                json=state
            )
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logger.exception(e)

    def set_payment(self, driver_id: str, limit: str, park_id: str, client: str, api_key: str) -> bool:
        """
        Установить лимит водителя

        :param api_key: API Key
        :param client: Clien Key
        :param park_id: Идентификатор парка
        :param limit: '300' - наличный расчет, '150000' - безналичный расчет
        :param driver_id: Идентификатор водителя
        :return:
        """
        data = self.get_driver_profile_data(driver_id,  park_id, client, api_key)
        if not data:
            return False

        data['account']['balance_limit'] = limit
        try:
            response = requests.put(
                url='https://fleet-api.taxi.yandex.net/v2/parks/contractors/driver-profile',
                headers={
                    'X-Client-ID': client,
                    'X-Api-Key': api_key,
                    'X-Park-ID': park_id
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
    def get_driver_profile_data(driver_id: str,  park_id: str, client: str, api_key: str) -> dict:
        """
        Получить информацию о водителе

        :param api_key: API Key
        :param client: Clien Key
        :param park_id: Идентификатор парка
        :param driver_id: Идентификатор водителя
        :return: Словарь с параметрами для обновления данных
        """
        try:
            response = requests.get(
                url=f'https://fleet-api.taxi.yandex.net/v2/parks/contractors/driver-profile',
                headers={
                    'X-Client-ID': client,
                    'X-Api-Key': api_key,
                    'X-Park-ID': park_id
                },
                params={
                    'contractor_profile_id': driver_id
                }
            ).json()
            return response
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get_current_order_status(driver_id: str, park_id: str, session_id: str) -> dict:
        """
        Получить текущее состояние заказа

        :param session_id: Сессия парка
        :param park_id: Идентификатор парка
        :param driver_id: Идентификатор водителя
        :return: Словарь с текущим состоянием заказа
        """
        try:
            response = requests.get(
                url='https://fleet.yandex.ru/api/fleet/map/v1/drivers/item',
                headers=headers(park_id=park_id),
                cookies=cookies(session_id=session_id),
                params={'driver_id': driver_id}
            ).json()
            return response
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get_unpaid_orders(driver_id: str, park_id: str, session_id: str) -> list | None:
        """
        Получить неоплаченые заказы

        :param session_id: Сессия парка
        :param park_id: Идентификатор парка
        :param driver_id: Идентификатор водителя
        :return:
        """
        today = datetime.today()
        date_from = today - timedelta(weeks=1)

        data = {
            "date_type": "booked_at",
            "order_statuses": ["complete"],
            "order_payments": ["cashless"],
            "driver_id": driver_id,
            "date_from": f"{date_from}T00:00:00.000+03:00",
            "date_to": f"{datetime.today().strftime('%Y-%m-%d')}T23:59:00.000+03:00"
        }

        result = []
        while True:
            try:
                response = requests.post(
                    url='https://fleet.yandex.ru/api/reports-api/v1/orders/list',
                    headers=headers(park_id=park_id),
                    cookies=cookies(session_id=session_id),
                    json=data
                ).json()

                try:
                    response['orders']
                except Exception as e:
                    logger.exception(e)
                    return []

                data['cursor'] = response.get('cursor')

                for i in response['orders']:
                    price = int(i.get('price', 0))
                    price_card = int(i.get('price_card', 0))
                    price_corporate = int(i.get('price_corporate', 0))
                    price_promotion = int(i.get('price_promotion', 0))

                    full_price = price_card + price_corporate + price_promotion
                    if full_price != price:
                        date = i.get('ended_at').split('.')[0].replace('T', ' ')
                        order_id = i.get('short_id')
                        address_from = i.get('address_from')
                        address_to = i.get('address_to')
                        category = i.get('category')

                        result.append(
                            {
                                'order_id': order_id,
                                'price': price,
                                'date': date,
                                'address_from': address_from,
                                'address_to': address_to,
                                'category': category
                            }
                        )
                if len(response.get('orders')) < 40:
                    return result
            except Exception as e:
                logger.exception(e)
                return

    # def smz(self):
    #     response = requests.get(
    #         url='https://fleet-api.taxi.yandex.net/v1/parks/driver-work-rules?park_id=21d56564727d43a986318d1df5188df1',
    #         headers={
    #             'X-Client-ID': os.getenv('X_CLIENT_ID'),
    #             'X-Api-Key': os.getenv('X_API_KEY'),
    #             'X-Park-ID': os.getenv('PARK_ID')
    #         },
    #         # cookies=self.cookies
    #     ).json()
    #     print(response)
