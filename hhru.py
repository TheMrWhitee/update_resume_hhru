import os

import requests
import telebot
from dotenv import find_dotenv, load_dotenv, set_key

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
RESUME_ID = os.getenv('RESUME_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
body = {'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN}
update_url = f'https://api.hh.ru/resumes/{RESUME_ID}/publish/'
refresh_url = f'https://hh.ru/oauth/token/'
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def update_resume():
    response = requests.post(update_url, headers=headers)
    if response.status_code == 204:
        return send_message('Резюме успешно обновлено!')
    error_code = response.status_code
    error_value = response.json()['errors'][0]['value']
    send_message(f'Ошибка {error_code}: {error_value}')
    if error_value == 'token_expired':
        refresh_token()


def refresh_token():
    response = requests.post(refresh_url, headers=headers, data=body)
    if response.status_code == 200:
        new_access_token = response.json()['access_token']
        new_refresh_token = response.json()['refresh_token']
        write_to_env(new_access_token, new_refresh_token)
        return send_message('Токен успешно обновлён!')
    error_code = response.status_code
    error = response.json()['error']
    error_description = response.json()['error_description']
    return send_message(f'Ошибка {error_code}. {error}: {error_description}')


def write_to_env(at, rt):
    set_key(dotenv_file, 'ACCESS_TOKEN', at)
    set_key(dotenv_file, 'REFRESH_TOKEN', rt)


if __name__ == '__main__':
    update_resume()
