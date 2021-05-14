import telebot
import random as r

from requests import get
from telebot import types
from loguru import logger as log

# LOCAL FILES
import libvirt_api as virt
import sign_api
from codec_smiles import smile_dict
from config import TOKEN, vip
from sql_api import *
from ssh_api import send_keys_with_password


# INIT
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document'])
def getMessage(message):
    id_user = message.from_user.id
    text = message.text
    username = f'@{message.from_user.username}'

    
    commands = ['/start', '/addkey', '/id', '/info', '/registr', '/manage', '/hi_admin', '/activate', '/all']

    kommands = ['Вкл/Выкл', 'Создать/Удалить', 'Информация о ВМ', 'Закинуть ключи', 'Информация о гипервизоре']
    keyboard = types.ReplyKeyboardMarkup()
    
    reg_btn = types.InlineKeyboardButton('Быстрая регистрация', callback_data='registr')
    reg_cb_func = types.InlineKeyboardMarkup().add(reg_btn)
    
    def write_key_in_file(id_user, pub_key):
        # Вспомогательная функция (записывает ключ в tmp-file)
        with open(f'tmp/{id_user}.txt', 'w') as f:
            f.write(pub_key)

    def print_bot(text):
        # Вспомогательная функция (Отправка сообщения + рандомный смайлик)
        rand_smile = r.choice(smile_dict)
        bot.send_message(id_user, f'{text} {rand_smile.decode()}')
    

    # BODY
    if text == commands[0]: # START
        bot.send_message(id_user, "Привет, Я - Бот менеджер ваших виртуальных машин", reply_markup=reg_cb_func)
    elif text == commands[1] or text == kommands[3]: # ADDKEY
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        if not check_account(id_user):
            print_bot('Ваш статус неактивен, отправьте заявку администратору /hi_admin')
            return False
        @log.catch
        def add_key_func(message):
            # Обработка ключей
            def send_key_func(message, pub_key, pb, sign):
                # Отправка ключей
                req = message.text
                if req == '/cancel':
                    print_bot('Отмена отправки')
                    return False
                # ПРОВЕРКА ЭЦП -------------------------------------------
                elif req == '/send' and sign_api.check(pub_key, pb, sign):
                    try:
                        write_key_in_file(id_user, pub_key)
                        ip_vm = get_ip_vm(id_user)
                        try:
                            send_keys_with_password(ip_vm, id_user)
                            print_bot('Ключи отправлены!')
                            update_user_info(id_user, 'pub_key_status', 'True')
                        except Exception as e:
                            print_bot(e)
                            return False
                    except Exception as e:
                        error = 'Что то пошло не так /info\n' + 'SYS: ' + str(e)
                        print_bot(error)
            if message.text:
                pub_key = message.text
                pb, sign = sign_api.create_sign(pub_key)
                print_bot(pub_key)
                print_bot('Если все верно, нажмите /send, иначе нажмите /cancel')
                bot.register_next_step_handler(message, send_key_func, pub_key, pb, sign)
            elif message.document:
                doc_id = message.document.file_id
                file_info = bot.get_file(doc_id)
                pub_key = get(f'http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}').content
                print_bot(pub_key.decode())
                pb, sign = sign_api.create_sign(pub_key.decode())
                print_bot('Если все верно, нажмите /send, иначе нажмите /cancel')
                bot.register_next_step_handler(message, send_key_func, pub_key.decode(), pb, sign)
            else:
                print_bot('Ожидается файл или текст')
        print_bot("Пришлите ключ файлом или текстом")
        bot.register_next_step_handler(message, add_key_func)
    elif text == commands[2]: # get ID
        print_bot(id_user)
    elif text == commands[3]: # INFO
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        try:
            info = get_info(id_user)
        except:
            print_bot('Похоже вы не зарегистрированы /start')
            return False
        help_dict = ['Статус аккаунта', 'Виртуальная машина', 'Ключи на машине', 'Адрес ВМ']
        buff_dict = dict(zip(help_dict, info))
        buff = ''
        for key in buff_dict:
            buff += f'{key} : {buff_dict[key]} \n'
        bot.send_message(id_user, buff) # чтобы не было смайликов
    elif text == commands[4]: # REGISTRATION
        print_bot(reg(id_user, username))
    elif text == commands[5]: # MANAGE
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        keyboard.row(kommands[0], kommands[1])
        keyboard.row(kommands[3], kommands[2])
        keyboard.row(kommands[4])
        bot.send_message(id_user, "Выбери действие", reply_markup=keyboard)
    elif text == kommands[0]: # On/Off
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        if not check_account(id_user):
            print_bot('Ваш статус неактивен, отправьте заявку администратору /hi_admin')
            return False
        try:
            if virt.status_instance(id_user):
                virt.stop_instance(id_user)
                print_bot('ВМ остановлена подождите 10 секунд')
            else:
                virt.start_instance(id_user)
                print_bot('ВМ запущена, подождите 30 секунд')
        except Exception as e:
            error = 'Видимо машина не создана\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == kommands[1]: # Create/Delete
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        if not check_account(id_user):
            print_bot('Ваш статус неактивен, отправьте заявку администратору /hi_admin')
            return False
        try:
            info = virt.get_info_instance(id_user)
            if info['Работает'] == 'Да':
                print_bot('Перед этой операцией нужно выключить машину')
                return False
        except Exception as e:
            pass

        list_instances = virt.get_list_instances()
        if str(id_user) in list_instances:
            @log.catch
            def delete_func(message):
                # Удаление машины после подтверждения
                text = (message.text).lower()
                if text == 'д' or text == 'y':
                    try:
                        virt.delete_instance(id_user)
                        print_bot('Машина удалена')
                        update_user_info(id_user, 'vm_status', 'False')
                    except Exception as e:
                        error = 'Что то пошло не так\n' + 'SYS: ' + str(e)
                        print_bot(error)
                else:
                    print_bot('Отмена операции')

            print_bot('Хотите удалить ВМ? [Д/н]')
            bot.register_next_step_handler(message, delete_func)
        else:
            try:
                print_bot("""Ваша виртуальная машина создается, пожалуйста подождите 1 минуту и нажмите 'Информация о ВМ'""")
                virt.clone_instance('alpine_orig', id_user)
                update_user_info(id_user, 'vm_status', 'True')
            except Exception as e:
                error = 'Видимо ваша машина еще не создана\n' + 'SYS: ' + str(e)
                print_bot(error)
            
    elif text == kommands[2]: # GET Info
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        if not check_account(id_user):
            print_bot('Ваш статус неактивен, отправьте заявку администратору /hi_admin')
            return False
        try:
            info = virt.get_info_instance(id_user)
            buff = ''
            for key in info:
                buff += f'{key} : {info[key]}\n'
            print_bot(buff + '/getip - присвоить IP адрес\n/info - мой аккаунт')
        except Exception as e:
            error = 'Видимо ВМ не создано\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == '/getip': # GET IP VM
        if not check_account(id_user):
            print_bot('Ваш статус неактивен, отправьте заявку администратору /hi_admin')
            return False
        try:
            ip_vm = virt.get_ip(id_user)
            print_bot(ip_vm)
            update_user_info(id_user, 'ip_vm', ip_vm)
        except Exception as e:
            error = 'Видимо ваша машина еще не создана или не работает\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == kommands[4]: # GET INFO ABOUT GPV
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        try:
            info = virt.get_node_info()
            buff = ''
            for key in info:
                buff += f'{key} : {info[key]}\n'
            print_bot(buff)
        except Exception as e:
            error = 'Что то пошло не так\n' + 'SYS: ' + str(e)
            print_bot(error)
    elif text == commands[6]: # SEND REQ TO ADMIN
        if not check_reg(id_user):
            print_bot('Пройдите пожалуйста регистрацию /start')
            return False
        bot.send_message(vip['admin'], f'Пользователь: {username}\nID: {id_user}\n/activate')
    elif text == commands[7]: # SET STATUS ACTIVE
        if id_user not in vip.values():
            print_bot('Это действие может делать только администратор')
            return False
        def set_status_active(message):
            text = (message.text).split(' ')
            user_id = text[0]
            try:
                status = int(text[1])
            except:
                print_bot('Напиши айди пользователя и 1/0')
                return False
            change_status(user_id, status)
            bot.send_message(int(user_id), 'Ваш статус изменился\n/info')
            print_bot('Готово')
        print_bot('Напиши айди пользователя и число')
        bot.register_next_step_handler(message, set_status_active)
    elif text == commands[8]: # GET CLIENTS
        if id_user not in vip.values():
            print_bot('Это действие может делать только администратор')
            return False
        help_dict = ['Имя', 'ID', 'Статус аккаунта', 'Адрес ВМ']
        clients = get_all_clients()
        buff = ''
        for client in clients:
            info_client = dict(zip(help_dict, client))
            for key in info_client:
                buff += f'{key} : {info_client[key]} \n'
            print_bot(buff)
    else:
        print_bot("Неизвестная команда, попробуйте нажать на '/'")


@bot.callback_query_handler(func=lambda c: c.data == 'registr')
def process_callback_button1(callback_query: types.CallbackQuery):
    # Структура callback-функции для регистрации пользователя
    bot.answer_callback_query(callback_query.id)
    id_user = callback_query.from_user.id
    username = "@" + str(callback_query.from_user.username)
    answer = reg(id_user, username)
    bot.send_message(id_user, answer)

# MAIN
if __name__ == "__main__":
    print('Bot is starting...')
    bot.polling(none_stop=True)
