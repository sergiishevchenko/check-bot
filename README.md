# Телеграм бот - job_bot.

## Описание функционала
Бот позволяет узнать статус о проверенных задачах.


## Настройка и запуск
Для успешного запуска необходимо указать переменные окружения в файле `.env` в корне проекта.
Вам понадобится указать две переменные: **DEVMAN_TOKEN** и **BOT_TOKEN**.
**DEVMAN_TOKEN** - это ваш персональный токен. **BOT_TOKEN** - токен бота, который вы получили от GodfatherBot.
Более подробно о том, как настраиваются и извлекаются переменные окружения, можно прочитать [здесь](https://pypi.org/project/environs/) или [здесь](https://docs.djangoproject.com/en/4.1/ref/settings/).

## Как запустить проект локально?
```
git clone <SSH address of this repo> \n
cd check_bot/
python3 -m myenv venv
source venv\bin\activate
pip install -r requirements.txt
python3 main.py

## Как получить информацию о статусе проверенных задач?
```
Чтобы узнать статус о проверенных задачах, наберите командной строке бота **job_bot** следующую команду:
```
/send_notifications
```
В ответ получите примерно такое сообщение:
![Alt text](https://file%2B.vscode-resource.vscode-cdn.net/var/folders/t9/254vh6ys22370837thlb7tc40000gn/T/TemporaryItems/NSIRD_screencaptureui_9usS8f/Screenshot%202022-12-03%20at%2008.53.58.png?version%3D1670054057525)