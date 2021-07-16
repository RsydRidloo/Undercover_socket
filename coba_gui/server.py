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
x = 0
y = 1
idx = 0
old_remaining_client = 0

def clientthread(conn, addr):
    global turn
    global role_of_clients
    global remaining_clients
    global i
    global x
    global y
    global idx
    global old_remaining_client
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
                    if x == 0:
                        index = random.randint(0, 4)
                        x=1
                    if number_of_clients > 5:
                        role_of_clients = numpy.ones(number_of_clients)
                        role_of_clients[(number_of_clients-2):] = 2
                        random.shuffle(role_of_clients)
                        print(role_of_clients)
                    else:
                        role_of_clients = numpy.ones(number_of_clients)
                        role_of_clients[(number_of_clients-1):] = 2
                        random.shuffle(role_of_clients)
                        print(role_of_clients)
                    role_of_clients = role_of_clients.tolist()
                    for clients in list_of_clients:
                        print(clients)
                        if role_of_clients[i] == 2:
                            word_to_send = "word/" + undercover_words[index]
                        else:
                            word_to_send = "word/" + civillian_words[index]
                        print(word_to_send)
                        clients.send(word_to_send.encode())
                        i = i + 1
                    sendToAll("clue_turn/" + remaining_clients[0], conn)
                    # print(name_of_clients[0])
                elif data.split("/")[0] == "clue":
                    # if y == 0:                        
                    #     amount_of_client = len(remaining_clients)
                    # else:
                    #     amount_of_client = old_remaining_client
                    amount_of_client = clientCounter(len(name_of_clients), y)
                    turn += 1
                    idx += 1
                    print(turn)
                    broadcast("clue_send/" + data.split("/")[1], conn)
                    if turn - amount_of_client == 0:
                        y += 1
                        idx = 0
                        sendToAll("discussion/", conn)
                        time.sleep(10)
                        sendToAll("vote_time/", conn)
                    else:
                        sendToAll("clue_turn/" + remaining_clients[idx], conn)
                elif data.split("/")[0] == "vote":
                    voted_client.append(data.split("/")[1])
                    print(voted_client)
                    print(len(remaining_clients))
                    print(len(voted_client))
                    if len(remaining_clients) == len(voted_client):
                        name = most_frequent(voted_client)
                        # old_remaining_client = len(remaining_clients) + len(remaining_clients) - 1
                        index = name_of_clients.index(name)
                        remaining_clients.remove(name)
                        print(name)
                        print(index)
                        print(role_of_clients)
                        print(type(remaining_clients))
                        print(type(role_of_clients))
                        if(role_of_clients[index] == 2):
                            role = "undercover"
                        else:
                            role = "civillian"
                        print(role)
                        print(type(role_of_clients))
                        role_of_clients.pop(index)
                        most_voted_client = "mostVoted/" + role + "/" + name
                        print(most_voted_client)
                        sendToAll(most_voted_client, conn)
                        if len(remaining_clients)<3:
                            print("test1")
                            if 2 not in role_of_clients:
                                sendToAll("civillian_win/", conn)
                                print("civillian_win")
                            else:
                                sendToAll("undercover_win/", conn)
                                print("undercover_win")
                            break
                        if 2 not in role_of_clients:
                            sendToAll("civillian_win/", conn)
                            print("civillian_win")
                            break
                        # del remaining_roles[index]
                        voted_client.clear()
                        sendToAll("clue_turn/" + remaining_clients[0], conn)
                else:
                    # print(data.split("/")[0] + ' : ' + data.partition('/')[2])
                    message_to_send = data.split(
                        "/")[0] + ' : ' + data.partition('/')[2]
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def clientCounter(client, index) :
    result = client + (index-1)*(client-1) + ((index-1)*(index-2)*(-1))/2
    return result

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
