# Установка postgresql (ubuntu\debian\kali\подобное)
```sh
sudo apt-get update
sudo apt-get install postgresql-13; echo "установка сервера"
sudo service start postgresql; echo "запуск сервера" 
sudo service enable postgresql; echo "автозапуск"  
service status postgresql; echo "проверка" 
```

## Создать пользователя и бд
```sh
sudo -i
su - postgres  
createdb testdb
psql -U postgres template1  
$ SELECT * FROM pg_user;
$ CREATE USER test WITH PASSWORD 'password'; 
$ GRANT ALL PRIVILEGES ON DATABASE "testdb" to test; 
$ \q
```
## Заходим в нашу бд под новым пользователем  
```sh
psql -U test testdb
$ SELECT version();
```

> если нужно настроить удаленное [подключение](https://www.dmosk.ru/miniinstruktions.php?mini=pgsql-remote)  
> теперь можно заняться work_with_db.py

### Если возникли какие то проблемы  
[раз](https://www.dmosk.ru/miniinstruktions.php?mini=postgresql-users)  
[два](https://postgrespro.ru/docs/postgresql/9.6/app-createuser)  
  
