from loguru import logger as log
from config import TABLE_NAME as table
import psycopg2 # подключаем библиотеку для апи к бд (подробности https://www.postgresqltutorial.com/postgresql-python/)


from config import DB_NAME, USER_NAME, USER_PASSWORD, HOST # импортируем данные авторизации
# чтобы все работало нужно скачать модуль (pip install -r req.txt) или (pip install psycopg2)
# и установить\создать бд (читайте README.md)


@log.catch
def reg(id_user, username):
    # Регистрация пользователя
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST) # коннектимся под каким нибудь логином в бд
        sql = db.cursor() # создаем курсор
        script = f"""INSERT INTO {table} (id_user, user_name) 
                        VALUES (%s, %s)""" # пишем скрипт (подробности https://postgrespro.ru/docs/postgresql/9.6/sql-insert)
        try:
            sql.execute(script, (id_user, username,)) # выполняем скрипт
            db.commit()
            return "Регистрация прошла успешно"
        except Exception as e:
            print(e) # чтобы получить подробности ошибки - раскоментить
            return "Вы уже зарегистрированы"
        db.close()
    except Exception as e:
        print(e)
        

@log.catch
def get_info(id_user):
    # Описание 
    """Возвращает список:
            * статус аккаунта (активн\неактив)
            * статус машины (вкл\выкл)
            * статус ключей (на машине\нет)
            * адрес машины
    """
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""SELECT user_status, vm_status, pub_key_status, ip_vm 
                        FROM {table}
                            WHERE id_user=%s"""
        sql.execute(script, (id_user,))
        info = sql.fetchone()
        db.close()
        return info
    except Exception as e:
        print(e)
        

@log.catch
def get_all_clients():
    # Возвращает список всех пользователей (для администраторов)
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""SELECT user_name, id_user, user_status, ip_vm 
                        FROM {table}"""
        sql.execute(script)
        info = sql.fetchall()
        db.close()
        return info
    except Exception as e:
        print(e)
        

@log.catch
def check_reg(id_user):
    # Проверяет наличие пользователя в БД (т.е. регистрацию)
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""SELECT exists(
                        SELECT * FROM {table}
                            WHERE id_user=%s)"""
        sql.execute(script, (id_user,))
        exists = sql.fetchone()[0]
        db.close()
        return exists
    except Exception as e:
        print(e)
        

@log.catch
def update_user_info(id_user, column_update, on_what_update):
    # универсальная функция для изменения информации о пользователе
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""UPDATE {table}
                        SET {column_update}=%s
                            WHERE id_user=%s"""
        sql.execute(script, (on_what_update, id_user,))
        db.commit()
        db.close()
    except Exception as e:
        print(e)


@log.catch
def get_ip_vm(id_user):
    # Возвращает ip-адрес пользователя
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""SELECT ip_vm FROM {table}
                        WHERE id_user=%s"""
        sql.execute(script, (id_user,))
        ip_vm = sql.fetchone()[0]
        db.close()
        return ip_vm
    except Exception as e:
        print(e)


@log.catch
def check_account(id_user):
    # Возвращает статус аккаунта пользователя (0 - False, 1 - True)
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""SELECT user_status FROM {table}
                        WHERE id_user=%s"""
        sql.execute(script, (id_user,))
        pre_status = sql.fetchone()[0]
        if pre_status == 'false':
            status = 0
        else: status = 1
        db.close()
        return status
    except Exception as e:
        print(e)


@log.catch
def change_status(id_user, status):
    # Изменяет статус аккаунта пользователя
    if status: status = 'True'
    else: status = 'false'
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = f"""UPDATE {table}
                        SET user_status=%s
                            WHERE id_user=%s"""
        try:
            sql.execute(script, (status, id_user))
            db.commit()
        except Exception as e:
            error = 'Пользователь не найден\n' + 'SYS: ' + str(e)
            print(error)
        db.close()
    except Exception as e:
        print(e)
        
