import time
import telebot
from environs import Env
import requests

env = Env()
env.read_env()
tg_token = env('TG_TOKEN')
chat_id = env('CLIENT_ID')
devman_token = env('DEVMAN_TOKEN')
url = 'https://dvmn.org/api/user_reviews/'
url_long = 'https://dvmn.org/api/long_polling/'
headers = {
    "Authorization": f'Token {devman_token}'
}

bot = telebot.TeleBot(token=tg_token)

while True:

    try:
        response = requests.get(url_long, headers=headers)
        response.raise_for_status()
        if response.json()['status'] == 'timeout':

            response_timestamp = response.json()['timestamp_to_request']
            payLoad_last_attempt = {
                'timestamp': response_timestamp
            }
            response_last_attempt = requests.get(url_long, headers=headers, params=payLoad_last_attempt)
            response_last_attempt.raise_for_status()
            if response_last_attempt.json()['found']:
                if response.json()['new_attempts'][0]['is_negative']:
                    bot.send_message(chat_id=chat_id, text=f"У вас проверили работу "
                                                           f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                                           f"В ней есть ошибки\n\n"
                                                           f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")
                else:
                    bot.send_message(chat_id=chat_id, text=f"У вас проверили работу "
                                                           f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                                           f"Работа принята!\n\n"
                                                           f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")
        else:
            if response.json()['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=chat_id, text=f"У вас проверили работу "
                                                       f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                                       f"В ней есть ошибки\n\n"
                                                       f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")
            else:
                bot.send_message(chat_id=chat_id, text=f"У вас проверили работу "
                                                       f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                                       f"Работа принята!\n\n"
                                                       f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")

    except requests.exceptions.ReadTimeout:
        time.sleep(5)
    except requests.ConnectionError:
        time.sleep(30)
