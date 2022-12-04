# Телеграм бот - job_bot.

## Описание функционала
Бот позволяет узнать статус о проверенных задачах.


## Настройка и запуск
Для успешного запуска необходимо указать переменные окружения в файле `.env` в корне проекта.\
Вам понадобится указать три переменные: **DEVMAN_TOKEN**, **TG_CHAT_ID** и **TELEGRAM_TOKEN**.\
**DEVMAN_TOKEN** - это ваш персональный токен.\
**TG_CHAT_ID** - id пользователя, которому надо отправить сообщение.\
**TELEGRAM_TOKEN** - токен бота, который вы получили от **GodfatherBot**.\
Более подробно о том, как настраиваются и извлекаются переменные окружения, можно прочитать [здесь](https://pypi.org/project/environs/) или [здесь](https://docs.djangoproject.com/en/4.1/ref/settings/).

## Как запустить проект локально?
```
git clone <SSH address of this repo>
cd check_bot/
python3 -m myenv venv
source venv\bin\activate
pip install -r requirements.txt
python3 main.py
```
После запуска бота в ответ получите примерно такое сообщение:

<img width="387" alt="Screenshot 2022-12-03 at 08 58 12" src="https://user-images.githubusercontent.com/29278979/205431011-93d32846-0f82-485e-b013-f0ed59c5145f.png">
