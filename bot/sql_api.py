import psycopg2 # подключаем библиотеку для апи к бд (подробности https://www.postgresqltutorial.com/postgresql-python/)

from config import DB_NAME, USER_NAME, USER_PASSWORD, HOST # импортируем данные авторизации
# чтобы все работало нужно скачать модуль (pip install -r req.txt) или (pip install psycopg2)
# и установить\создать бд (читайте README.md)

def reg(user_id):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST) # коннектимся под каким нибудь логином в бд
        sql = db.cursor() # создаем курсор
        script = """INSERT INTO clients (user_id, user_status, vm_status, pub_key_status, ip_vm) 
                        VALUES (%s, 'Inactive', 'False', 'False', 'False')""" # пишем скрипт (подробности https://postgrespro.ru/docs/postgresql/9.6/sql-insert)
        try:
            sql.execute(script, (user_id,)) # выполняем скрипт
            db.commit()
            return "Регистрация прошла успешно"
        except Exception as e:
            #print(e) # чтобы получить подробности ошибки - раскоментить
            return "Вы уже зарегистрированы"
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"

def get_info(user_id):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """SELECT user_status, vm_status, pub_key_status, ip_vm FROM clients
                        WHERE user_id=%s"""
        try:
            sql.execute(script, (user_id,))
            info = sql.fetchone()
            return info
        except Exception as e:
            #print(e)
            return "Пройдите пожалуйста регистрацию /start"
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"

def update_ip_vm(user_id, ip_vm):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """UPDATE clients
                        SET ip_vm=%s
                        WHERE user_id=%s"""
        try:
            sql.execute(script, (ip_vm, user_id,))
            db.commit()
        except Exception as e:
            #print(e)
            return "Пройдите пожалуйста регистрацию /start"
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"

def get_ip_vm(user_id):
    try:
        db = psycopg2.connect(dbname=DB_NAME, user=USER_NAME, 
                        password=USER_PASSWORD, host=HOST)
        sql = db.cursor()
        script = """SELECT ip_vm FROM clients
                        WHERE user_id=%s"""
        try:
            sql.execute(script, (user_id,))
            ip_vm = sql.fetchone()[0]
            return ip_vm
        except Exception as e:
            #print(e)
            return "Пройдите пожалуйста регистрацию /start"
    except Exception as e:
        #print(e)
        return "Проблемы с подключением к БД"
