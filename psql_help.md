# Скачать postgresql (ubuntu\debian\kali\подобное)
> sudo apt-get update  
> sudo apt-get install postgresql-13  
> sudo service start postgresql  
> sudo service enable postgresql  
> service status postgresql  

# Создать пользователя и бд
> sudo -i  
> su - postgres  
> createdb testdb  
> psql -U postgres template1   
> $ SELECT * FROM pg_user; (узнаем какие есть пользователи)  
> $ CREATE USER test WITH PASSWORD 'password';  
> $ GRANT ALL PRIVILEGES ON DATABASE "testdb" to test;  
> $ \q  (чтобы выйти)  

# Теперь можно зайти в нашу бд новым пользователем  
> psql -U test testdb  
> $ SELECT version();  
> теперь можно заняться work_with_db.py

# Если возникли какие то проблемы  
> https://www.dmosk.ru/miniinstruktions.php?mini=postgresql-users  
> https://postgrespro.ru/docs/postgresql/9.6/app-createuser  
> https://apps.timwhitlock.info/emoji/tables/unicode - сайт с кодировками смайликов  