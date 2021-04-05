import libvirt
import os

from loguru import logger as log

from alpine_for_clone import clone, volume

def get_orig_name():
    # Получение названия хранилища оригинала
    conn = libvirt.open('qemu:///system')
    pools = conn.listAllStoragePools(0)
    # name = pools[-1].listVolumes()[0].split('.')[0] # Получение имени
    return pools[-1].listVolumes()[0]

def get_node_info():
    # Возвращает словарь с информацией о гипервизоре
    conn = libvirt.open('qemu:///system')
    inf_dict = ['Модель', 'ОЗУ', 'Кол-во CPUs', 'MHz CPU',
                'Кол-во узлов NUMA', 'Кол-во CPU-sockets', 
                'Кол-во ядер процессора на сокет', 
                'Кол-во потоков процессора на ядро']
    node_info = conn.getInfo()
    buff = dict(zip(inf_dict, node_info))    
    conn.close()
    return buff

def create_new_instance_xml(xmlFile_instance):
    # Создает новую машину из XML файла
    conn = libvirt.open('qemu:///system')
    with open(xmlFile_instance, 'r') as f:
        xmlconf = f.read()
    conn.defineXML(xmlconf)
    conn.close()

def create_new_instance(name):
    # Создает новую машину из шаблона
    conn = libvirt.open('qemu:///system')
    new_volume = volume.format(name_1=name, name_2=name)
    new_vm = clone.format(name_1=name, name_2=name)
    pool = conn.storagePoolLookupByName('default')
    pool.createXML(new_volume, 0)
    conn.defineXML(new_vm)
    conn.close()

def clone_instance(original, clone):
    # Клонирует оригинал
    os.system(f"virt-clone --original {original} --name {str(clone)} --auto-clone")

def delete_instance(name):
    # Удаляет машину
    conn = libvirt.open('qemu:///system')

    if str(name) == 'alpine_orig': # на всякий случай
        return False

    pool = conn.storagePoolLookupByName('default')
    volume = pool.storageVolLookupByName(f'{name}.qcow2')
    instance = conn.lookupByName(str(name))
    instance.undefine()
    volume.delete(0)
    conn.close()

def get_list_instances():
    # Возвращает массив доступных машин
    conn = libvirt.open('qemu:///system')
    list_instances = conn.listDefinedDomains()
    conn.close()
    return list_instances

def get_ip(name):
    # Возвращает IP машины
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(str(name))
    data = list(instance.interfaceAddresses(0).values())
    ip = data[0]['addrs'][0]['addr']
    conn.close()
    return ip

def status_instance(name):
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(str(name))
    info = instance.info()
    status = info[4]
    conn.close()
    return status

def get_info_instance(name):
    # Возвращает словарь с информацией о конкретной машине
    help_dict = ['Статус', 'ОЗУ', 'ОЗУ(есть)', 
                 'Использует ядер', 'Работает']
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(str(name))
    info = instance.info()
    info[1] = f'{info[1]/1024} MB'
    info[2] = f'{info[2]/1024} MB'

    if info[4]: info[4] = 'Да'
    else: info[4] = 'Нет'

    buff = dict(zip(help_dict, info))
    conn.close()
    return buff

def start_instance(name):
    # Запускает машину по имени
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(str(name))
    instance.create()
    conn.close()

def stop_instance(name):
    # Останавливает машину по имени
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(str(name))
    instance.shutdown()
    conn.close()

# @log.catch
# def main():
#     # l = get_info_instance('alpine_orig')
#     # log.debug(l)
#     # start_instance('alpine_orig')
#     # stop_instance('alpine_clone')
#     # clone_instance('alpine_orig','alpine_clone')
#     # delete_instance('alpine_clone')
#     # log.debug(get_ip('alpine_orig'))

# if __name__ == "__main__":
#     main()
