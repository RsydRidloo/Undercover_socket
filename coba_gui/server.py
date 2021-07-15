import socket
import threading
import numpy
import random
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
name_of_clients = []
remaining_clients = []
role_of_clients = []
voted_client = []
undercover_words = ['fanta', 'singa', 'pecel', 'alfamart', 'sapi']
civillian_words = ['sprite', 'macan', 'gado-gado', 'indomaret', 'kerbau']
turn = 0
i = 0

def clientthread(conn, addr):
    global turn
    global role_of_clients
    global remaining_clients
    global i
    while True:
        try:
            data = conn.recv(2048).decode()
            print(data)
            if data:
                if data.split("/")[0] == "joined":
                    print(data)
                    name_of_clients.append(data.split("/")[1])
                    # data = data.split("/")[1] + " joined"
                    broadcast(data, conn)
                elif data.split("/")[0] == "start":
                    remaining_clients = name_of_clients.copy()
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
                    for clients in list_of_clients:
                        if role_of_clients[i] == 0:
                            word_to_send = "word/" + undercover_words[index]
                        else:
                            word_to_send = "word/" + civillian_words[index]
                        print(word_to_send)
                        clients.send(word_to_send.encode())
                        i = i + 1
                    sendToAll("clue_turn/" + name_of_clients[0], conn)
                elif data.split("/")[0] == "clue":
                    turn += 1
                    amount_of_client = len(name_of_clients)
                    broadcast("clue_send/" + data.split("/")[1], conn)
                    if turn%amount_of_client == 0:
                        sendToAll("discussion/", conn)
                        time.sleep(10)
                        sendToAll("vote_time/", conn)
                    else:
                        sendToAll("clue_turn/" + name_of_clients[turn%amount_of_client], conn)
                elif data.split("/")[0] == "vote":
                    voted_client.append(data.split("/")[1])
                    print(voted_client)
                    print(len(name_of_clients))
                    print(len(voted_client))
                    if len(name_of_clients) == len(voted_client):
                        name = most_frequent(voted_client)
                        remaining_clients.remove(name)
                        print(name)
                        index = name_of_clients.index(name)
                        print(index)
                        print(role_of_clients)
                        if(role_of_clients[index] == 0):
                            role = "undercover"
                        else:
                            role = "civillian"
                        print(role)
                        most_voted_client = "mostVoted/" + role + "/" + name
                        print(most_voted_client)
                        sendToAll(most_voted_client, conn)
                        voted_client.clear()
                        sendToAll("clue_turn/" + name_of_clients[0], conn)
                else:
                    # print(data.split("/")[0] + ' : ' + data.partition('/')[2])
                    message_to_send = data.split(
                        "/")[0] + ' : ' + data.partition('/')[2]
                    broadcast(message_to_send, conn)
            elif len(remaining_clients)<3:
                print("test1")
                if 0 not in role_of_clients:
                    sendToAll("undercover_win/", conn)
                    print("undercover_win")
                else:
                    sendToAll("civillian_win/", conn)
                    print("civillian_win")
            else:
                remove(conn)
        except:
            continue

def waitUntil(condition, output): #defines function
    wU = True
    while wU == True:
        print(condition)
        if condition: #checks the condition
            output
            wU = False
        time.sleep(1) #waits 60s for preformance

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
