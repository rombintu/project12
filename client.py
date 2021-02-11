import socket

message = input("Enter your message: ")

sock = socket.socket()
sock.connect(('25.52.54.55', 9090))
sock.send(message.encode())


sock.close()
