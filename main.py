import time
import requests

from functions import send_message
from environs import Env


if __name__ == '__main__':

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
                    send_message(response_last_attempt, tg_token, chat_id)
            else:
                if response.json()['new_attempts'][0]['is_negative']:
                    send_message(response, tg_token, chat_id)

        except requests.exceptions.ReadTimeout:
            time.sleep(5)
        except requests.ConnectionError:
            time.sleep(30)
