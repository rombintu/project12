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

# Источники  
> https://linuxhint.com/libvirt_python/ - libvirt  
> https://www.rupython.com/kvm-api-89448.html  
> https://wiki.libvirt.org/page/UbuntuKVMWalkthrough  
> https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections.html  
> https://linuxhint.com/libvirt_python/  
> https://www.cyberciti.biz/faq/how-to-clone-existing-kvm-virtual-machine-images-on-linux/  
