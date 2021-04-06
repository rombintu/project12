import os
import paramiko as ssh
from config import USERNAME_SSH, PASSWORD_SSH, PORT_SSH, PUB_KEY_SERVER

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
    command = f'scp tmp/{keyfile}.txt alpine@{host_vm_user}:/home/alpine/.ssh/authorized_keys'
    os.system(command)


