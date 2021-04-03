import os
import paramiko as ssh
from config import username, password

def send_keys_with_password(host, keyfile):
    # Отправка ключей с использованием пароля
    port = 22
    transport = ssh.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = ssh.SFTPClient.from_transport(transport)

    local_path = f'tmp/{keyfile}'
    remote_path = '/home/alpine/.ssh/authorized_keys'
    
    sftp.put(local_path, remote_path)

    sftp.close()
    transport.close()

def send_keys_os(host, keyfile):
    # Отправка ключей без пароля (beta)
    with open(f'tmp/{keyfile}', 'r') as f:
        buff = f.read()
    command = f'scp tmp/{keyfile} alpine@{host}:/home/alpine/.ssh/authorized_keys'
    os.system(command)


