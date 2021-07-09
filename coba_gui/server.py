import socket
import threading
import numpy
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
name_of_clients = []
role_of_clients = []
undercover_words = ['fanta', 'singa', 'pecel', 'alfamart', 'sapi']
civillian_words = ['sprite', 'macan', 'gado-gado', 'indomaret', 'kerbau']


def clientthread(conn, addr):
    while True:
        try:
            data = conn.recv(2048).decode()
            if data:
                if "joined" in data:
                    print(data)
                    name_of_clients.append(data.split(" ")[0])
                    role_of_clients = numpy.ones(10)
                    role_of_clients[8:] = 0
                    random.shuffle(role_of_clients)
                    index = random.randint(0, 4)
                    undercover_words[index]
                    print(undercover_words[index])
                    print(role_of_clients)
                    broadcast(data, conn)
                else:
                    print(data.split(" ")[0] + ' : ' + data.partition(' ')[2])
                    message_to_send = data.split(
                        " ")[0] + ' : ' + data.partition(' ')[2]
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(list_of_clients)
    # print(addr[0] + ' connected')
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
