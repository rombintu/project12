import psycopg2 # подключаем библиотеку для апи к бд (подробности https://www.postgresqltutorial.com/postgresql-python/)

# чтобы все работало нужно скачать модуль (pip install -r req.txt) или (pip install psycopg2)
# и установить\создать бд (читайте README.md)

def reg(user_id):
    db = psycopg2.connect(dbname='testdb', user='test', 
                        password='password', host='localhost') # коннектимся под каким нибудь логином в бд
    sql = db.cursor() # создаем курсор
    script = """INSERT INTO vps (id, status_user, name_vm, status_vm, pub_key_host) 
                        VALUES (%s, 'inactive', 'none', 'none', 'none')""" # пишем скрипт (подробности https://postgrespro.ru/docs/postgresql/9.6/sql-insert)
    sql.execute(script, (user_id,)) # выполняем скрипт
    db.commit()
    print("Регистрация прошла успешно")
try:
    reg(1)
except Exception as e:
    print("Вы уже зарегистрированы")
    # print(e) # чтобы получить подробности ошибки - раскоментить
