import requests
from bs4 import BeautifulSoup
from config import *
from logger import logger


def login_and_get_users_rows():
    session = requests.Session()

    logger.info('Получаем токен входа.')
    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token_input = soup.find('input', {'name': 'token'})
    if not token_input:
        logger.error('Не удалось найти токен входа.')
        raise ValueError('Token not found.')

    token = token_input['value']
    logger.debug(f'Токен получен: {token}')

    login_data = {
        'pma_username': USERNAME,
        'pma_password': PASSWORD,
        'server': 1,
        'target': 'index.php',
        'token': token
    }

    logger.info('Выполняем авторизацию.')
    login_response = session.post(LOGIN_URL, data=login_data)
    if 'phpMyAdmin' not in login_response.text:
        logger.error('Ошибка авторизации.')
        raise PermissionError('Login failed.')

    logger.info(f'Успешная авторизация {login_data["pma_username"]}.')

    browse_url = f'{BASE_URL}/index.php?route=/sql&db={DB_NAME}&table={TABLE_NAME}&pos=0'
    logger.info(f'Получаем данные таблицы `{TABLE_NAME}`.')
    browse_page = session.get(browse_url)
    soup = BeautifulSoup(browse_page.text, 'html.parser')
    rows = soup.select('tbody tr')
    logger.debug(f'Найдено строк: {len(rows)}')

    return rows


def print_table():
    try:
        rows = login_and_get_users_rows()
        if not rows:
            logger.warning('Таблица пуста или не найдена.')
        else:
            print(f'\n📋 Данные из таблицы `{TABLE_NAME}`:\n')
            for row in rows:
                cols = [col.get_text(strip=True) for col in row.select('td')]
                print(' | '.join(cols))
    except Exception as e:
        logger.exception(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print_table()
