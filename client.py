import socket
import threading

nickname = input('Enter a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '192.168.56.1'
PORT = 8082

client.connect((HOST, PORT))


def receive():
    while True:
        message = client.recv(1024).decode('ascii')
        if message == 'NICK':
            client.send(nickname.encode('ascii'))
        else:
            print(message)


def send():
    while True:
        message = f'{input()}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
