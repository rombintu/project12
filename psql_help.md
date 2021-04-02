# Установка postgresql (ubuntu\debian\kali\подобное)
> `sudo apt-get update`  
> `sudo apt-get install postgresql-13` установка сервера  
> `sudo service start postgresql` запуск сервера  
> `sudo service enable postgresql` автозапуск  
> `service status postgresql` проверка  

## Создать пользователя и бд
> `sudo -i` становимся суперпользователем  
> `su - postgres` становимся пользователем postgres  
> `createdb testdb` создаем БД  
> `psql -U postgres template1` заходим в дефолтную БД   
> $ `SELECT * FROM pg_user;` узнаем какие есть пользователи  
> $ `CREATE USER test WITH PASSWORD 'password';`  
> $ `GRANT ALL PRIVILEGES ON DATABASE "testdb" to test;`  
> $ `\q`  чтобы выйти  

## Заходим в нашу бд под новым пользователем  
> `psql -U test testdb`  
> $ `SELECT version();`  
> если нужно настроить удаленное [подключение](https://www.dmosk.ru/miniinstruktions.php?mini=pgsql-remote)
> теперь можно заняться work_with_db.py

### Если возникли какие то проблемы  
[раз](https://www.dmosk.ru/miniinstruktions.php?mini=postgresql-users)  
[два](https://postgrespro.ru/docs/postgresql/9.6/app-createuser)  
  
