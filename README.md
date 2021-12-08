# update_resume_hhru
Скрипт автоматически поднимает резюме на hh.ru и уведомляет об этом в ваш телеграм.  
***
## Использование
#### Склонируйте репозиторий и перейдите в него:
    cd update_resume_hhru
#### Создайте виртуальное окружение, активируйте его и установите зависимости:
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
#### Создайте файил *.env* и добавьте в него свои значения:
    HHRU_TOKEN = Ваш токен, для доступа к API hh.ru
    RESUME_ID = ID вашего резюме (из адресной строки страницы с резюме)
    TELEGRAM_TOKEN = Токен вашего телеграм-бота
    CHAT_ID = ID вашего телеграм аккаунта
Как получить токен для API можно почитать [здесь](https://github.com/hhru/api/blob/master/docs/authorization_for_user.md).  
***
#### Теперь нужно запускать скрипт каждые 4 часа, для этого добавьте таск в cron:  
Открываем cron на редактирование:

    crontab -e
И добавляем в конец строку:

    0 */4 * * * update_resume_hhru/venv/bin/python update_resume_hhru/hhru.py

Готово!