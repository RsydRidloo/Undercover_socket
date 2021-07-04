from tkinter import *
from tkinter import scrolledtext

window = Tk()

window.title("Undercover")
# window.geometry('350x400')
# window.resizable(0,0)

title = Label(window, text="Undercover", font=("Arial", 30), justify='center')
title.pack(anchor='n', pady=(10,20))

def retrieve_input():
    inputValue=textBox.get("1.0","end-1c")
    print(inputValue)

textBox=Text(window, height=1, width=40)
textBox.pack(side='top', anchor='nw', padx=5)
buttonCommit=Button(window, height=1, width=10, text="Main", justify=LEFT,
                    command=lambda: retrieve_input())
buttonCommit.pack(side='top', anchor='nw', pady=(0,7), padx=5)

lbl = Label(window, text="Chat box", font=("Arial", 15), justify='left')
lbl.pack(anchor='nw', pady=5, padx=5)

txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.pack(anchor='nw', padx=5)

lbl1 = Label(window, text="Masukan pesan :", font=("Arial", 12), justify='left')
lbl1.pack(anchor='nw' , pady=(10,2), padx=5)

fieldBox=Text(window, height=5, width=40)
fieldBox.pack(anchor='nw', pady=(0,10), padx=5)
# btn = Button(window, text='Stop', command=window.destroy)
# btn.grid(column=0,row=3)

window.mainloop()