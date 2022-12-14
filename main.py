import logging
import os
import requests
import telegram
import time

from logger import TelegramLogsHandler

from requests.exceptions import ConnectionError, ReadTimeout

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))

    logger.addHandler(TelegramLogsHandler(bot, os.getenv('TG_CHAT_ID')))
    logger.info('Бот запущен!')

    timestamp_to_request = time.time()

    while True:
        try:
            url = 'https://dvmn.org/api/long_polling/'
            headers = {
                'Authorization': 'Token {}'.format(os.getenv('DEVMAN_TOKEN'))
            }
            response = requests.get(url, headers=headers, params={'timestamp': timestamp_to_request})
            response.raise_for_status()
            reviews_update = response.json()

            if reviews_update.get('status') == 'timeout':
                timestamp_to_request = reviews_update.get('timestamp_to_request', '')
            if reviews_update.get('status') == 'found':
                timestamp_to_request = reviews_update.get('last_attempt_timestamp', '')

            if new_attempts := reviews_update.get('new_attempts'):
                last_record = new_attempts[0]
                if last_record.get('is_negative'):
                    text = f"""\
                    У вас проверили работу '{last_record.get('lesson_title')}'.
                    К сожалению, в работе нашлись ошибки.
                    Ссылка на урок - {last_record.get('lesson_url')}"
                    """
                else:
                    text = f"""\
                    У вас проверили работу '{last_record.get('lesson_title')}'.
                    Преподавателю всё понравилось, можно приступать к следующему уроку!
                    Ссылка на урок - {last_record.get('lesson_url')}"
                    """
                bot.send_message(chat_id=os.getenv('TG_CHAT_ID'), text=text)
                logger.debug('Сообщение отправлено в чат!')
        except ConnectionError as error:
            time.sleep(60)
            logger.error('Exception description - {}'.format(error))
        except ReadTimeout as error:
            logger.error('Exception description - {}'.format(error))


if __name__ == '__main__':
    main()


