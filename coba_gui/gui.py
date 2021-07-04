from tkinter import *
from tkinter import scrolledtext
import socket
import select
import sys
from threading import Thread
from ftplib import FTP

class GUI:
    server = None
    latest_chat = None

    def __init__(self, master):
        self.root = master
        # self.init_socket()
        self.init_gui()

    def init_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('127.0.0.1', 8081))

    def init_gui(self):
        self.root.title("Undercover")
        self.root.resizable(0, 0)
        self.title_game()
        self.username_player()
        self.view_chat_box()
        self.send_chat_box()

    def title_game(self):
        frame = Frame()
        Label(frame, text="Undercover", font=("Arial", 30), justify='center').pack()
        frame.pack()

    def username_player(self):
        frame = Frame()
        Text(frame, height=1, width=40).pack(side='top', anchor='nw', padx=5)
        Button(frame, height=1, width=10, text="Main", justify=LEFT).pack(side='top', anchor='nw', pady=(0,7), padx=5)
        frame.pack()

    def view_chat_box(self):
        frame = Frame()
        Label(frame, text="Chat box", font=("Arial", 15), justify='left').pack(anchor='nw', pady=5, padx=5)
        self.latest_chat = scrolledtext.ScrolledText(frame,width=40,height=10).pack(anchor='nw', padx=5)
        frame.pack()

    def send_chat_box(self):
        frame = Frame()
        Label(frame, text="Masukan pesan :", font=("Arial", 12), justify='left').pack(anchor='nw' , pady=(10,2), padx=5)
        Text(frame, height=5, width=40).pack(anchor='nw', padx=5)
        frame.pack(pady=(0,10))

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
