from tkinter import *
import socket
import select
import sys
from threading import Thread


class GUI:
    server = None

    def __init__(self, master):
        self.root = master
        self.player_name = []
        self.radio_button = []
        self.clue_player = ["foo", "bar", "baz", "foo", "bar",
                            "baz", "foo", "bar", "baz", "foo", "bar", "baz"]
        self.chat_transcript = None
        self.text_player = None
        self.word_label = None
        self.enter_text_widget = None
        self.text_clue = None
        self.join_button = None
        self.var = StringVar()
        self.view_word()
        self.init_socket()
        self.init_gui()
        self.thread_gui()

    def init_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('127.0.0.1', 8081))

    def init_gui(self):
        self.root.title("Undercover")
        self.root.resizable(0, 0)
        self.root.geometry('700x550')
        self.title_game()
        self.input_username()
        self.view_voting_box()
        self.view_chat_box()
        self.send_chat_box()
        self.input_clue()
        self.view_clue_box()
        self.start_game()

    def start_game(self):
        frame = Frame()
        Button(frame, height=1, width=10, command=self.on_start,
               text="Start").pack(side='left')
        frame.place(x=10, y=70)

    def thread_gui(self):
        # Thread(target=self.send_msg, args=(self.server,)).start()
        Thread(target=self.recv_msg, args=(self.server,)).start()

    def send_msg(self):
        sender_name = self.text_player.get()
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (sender_name + '/' + data).encode()
        to_chat_box = ('me' + ' : ' + data).encode()
        self.chat_transcript.insert('end', to_chat_box.decode() + '\n')
        self.chat_transcript.yview(END)
        self.server.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def recv_msg(self, so):
        while True:
            buffer = so.recv(2048)
            if not buffer:
                break
            message = buffer.decode()
            if message.split("/")[0] == "word":
                self.chat_transcript.insert(
                    'end', "kata anda adalah " + message.split("/")[1] + '\n')
                word_player = message.split("/")[1]
                self.word_label.config(text="Kata : " + word_player)
                self.view_voting_box()
            elif message.split("/")[0] == "mostVoted":
                if message.split("/")[1] == self.text_player.get():
                    break
                index = self.player_name.index(message.split("/")[1])
                print(self.player_name[index])
                self.radio_button[index].configure(state=DISABLED)
                # for message.split("/")[1] in self.radio_button:
                #     self.radio_button.index(message.split("/")[1]).configure(state = DISABLED)
            else:
                if message.split("/")[0] == "joined":
                    self.player_name.append(message.split("/")[1])
                    message = message.split("/")[1] + " joined"
                self.chat_transcript.insert('end', message + '\n')
            self.chat_transcript.yview(END)
        so.close()

    def on_join(self):
        if len(self.text_player.get()) == 0:
            return
        self.text_player.config(state='disabled')
        self.server.send(("joined/" + self.text_player.get()).encode())

    def on_start(self):
        if len(self.text_player.get()) == 0:
            return
        self.text_player.config(state='disabled')
        self.server.send(("start/" + self.text_player.get()).encode())

    def on_enter_chat(self, event):
        if len(self.text_player.get()) == 0:
            return
        self.send_msg()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def title_game(self):
        frame = Frame()
        Label(frame, text="Undercover", font=(
            "Arial", 30), justify='center').pack()
        frame.place(x=250, y=0)

    def input_username(self):
        frame = Frame()
        self.text_player = Entry(frame, borderwidth=1, width=28)
        self.text_player.pack(side='left', padx=2)
        self.join_button = Button(
            frame, height=1, width=10, command=self.on_join, text="Join").pack(side='left', padx=2)
        frame.place(x=200, y=70)

    def view_chat_box(self):
        frame = Frame()
        Label(frame, text="Chat box", font=("Arial", 15),
              justify='left').pack(anchor='w', pady=5, padx=5)
        self.chat_transcript = Text(
            frame, width=40, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(
            frame, command=self.chat_transcript.yview, orient=VERTICAL)
        self.chat_transcript.config(yscrollcommand=scrollbar.set)
        self.chat_transcript.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.place(x=10, y=120)

    def view_clue_box(self):
        frame = Frame()
        Label(frame, text="Clue Box", font=(
            "Arial", 15), justify='left').pack(pady=5)
        Lb = Listbox(frame, width=10, height=10)
        Sb = Scrollbar(frame, orient="vertical")
        for listbox in self.clue_player:
            Lb.insert(END, listbox)
        Lb.config(yscrollcommand=Sb.set)
        Sb.config(command=Lb.yview)
        Lb.bind('<KeyPress>', lambda e: 'break')
        Lb.pack(side='left', padx=10)
        Sb.pack(side='right', fill='y')
        frame.place(x=420, y=120)

    def input_clue(self):
        frame = Frame()
        Label(frame, text="Input Clue :", font=(
            "Arial", 15), justify='left').pack(pady=5)
        self.text_clue = Text(frame, width=10, height=1, font=("Serif", 12))
        self.text_clue.pack()
        self.enter_text_widget.bind('<Return>', self.on_enter_chat)
        frame.place(x=550, y=120)

    def view_voting_box(self):
        frame = Frame()
        Label(frame, text="Voting",
              font=("Arial", 15), justify='left').pack()
        text = Text(frame, width=10, height=6, cursor="arrow")
        vsb = Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        text.bind('<KeyPress>', lambda e: 'break')
        text.pack(side='left', pady=15, padx=10)
        vsb.pack(side='left', fill='y', pady=15)
        for checkBoxName in self.player_name:
            c = Radiobutton(text, text=checkBoxName,
                            variable=self.var, value=checkBoxName)
            self.radio_button.append(c)
            text.window_create("end", window=c)
            text.insert("end", "\n")
        text.configure(state="disabled")
        Button(frame, height=1, width=10, command=self.on_choose,
               text="Pilih").pack(side='bottom')
        frame.place(x=420, y=350)

    def on_choose(self):
        self.server.send(("vote/"+self.var.get()).encode())
        # self.judul.config(text=self.var.get())

    def send_chat_box(self):
        frame = Frame()
        Label(frame, text="Masukan pesan :", font=("Arial", 12),
              justify='left').pack(anchor='nw', pady=(10, 2), padx=5)
        self.enter_text_widget = Text(
            frame, width=40, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15, padx=10)
        self.enter_text_widget.bind('<Return>', self.on_enter_chat)
        frame.place(x=10, y=350)

    def view_word(self):
        frame = Frame()
        self.word_label = Label(frame, text="Kata : -",
                                font=("Arial", 12), justify='left')
        self.word_label.pack()
        frame.place(x=550, y=10)

    def refresh(self):
        self.destroy()
        self.__init__()


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
