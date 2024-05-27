import time
import requests

from send_message import send_message
from environs import Env


if __name__ == '__main__':

    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
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
            response_check = response.json()
            if response_check['status'] == 'timeout':

                response_timestamp = response_check['timestamp_to_request']
                payLoad_last_attempt = {
                    'timestamp': response_timestamp
                }
                response_last_attempt = requests.get(url_long, headers=headers, params=payLoad_last_attempt)
                response_last_attempt.raise_for_status()
                response_check_last_attempt = response_last_attempt.json()
                if response_check_last_attempt['found']:
                    send_message(response_check_last_attempt, tg_token, tg_chat_id)
            else:
                if response_check['new_attempts'][0]['is_negative']:
                    send_message(response_check, tg_token, tg_chat_id)

        except requests.exceptions.ReadTimeout:
            time.sleep(5)
        except requests.ConnectionError:
            time.sleep(30)
