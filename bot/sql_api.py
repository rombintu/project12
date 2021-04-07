from loguru import logger as log
import psycopg2 # подключаем библиотеку для апи к бд (подробности https://www.postgresqltutorial.com/postgresql-python/)

from config import DB_NAME, USER_NAME, USER_PASSWORD, HOST # импортируем данные авторизации
# чтобы все работало нужно скачать модуль (pip install -r req.txt) или (pip install psycopg2)
# и установить\создать бд (читайте README.md)

@log.catch
def reg(id_user):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST) # коннектимся под каким нибудь логином в бд
        sql = db.cursor() # создаем курсор
        script = """INSERT INTO clients (id_user) 
                        VALUES (%s)""" # пишем скрипт (подробности https://postgrespro.ru/docs/postgresql/9.6/sql-insert)
        try:
            sql.execute(script, (id_user,)) # выполняем скрипт
            db.commit()
            return "Регистрация прошла успешно"
        except Exception as e:
            print(e) # чтобы получить подробности ошибки - раскоментить
            return "Вы уже зарегистрированы"
        db.close()
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"

@log.catch
def get_info(id_user):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """SELECT user_status, vm_status, pub_key_status, ip_vm FROM clients
                        WHERE id_user=%s"""
        try:
            sql.execute(script, (id_user,))
            info = sql.fetchone()
            return info
        except Exception as e:
            print(e)
            return "Пройдите пожалуйста регистрацию /start"
        db.close()
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"

# @log.catch
# def update_ip_vm(id_user, ip_vm):
#     try:
#         db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
#                         password=USER_PASSWORD, host=HOST)
#         sql = db.cursor()
#         script = """UPDATE clients
#                         SET ip_vm=%s
#                         WHERE id_user=%s"""
#         try:
#             sql.execute(script, (ip_vm, id_user,))
#             db.commit()
#         except Exception as e:
#             #print(e)
#             return "Пройдите пожалуйста регистрацию /start"
#     except Exception as e:
#         #print(e)
#         return "Проблемы с подключением к БД"

@log.catch
def update_user_info(id_user, column_update, on_what_update):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        # buff = ''
        # for i, el in enumerate(columns_update_list):
        #     buff += f'{el}={onwhat_update_list[i]}, '
        script = f"""UPDATE clients
                        SET {column_update}=%s
                        WHERE id_user=%s"""
        try:
            sql.execute(script, (on_what_update, id_user,))
            db.commit()
        except Exception as e:
            print(e)
        db.close()
    except Exception as e:
        print(e)

@log.catch
def get_ip_vm(id_user):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """SELECT ip_vm FROM clients
                        WHERE id_user=%s"""
        try:
            sql.execute(script, (id_user,))
            ip_vm = sql.fetchone()[0]
            return ip_vm
        except Exception as e:
            print(e)
        db.close()
    except Exception as e:
        print(e)

@log.catch
def check_account(id_user):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """SELECT user_status FROM clients
                        WHERE id_user=%s"""
        try:
            sql.execute(script, (id_user,))
            pre_status = sql.fetchone()[0]
            if pre_status == 'False':
                status = 0
            else: status = 1
            return status
        except Exception as e:
            print(e)
        db.close()
    except Exception as e:
        print(e)

@log.catch
def change_status(id_user, status):
    if status: status = 'True'
    else: status = 'False'
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """UPDATE clients
                        SET user_status=%s
                        WHERE id_user=%s"""
        try:
            sql.execute(script, (status, id_user))
            db.commit()
        except Exception as e:
            error = 'Пользователь не найден\n' + 'SYS: ' + str(e)
            print_bot(error)
        db.close()
    except Exception as e:
        error = 'Проблемы с подключением к БД\n' + 'SYS: ' + str(e)
        print_bot(error)
        
