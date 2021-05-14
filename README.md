# VPS on Telegram-bot  

## Описание  
#### Что такое VPS хостинг
**VPS (Virtual Private Server)** — это хостинг-услуга, где пользователю предоставляется виртуальный сервер с максимальными привилегиями. VPS эмулирует работу реального физического сервера — есть root-доступ, возможна установка своих операционных систем и программного обеспечения.  

#### Что умеет данный бот
С помощью данного бота есть возможность:  
> Создавать\удалять свою ВМ  
> Включить\выключить свою ВМ  
> Получить подробную информацию о ВМ и гипервизоре  
> Переслать свой *публичный ключ* на машину  

В тестовом режиме используется AlpineOS Standart x86-64 (512MB/4GB)  

**Frontend** проекта - удобный интерфейс телеграмм-бота, который позволяет совершать действия над виртуальными машинами, без каких-либо технических навыков.

*Данный проект создан на основе *open-source* технологий и в учебных целях. Более глубокий разбор - [тут](https://github.com/rombintu/project12/blob/main/bot/README.md)
## Установка зависимостей pip  
```sh
pip install -r requirements.txt
```  

### Прочие зависимости 
```sh
qemu=>1.5.2
qemu-kvm=>1.5.2
libvirt=>7.0.0
postgresql=>10
```  
###### *Прочитайте [postgresql](https://github.com/rombintu/project12/blob/main/tests/psql_help.md)

## Бот часть  
### API  
| Файл | Описание |
| :----: | -------- |
| sql_api | Управление БД |
| ssh_api | Передача ключей |
| libvirt_api | Управление ВМ |
| sign_api | Подпись файла и проверка ЭЦП
| parse_smiles | Создание файла с кодировками смайлов |

### Запуск  
```sh
git clone https://github.com/rombintu/project12.git
cd project12
cp bot/config.py.bak bot/config.py
настройте файл config.py  
python3 main.py
```

## Сайт часть  
### Запуск  
```sh
git clone https://github.com/rombintu/project12.git
cd project12/site
cp .env.bak .env
python3 -m flask run
```

## Источники  
* [libvirt](https://linuxhint.com/libvirt_python/)  
* [libvirt-api](https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/pdf/Version-1.1-Libvirt_Application_Development_Guide_Using_Python-en-US.pdf)  
* [kvm](https://www.rupython.com/kvm-api-89448.html)  
* [libvirt-more](https://wiki.libvirt.org/page/UbuntuKVMWalkthrough)  
* [libvirt-guid](https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections.html)  
* [how clone vm](https://www.cyberciti.biz/faq/how-to-clone-existing-kvm-virtual-machine-images-on-linux/)    
* [ssh-api](https://habr.com/ru/post/150047/)  
### License
MIT
