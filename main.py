import requests
import telegram
import logging
import os

from requests.exceptions import ReadTimeout, ConnectionError

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from dotenv import load_dotenv

load_dotenv()

bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def send_notifications(update: Update, context: CallbackContext):
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        "Authorization": "Token {}".format(os.getenv("DEVMAN_TOKEN"))
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    while True:
        try:
            long_polling_url = 'https://dvmn.org/api/long_polling/'
            long_polling_response = requests.get(long_polling_url, headers=headers)
            timestamp_to_request = long_polling_response.json().get('timestamp_to_request', '')
            requests.get(long_polling_url, headers=headers, params={'timestamp': timestamp_to_request})

            results = response.json().get('results', [])
            last_record = results[0]
            if last_record.get('is_negative'):
                text = "У вас проверили работу '{}'.\n\n К сожалению, в работе нашлись ошибки.\n\n Ссылка на урок - {}"\
                    .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
            else:
                text = "У вас проверили работу '{}'.\n\n Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n Ссылка на урок - {}"\
                    .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
            chat_id = input('Введите id пользователя, которому нужно отправить сообщение:') # 486128297
            bot.send_message(chat_id=chat_id, text=text)
        except (ReadTimeout, ConnectionError) as error:
            return 'Exception description - {}'.format(error)


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('get_job_status', send_notifications))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()


