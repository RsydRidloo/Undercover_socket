from tkinter import *
from tkinter import scrolledtext
import socket
import select
import sys
from threading import Thread

class GUI:
    server = None
    latest_chat = None

    def __init__(self, master):
        self.root = master
        self.player_name = ["foo", "bar", "baz","foo", "bar", "baz","foo", "bar", "baz","foo", "bar", "baz"]
        self.clue_player = ["foo", "bar", "baz"]
        # self.init_socket()
        self.init_gui()

    def init_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('127.0.0.1', 8081))

    def init_gui(self):
        self.root.title("Undercover")
        self.root.resizable(0, 0)
        self.root.geometry('700x450')
        self.role_player = "undertaker"
        self.title_game()
        self.username_player()
        self.view_role()
        self.view_chat_box()
        self.send_chat_box()
        self.view_clue_box()
        self.view_voting()

    def title_game(self):
        frame = Frame()
        Label(frame, text="Undercover", font=("Arial", 30), justify='center').pack()
        frame.place(x=250, y=0)

    def username_player(self):
        frame = Frame()
        Text(frame, height=1, width=28).pack(side='left', padx=2)
        Button(frame, height=1, width=10, text="Start", justify=LEFT).pack(side='left', padx=2)
        frame.place(x=200, y=70)

    def view_chat_box(self):
        frame = Frame()
        Label(frame, text="Chat box", font=("Arial", 15), justify='left').pack(anchor='w',pady=5, padx=5)
        self.latest_chat = scrolledtext.ScrolledText(frame,width=40,height=10).pack(padx=5)
        frame.place(x=10, y=120)

    def send_chat_box(self):
        frame = Frame()
        Label(frame, text="Masukan pesan :", font=("Arial", 12), justify='left').pack(anchor='nw' , pady=(10,2), padx=5)
        Text(frame, height=5, width=40).pack(anchor='nw', padx=5)
        frame.place(x=10, y=300)

    def view_voting(self):
        frame = Frame(root, highlightbackground="black", highlightthickness=6, bd= 0)
        Label(frame, text="Voting", font=("Arial", 15), justify='left').pack(pady=5)
        text = Text(root, width=10, height=6, cursor="arrow")
        vsb = Scrollbar(root, command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        text.place(x=400, y=300)
        vsb.place(x=400, y=300)
        for checkBoxName in self.player_name:
            c = Checkbutton(text, text=checkBoxName)
            text.window_create("end", window=c)
            text.insert("end", "\n")
        text.configure(state="disabled")
        frame.place(x=400, y=300)

    def view_role(self):
        frame = Frame()
        Label(frame, text="Role : " + self.role_player, font=("Arial", 12), justify='left').pack()
        frame.place(x=550, y=10)


    def view_clue_box(self):
        frame = Frame()
        Label(frame, text="Clue Box", font=("Arial", 15), justify='left').pack(pady=5)
        Lb = Listbox(root)
        Lb.place(x=400, y=160)
        Sb = Scrollbar(orient="vertical",width=200)
        Sb.place(x=400, y=130)
        for listbox in self.clue_player:
            Lb.insert(END, listbox)
        Lb.config(yscrollcommand=Sb.set)
        Sb.config(command=Lb.yview)
        frame.place(x=400, y=120)

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
