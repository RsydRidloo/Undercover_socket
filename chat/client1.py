import socket
import select
import sys
from threading import Thread
from ftplib import FTP

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 8081))

name = "client1"

def send_msg(sock):
	while True:
		data = input()
		
		sock.send((name + ' ' + data).encode())
		sys.stdout.flush()

def recv_msg(sock):
	while True:
		data = sock.recv(2048)
		sys.stdout.write(data.decode() + '\n')

Thread(target=send_msg, args=(server,)).start()
# Thread(target=recv_msg, args=(server,)).start()

while True:
	sockets_list = [server]
	read_socket, write_socket, error_socket = select.select(sockets_list, [], [])
	for socks in read_socket:
		send_msg(socks)
		# if socks == server:
		# 	recv_msg(socks)
		# # else:
		# # 	send_msg(socks)

server.close()