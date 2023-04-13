# update_resume_hhru
Скрипт автоматически поднимает резюме на hh.ru и уведомляет об этом в ваш телеграм.  
***
## Использование
#### Клонируйте репозиторий и перейдите в него:
    cd update_resume_hhru
#### Создайте виртуальное окружение, активируйте его и установите зависимости:
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
#### Создайте файл *.env* и добавьте в него свои значения:
    ACCESS_TOKEN = Ваш токен, для доступа к API hh.ru
    REFRESH_TOKEN = Токен для обновления access токена
    RESUME_ID = ID вашего резюме (из адресной строки страницы с резюме)
    TELEGRAM_TOKEN = Токен вашего телеграм-бота
    CHAT_ID = ID вашего телеграм аккаунта
Как получить токен для API можно почитать [здесь](https://github.com/hhru/api/blob/master/docs/authorization_for_user.md).  
Краткая инструкция:
 - отправляем запрос к hh.ru, чтобы получить authorization_code. В браузере переходим по ссылке 
`https://hh.ru/oauth/authorize?response_type=code&client_id=<ваш client_id из личного кабинета разработчика>`
после успешной авторизации будет редирект, нужное значение лежит 
в параметре `code` - смотрим в адресной строке
 - далее запрос для получения токенов
`curl -X POST https://hh.ru/oauth/token -F grant_type=authorization_code -F client_id=<ваш client_id из личного кабинета разработчика> -F client_secret=<ваш client_secret из личного кабинета разработчика> -F code=<authorization_code полученный на предыдущем шаге>`
в ответ придёт JSON, в котором будут `access_token` и `refresh_token`
***
#### Теперь нужно запускать скрипт по расписанию, для этого используем cron:  
Открываем cron на редактирование:

    crontab -e
И добавляем в конец строки:

    0 9 * * * update_resume_hhru/venv/bin/python update_resume_hhru/hhru.py
    1 13 * * * update_resume_hhru/venv/bin/python update_resume_hhru/hhru.py
    2 17 * * * update_resume_hhru/venv/bin/python update_resume_hhru/hhru.py
    3 21 * * * update_resume_hhru/venv/bin/python update_resume_hhru/hhru.py

Готово!  
P.S. 4 таски с разницей в минуту используем потому что выполнение запроса занимает какое-то время (несколько мс),
и если следующий запрос к API hh.ru придёт хотя бы на 1мс раньше, то не будет успешно выполнен, т.к. 
обновлять резюме можно только ровно через 4 часа и ни милисекундой раньше. Далее эта разница
может накладываться и увеличиваться, т.о. резюме никогда не будет обновлено.

Access token действителен 2 недели и обновить его раньше нельзя.  
По истечении этого срока и получения ошибки, access token будет автоматически  
обновлён с помощью refresh token, и скрипт продолжит работу.  
Так же будет обновлён и refresh token, т.к. его можно использовать только один раз.  
О всех событиях придёт сообщение в телеграм.