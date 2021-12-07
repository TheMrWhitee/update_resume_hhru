import os
import time

import requests
import telebot
from dotenv import load_dotenv
from schedule import every, repeat, run_pending

load_dotenv()

ACCESS_TOKEN = os.getenv('HHRU_TOKEN')
RESUME_ID = os.getenv('RESUME_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
url = f'https://api.hh.ru/resumes/{RESUME_ID}/publish/'
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


@repeat(every(4).hours)
def update_resume():
    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        return send_message('Резюме успешно обновлено!')
    error_code = response.status_code
    error_value = response.json()['errors'][0]['value']
    error = f'Ошибка {error_code}: {error_value}'
    return send_message(error)


while True:
    run_pending()
    time.sleep(1)
