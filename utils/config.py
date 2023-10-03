
def cookies(session_id: str):
    return {
        'Session_id': session_id,
    }


def headers(park_id: str):
    return {
        'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
        'X-Park-Id': park_id,
    }
