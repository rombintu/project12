import telebot
import random as r

from requests import get
from telebot import types
from loguru import logger as log

# Локальные
from codec_smiles import smile_dict
from config import TOKEN, vip
from sql_api import *
from ssh_api import send_keys_with_password
import libvirt_api as virt

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document'])
def getMessage(message):
    id_user = message.from_user.id
    text = message.text
    username = message.from_user.username

    
    commands = ['/start', '/addkey', '/id', '/info', '/registr', '/manage']

    kommands = ['Вкл/Выкл', 'Создать/Удалить', 'Информация', 'Закинуть ключи', 'Информация о гипервизоре']
    keyboard = types.ReplyKeyboardMarkup()
    
    reg_btn = types.InlineKeyboardButton('Быстрая регистрация', callback_data='registr')
    reg_cb_func = types.InlineKeyboardMarkup().add(reg_btn)
    
    def write_key_in_file(id_user, pub_key):
        with opent(f'tmp/{id_user}.txt', 'w') as f:
            f.write(pub_key)

    def print_bot(text):
        rand_smile = r.choice(smile_dict)
        bot.send_message(id_user, f'{text} {rand_smile.decode()}')
    

    # BODY
    if text == commands[0]: # START
        bot.send_message(id_user, "Привет, Я - Бот менеджер ваших виртуальных машин", reply_markup=reg_cb_func)
    elif text == commands[1] or text == kommands[3]: # ADDKEY
        @log.catch
        def add_key_func(message):
            def send_key_func(message, pub_key):
                req = message.text
                if req == '/cancel':
                    print_bot('Отмена отправки')
                    return False
                elif req == '/send':
                    try:
                        write_key_in_file(id_user, pub_key)
                        ip_vm = get_ip_vm(id_user)
                        send_keys_with_password(ip_vm, id_user)
                        print_bot('Ключи отправлены!')
                    except Exception as e:
                        error = 'Что то пошло не так /info\n' + 'SYS: ' + str(e)
                        print_bot(error)
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
        help_dict = ['Статус аккаунта', 'Виртуальная машина', 'Ключи на машине', 'Адрес ВМ']
        info = get_info(id_user)
        buff_dict = dict(zip(help_dict, info))
        buff = ''
        for key in buff_dict:
            buff += f'{key} : {buff_dict[key]} \n'
        bot.send_message(id_user, buff)
            
    elif text == commands[4]: # REGISTRATION
        reg(id_user)
    elif text == commands[5]: # MANAGE
        keyboard.row(kommands[0], kommands[1])
        keyboard.row(kommands[3], kommands[2])
        keyboard.row(kommands[4])
        bot.send_message(id_user, "Выбери действие", reply_markup=keyboard)
    elif text == kommands[0]: # On/Off
        try:
            if virt.status_instance(id_user):
                virt.stop_instance(id_user)
                print_bot('ВМ остановлена')
            else:
                virt.start_instance(id_user)
                print_bot('ВМ запущена')
        except Exception as e:
            error = 'Видимо машина не создана\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == kommands[1]: # Create/Delete
        # try:
        #     list_instance = virt.get_list_instances()
        #     log.debug(list_instance)
        # except Exception as e:
            # print(e)
        # ДЕЛАТЬ КАКУЮ ТО ПРОВЕРКУ
        if str(id_user) in list_instance:
            @log.catch
            def delete_func(message):
                text = (message.text).lower()
                if text == 'д' or text == 'y':
                    try:
                        #virt.delete_instance(id_user)
                        print_bot('Машина удалена')
                        # ИЗМНЕНИТЬ ДАННЫЕ В БД
                    except Exception as e:
                        error = 'Что то пошло не так\n' + 'SYS: ' + str(e)
                        print_bot(error)
                else:
                    print_bot('Отмена операции')

            print_bot('Хотите удалить ВМ? [Д/н]')
            bot.register_next_step_handler(message, delete_func)
        else:
            try:
                #virt.clone_instance('alpine_orig', id_user)
                # ИЗМНЕНИТЬ ДАННЫЕ В БД
                print_bot("""Ваша виртуальная машина создается, пожалуйста подождите 1 минуту и нажмите /getip""")
            except Exception as e:
                error = 'Видимо ваша машина еще не создана\n' + 'SYS: ' + str(e)
                print_bot(error)
            
    elif text == kommands[2]: # GET Info
        try:
            info = virt.get_info_instance(id_user)
            buff = ''
            for key in info:
                buff += f'{key} : {info[key]}\n'
            print_bot(buff)
        except Exception as e:
            error = 'Что то пошло не так\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == '/getip': # GET IP VM
        try:
            ip_vm = virt.get_ip(id_user)
            print_bot(ip_vm)
            update_ip_vm(user_id, ip_vm)
        except Exception as e:
            error = 'Видимо ваша машина еще не создана\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == kommands[4]: # GET INFO ABOUT GPV
        try:
            info = virt.get_node_info()
            buff = ''
            for key in info:
                buff += f'{key} : {info[key]}\n'
            print_bot(buff)
        except Exception as e:
            error = 'Что то пошло не так\n' + 'SYS: ' + str(e)
            print_bot(error)
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
