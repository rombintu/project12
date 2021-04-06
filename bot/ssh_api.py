import os
import paramiko as ssh
from config import USERNAME_SSH, PASSWORD_SSH, PORT_SSH, PUB_KEY_SERVER

def send_keys_with_password(HOST, keyfile):
    # Отправка ключей с использованием пароля
    transport = ssh.Transport((HOST, PORT_SSH))
    transport.connect(username=username, password=password)
    sftp = ssh.SFTPClient.from_transport(transport)

    local_path = f'tmp/{keyfile}.txt'
    remote_path = '/home/alpine/.ssh/authorized_keys'
    
    sftp.put(local_path, remote_path)

    sftp.close()
    transport.close()

def send_keys_os(HOST, keyfile):
    # Отправка ключей без пароля (beta)
    command = f'scp tmp/{keyfile}.txt alpine@{HOST}:/home/alpine/.ssh/authorized_keys'
    os.system(command)


