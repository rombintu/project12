import os
import paramiko as ssh
from config import USERNAME_SSH, PASSWORD_SSH, PORT_SSH

def get_keys(file_name):
    with open(f'tmp/{file_name}.txt', 'r') as f:
        key = f.read()
        return key

def send_keys_with_password(host_vm_user, keyfile):
    # Отправка ключей с использованием пароля
    transport = ssh.Transport((host_vm_user, PORT_SSH))
    transport.connect(username=USERNAME_SSH, password=PASSWORD_SSH)
    sftp = ssh.SFTPClient.from_transport(transport)
    local_path = f'tmp/{keyfile}.txt'
    remote_path = '/home/alpine/.ssh/authorized_keys'
    sftp.put(local_path, remote_path)
    sftp.close()
    transport.close()

def send_keys_os(host_vm_user, keyfile):
    # Отправка ключей без пароля (beta)
    pub_key_server = get_keys('pub_key_server')
    pub_key_client = get_keys(keyfile)
    with open('tmp/tmp.txt', 'w') as f:
        f.write(pub_key_server + pub_key_client)
    command = f'scp tmp/tmp.txt alpine@{host_vm_user}:/home/alpine/.ssh/authorized_keys'
    os.system(command)


