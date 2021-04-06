# SERVER
import socket

sock = socket.socket()
sock.bind(('25.52.54.55', 9090))
sock.listen(2)

conn, address = sock.accept()

print(f"New connection: {address}")

def Listening():
    data = conn.recv(1024)
    if len(data) > 0: print(data.decode())
    else: return False
    
while True:
    Listening()

conn.close()
