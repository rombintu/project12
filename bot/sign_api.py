import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def create_sign_of_file(file_name):
    # Генерируем новый ключ
    key = RSA.generate(1024, os.urandom)
    # Получаем хэш файла
    hesh = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hesh.update(chunk)

    # Подписываем хэш
    signature = pkcs1_15.new(key).sign(hesh)

    # Получаем открытый ключ из закрытого
    pubkey = key.publickey()
    return pubkey, signature

def check_of_file(file_name, pubkey, signature):
    hesh = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hesh.update(chunk)
    # Переменная для проверки подписи
    check_sign = False
    try:
        pkcs1_15.new(pubkey).verify(hesh, signature)
        # Отличающийся хэш не должен проходить проверку
        # pkcs1_15.new(pubkey).verify(SHA256.new(b'test'), signature) # raise ValueError("Invalid signature")
        check_sign = True
        return check_sign
    except Exception as e:
        print(e)
        return check_sign    

def create_sign(content):
    key = RSA.generate(1024, os.urandom)
    hesh = SHA256.new(content.encode())
    signature = pkcs1_15.new(key).sign(hesh)
    pubkey = key.publickey()
    return pubkey, signature


def check(content, pubkey, signature):
    hesh = SHA256.new(content.encode())
    check_sign = False
    try:
        pkcs1_15.new(pubkey).verify(hesh, signature)
        check_sign = True
        return check_sign
    except Exception as e:
        print(e)
        return check_sign  

# pubkey, sign = create_sign('README.md')
# print(check('README.md', pubkey, sign))