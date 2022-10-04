import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8082
server.bind((HOST, PORT))

print(HOST)

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))


def handle(client, address, nickname):
    try:
        while True:
            message = client.recv(1024).decode('ascii')
            broadcast(f'{nickname}: {message}')
    except:
        print(f'{address} has disconnected.')
        client.close()
        clients.remove(client)

        broadcast(f'{nickname} has disconnected.')
        nicknames.remove(nickname)


def receive():
    while True:
        conn, addr = server.accept()
        print(f'{addr} has connected.')

        conn.send('NICK'.encode('ascii'))
        nickname = conn.recv(1024).decode('ascii')
        nicknames.append(nickname)

        conn.send(f'Connected to {HOST, PORT}.'.encode('ascii'))
        broadcast(f'{nickname} has joined.')

        clients.append(conn)

        handle_thread = threading.Thread(target=handle, args=(conn, addr, nickname))
        handle_thread.start()


server.listen()
print('Server is listening...')

receive_thread = threading.Thread(target=receive)
receive_thread.start()
