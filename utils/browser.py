import os
import pickle
from playwright.async_api import async_playwright, Page
from playwright._impl import _api_types

from logs.config import logger


async def driver(driver_id: str, action: str, category: str) -> bool:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        # Загрузка куки
        with open('utils/cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
        await context.add_cookies(cookies)

        profile_url = f'https://fleet.yandex.ru/drivers/{driver_id}/car?park_id={os.getenv("PARK_ID")}'
        page = await context.new_page()
        await page.goto(url=profile_url)

        try:
            await page.wait_for_selector('//form/div[2]/div/div/div[2]', timeout=10_000)
        except _api_types.TimeoutError:
            logger.error('Элемент с креслами не найден')
            return False

        result = None
        if action == 'delete':
            if await delete_seat(page, category):
                result = True
        else:
            if await create_seat(page, category):
                result = True

        await context.close()
        await browser.close()
        return True if result else False


async def delete_seat(page: Page, category: str) -> bool:
    """
    Удалить детское кресло

    :param page: Объект контекста playwright
    :param category: Номер удаляемой категории
    :return: True в случае успеха
    """
    try:
        seats = await page.query_selector_all('//form/div[2]/div/div/div[2]/div')
        for i in seats:
            get_category = await i.query_selector('//div[2]/div[1]/span[1]')
            category_text = await get_category.text_content()
            delete_button = await i.query_selector('button[aria-label="Удалить"]')
            confirm_button = page.locator('button:has-text("Удалить")')

            if category_text == category:
                await delete_button.click()
                await confirm_button.click()
                return True
            else:
                logger.error('Не найдена категория кресла для удаления')
    except Exception as e:
        logger.error(e)


async def create_seat(page: Page, category: str) -> bool:
    """
    Добавить новое кресло

    :param page: Объект контекста playwright
    :param category: Номер категории
    :return: True в случае успеха
    """
    if category == '0':
        category = "'Люлька • От 0 до 9 месяцев • Категория 0'"
    elif category == '1':
        category = "'Кресло • от 9 месяцев до 3 лет • Категория 1'"
    elif category == '2':
        category = "'Кресло • от 3 до 7 лет • Категория 2'"
    else:
        category = "'Бустер • от 7 до 12 лет • Категория 3'"

    try:
        elem = await page.wait_for_selector('button:has-text("Добавить детское кресло")', timeout=5_000)
        await elem.click()

        seat = page.locator(f"span:text({category})")
        await seat.click()

        confirm = page.locator('button:has-text("Добавить"):not(:has-text("детское кресло"))')
        await confirm.click()
        return True
    except _api_types.TimeoutError:
        logger.error('Элемент не найден')
    except Exception as e:
        logger.error(e)
