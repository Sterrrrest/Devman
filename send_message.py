import telebot
from textwrap import dedent


def send_message(response, tg_token, tg_chat_id):

    bot = telebot.TeleBot(token=tg_token)

    if response['new_attempts'][0]['is_negative']:
        text_accept = dedent((f'''
        У вас проверили работу '{response['new_attempts'][0]['lesson_title']}'
        В ней есть ошибки
        Ссылка на работу: {response['new_attempts'][0]['lesson_url']}'''))

        bot.send_message(chat_id=tg_chat_id, text=text_accept)
    else:
        bot.send_message(chat_id=tg_chat_id, text=dedent(f'''
        У вас проверили работу '{response['new_attempts'][0]['lesson_title']}'
        Работа принята!
        Ссылка на работу: {response['new_attempts'][0]['lesson_url']}'''))
