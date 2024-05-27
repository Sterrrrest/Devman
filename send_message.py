import telebot


def send_message(response, tg_token, tg_chat_id):

    bot = telebot.TeleBot(token=tg_token)

    if response.json()['new_attempts'][0]['is_negative']:
        bot.send_message(chat_id=tg_chat_id, text=f"У вас проверили работу "
                                               f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                               f"В ней есть ошибки\n\n"
                                               f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")
    else:
        bot.send_message(chat_id=tg_chat_id, text=f"У вас проверили работу "
                                               f"'{response.json()['new_attempts'][0]['lesson_title']}'\n\n "
                                               f"Работа принята!\n\n"
                                               f"Ссылка на работу: {response.json()['new_attempts'][0]['lesson_url']}")