import logging
import os
import requests
import telegram
import time

from requests.exceptions import ConnectionError

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def main():
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': 'Token {}'.format(os.getenv('DEVMAN_TOKEN'))
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    while True:
        try:
            long_polling_url = 'https://dvmn.org/api/long_polling/'
            requests.get(long_polling_url, headers=headers)

            results = response.json().get('results', [])
            last_record = results[0]
            if last_record.get('is_negative'):
                text = "У вас проверили работу '{}'.\n\n К сожалению, в работе нашлись ошибки.\n\n Ссылка на урок - {}"\
                    .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
            else:
                text = "У вас проверили работу '{}'.\n\n Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n Ссылка на урок - {}"\
                    .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
            bot.send_message(chat_id=os.getenv('TG_CHAT_ID'), text=text)
        except ConnectionError as error:
            return 'Exception description - {}'.format(error)
        time.sleep(60)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
    main()


