from tkinter import *


class GUI:
    server = None

    def __init__(self, master):
        self.root = master
        self.player_name = ["foo", "bar", "baz", "foo", "bar",
                            "baz", "foo", "bar", "baz", "foo", "bar", "baz"]
        self.clue_player = ["foo", "bar", "baz", "foo", "bar",
                            "baz", "foo", "bar", "baz", "foo", "bar", "baz"]
        self.chat_transcript = None
        self.text_player = None
        self.enter_text_widget = None
        self.text_clue = None
        self.join_button = None
        self.init_gui()

    def init_gui(self):
        self.root.title("Undercover")
        self.root.resizable(0, 0)
        self.root.geometry('700x550')


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
