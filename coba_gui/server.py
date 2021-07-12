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
voted_client = []
undercover_words = ['fanta', 'singa', 'pecel', 'alfamart', 'sapi']
civillian_words = ['sprite', 'macan', 'gado-gado', 'indomaret', 'kerbau']


def clientthread(conn, addr):
    while True:
        try:
            data = conn.recv(2048).decode()
            if data:
                if data.split("/")[0] == "joined":
                    print(data)
                    name_of_clients.append(data.split("/")[1])
                    # data = data.split("/")[1] + " joined"
                    broadcast(data, conn)
                elif data.split("/")[0] == "start":
                    number_of_clients = len(name_of_clients)
                    index = random.randint(0, 4)
                    if number_of_clients > 5:
                        role_of_clients = numpy.ones(number_of_clients)
                        role_of_clients[(number_of_clients-2):] = 0
                        random.shuffle(role_of_clients)
                    else:
                        role_of_clients = numpy.ones(number_of_clients)
                        role_of_clients[(number_of_clients-1):] = 0
                        random.shuffle(role_of_clients)
                        print(role_of_clients)
                    i = 0
                    for clients in list_of_clients:
                        if role_of_clients[i] == 1:
                            word_to_send = "word/" + civillian_words[index]
                        else:
                            word_to_send = "word/" + undercover_words[index]
                        print(word_to_send)
                        clients.send(word_to_send.encode())
                        i = i + 1
                elif data.split("/")[0] == "vote":
                    voted_client.append(data.split("/")[1])
                    if len(name_of_clients) == len(voted_client):
                        most_voted_client = "mostVoted/" + \
                            most_frequent(voted_client)
                        sendToAll(most_voted_client, conn)
                        voted_client.clear()
                else:
                    print(data.split("/")[0] + ' : ' + data.partition(' ')[2])
                    message_to_send = data.split(
                        "/")[0] + ' : ' + data.partition('/')[2]
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def most_frequent(List):
    return max(set(List), key=List.count)


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def sendToAll(message, connection):
    for clients in list_of_clients:
        clients.send(message.encode())


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
