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

    timestamp = None

    while True:

        try:
            payLoad = {
                'timestamp': timestamp
            }
            response = requests.get(url_long, headers=headers, params=payLoad)
            response.raise_for_status()
            response_check = response.json()

            if response_check['status'] == 'found':
                send_message(response_check, tg_token, tg_chat_id)
                timestamp = response_check['last_attempt_timestamp']
            else:
                timestamp = response_check['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            time.sleep(30)
