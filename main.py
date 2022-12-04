import logging
import os
import requests
import telegram
import time

from requests.exceptions import ConnectionError, ReadTimeout

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))

    timestamp_to_request = time.time()

    while True:
        try:
            url = 'https://dvmn.org/api/long_polling/'
            headers = {
                'Authorization': 'Token {}'.format(os.getenv('DEVMAN_TOKEN'))
            }
            response = requests.get(url, headers=headers, params={'timestamp': timestamp_to_request})
            response.raise_for_status()
            response = response.json()

            if response.get('status') == 'timeout':
                timestamp_to_request = response.get('timestamp_to_request', '')
            if response.get('status') == 'found':
                timestamp_to_request = response.get('last_attempt_timestamp', '')

            if response.get('new_attempts'):
                new_attempts = response.get('new_attempts', [])
                last_record = new_attempts[0]
                if last_record.get('is_negative'):
                    text = "У вас проверили работу '{}'.\n\n К сожалению, в работе нашлись ошибки.\n\n Ссылка на урок - {}"\
                        .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
                else:
                    text = "У вас проверили работу '{}'.\n\n Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n Ссылка на урок - {}"\
                        .format(last_record.get('lesson_title'), last_record.get('lesson_url'))
                bot.send_message(chat_id=os.getenv('TG_CHAT_ID'), text=text)
        except ConnectionError as error:
            time.sleep(60)
            print('Exception description - {}'.format(error))
        except ReadTimeout as error:
            print('Exception description - {}'.format(error))


if __name__ == '__main__':
    main()


