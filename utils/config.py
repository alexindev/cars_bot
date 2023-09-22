from dotenv import load_dotenv

import os


load_dotenv()

cookies = {
    'Session_id': os.getenv('SESSION_ID'),
}

headers = {
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
    'X-Park-Id': os.getenv('PARK_ID'),
}
