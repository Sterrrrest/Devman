import time
import requests
import telebot
import logging
import traceback

from textwrap import dedent
from environs import Env


logger = logging.getLogger("Debug")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, tg_chat_id):
        super().__init__()
        self.tg_chat_id = tg_chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


if __name__ == '__main__':

    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    tg_bot = telebot.TeleBot(token=tg_token)

    devman_token = env('DEVMAN_TOKEN')

    logging.basicConfig(level=logging.DEBUG, format="%(process)d %(levelname)s %(message)s %(asctime)s")

    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.setLevel(logging.INFO)
    logger.info('Старт бота')

    url = 'https://dvmn.org/api/user_reviews/'
    url_long = 'https://dvmn.org/api/long_polling/'
    headers = {
        "Authorization": f'Token {devman_token}'
    }

    timestamp = None

    while True:

        try:
            payLoad = {
                'timestamp': timestamp
            }
            response = requests.get(url_long, headers=headers, params=payLoad)
            response.raise_for_status()
            tasks_status = response.json()

            if tasks_status['status'] == 'found':

                if tasks_status['new_attempts'][0]['is_negative']:
                    text_accept = dedent((f'''
                    У вас проверили работу '{tasks_status['new_attempts'][0]['lesson_title']}'
                    В ней есть ошибки
                    Ссылка на работу: {tasks_status['new_attempts'][0]['lesson_url']}'''))

                    tg_bot.send_message(chat_id=tg_chat_id, text=text_accept)
                else:
                    tg_bot.send_message(chat_id=tg_chat_id, text=dedent(f'''
                    У вас проверили работу '{tasks_status['new_attempts'][0]['lesson_title']}'
                    Работа принята!
                    Ссылка на работу: {tasks_status['new_attempts'][0]['lesson_url']}'''))
                timestamp = tasks_status['last_attempt_timestamp']
            else:
                timestamp = tasks_status['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            time.sleep(30)
        except Exception:
            logger.info('Бот упал с ошибкой:')
            logger.info(traceback.format_exc())
            time.sleep(30)

