from __future__ import print_function
import sys
import libvirt
from loguru import logger as log


@log.catch
def get_node_info():
    conn = libvirt.open('qemu:///system')
    inf_dict = ['Модель', 'ОЗУ', 'Кол-во CPUs', 'MHz CPU',
                'Кол-во узлов NUMA', 'Кол-во CPU-sockets', 'Кол-во ядер процессора на сокет', 'Кол-во потоков процессора на ядро']
    node_info = conn.getInfo()
    buff = dict(zip(inf_dict, node_info))
    # log.debug(buff)
    conn.close()
    return buff

@log.catch
def create_new_instance(xmlFile_instance):
    conn = libvirt.open('qemu:///system')
    with open(xmlFile_instance, 'r') as f:
        xmlconf = f.read()
    inst = conn.defineXML(xmlconf)
    conn.close()

@log.catch
def get_list_instances():
    conn = libvirt.open('qemu:///system')
    list_instances = conn.listDefinedDomains()
    conn.close()
    return list_instances

@log.catch
def get_info_isntance(name):
    help_dict = ['Статус', 'ОЗУ', 'ОЗУ(есть)', 
                 'Использует ядер', 'Работает']
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(name)
    info = instance.info()
    buff = dict(zip(help_dict, info))
    # log.debug(buff)
    conn.close()

@log.catch
def start_instance(name):
    conn = libvirt.open('qemu:///system')
    instance = conn.lookupByName(name)
    instance.create()
    conn.close()

def main():
    # start_instance('cirros')


if __name__ == "__main__":
    main()
