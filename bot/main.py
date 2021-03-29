import telebot
import random as r

from requests import get
from telebot import types
from smiles import smile_dict
from config import TOKEN, vip
from dbfunc import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document'])
def getMessage(message):
    id_user = message.from_user.id
    text = message.text
    username = message.from_user.username

    
    commands = ['/start', '/addkey', '/id', '/info', '/registr']

    reg_btn = types.InlineKeyboardButton('Быстрая регистрация', callback_data='registr')
    reg_cb_func = types.InlineKeyboardMarkup().add(reg_btn)
    

    def print_bot(text):
        rand_smile = r.choice(smile_dict)
        bot.send_message(id_user, f'{text} {rand_smile.decode()}')
    
    def send_pub_key(pub_key):
        pass

    # BODY
    if text == commands[0]: # START
        bot.send_message(id_user, "Привет, Я - Бот менеджер ваших виртуальных машин", reply_markup=reg_cb_func)
    elif text == commands[1]: # ADDKEY
        def add_key_func(message):
            def send_key_func(message, pub_key):
                req = message.text
                if req == '/cancel':
                    print_bot('Отмена отправки')
                    return False
                elif req == '/send':
                    send_pub_key(pub_key)
                    print_bot('Ключи отправлены')
            if message.text:
                pub_key = message.text
                send_pub_key(pub_key)
                print_bot('Ключи отправлены')
            elif message.document:
                doc_id = message.document.file_id
                file_info = bot.get_file(doc_id)
                doc = get(f'http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}').content
                print_bot(doc.decode())

                
                print_bot('Если все верно, нажмите /send, иначе нажмите /cancel')
                bot.register_next_step_handler(message, send_key_func, doc.decode())
            else:
                print_bot('Ожидается файл или текст')
        print_bot("Пришлите ключ файлом или текстом")
        bot.register_next_step_handler(message, add_key_func)
    elif text == commands[2]: # get ID
        print_bot(id_user)
    elif text == commands[3]: # INFO
        pass
    elif text == commands[4]: # REGISTRATION
        reg(id_user)
    else:
        print_bot("Неизвестная команда, попробуйте нажать на '/'")



@bot.callback_query_handler(func=lambda c: c.data == 'registr')
def process_callback_button1(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    id_user = callback_query.from_user.id
    answer = reg(id_user)
    bot.send_message(id_user, answer)

# MAIN
if __name__ == "__main__":
    print('Bot is starting...')
    bot.polling(none_stop=True)