__author__ = 'Kyle Haltenhoff'

from Tkinter import *

inbox = Tk()
inbox.title('Inbox')

def clicked ():
    pass

inboxMessages = Listbox(inbox, height=10)
inboxMessages.pack()

message1 = inboxMessages.insert(END, 'test')

compose = Button(master=inbox, text="Compose Message", command=clicked)
compose.pack()

inbox.minsize(width=300, height=300)
inbox.resizable(width=FALSE, height=FALSE)
inbox.mainloop()

'''
from Tkinter import *

root = Tk()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root)
listbox.pack()

for i in range(100):
    listbox.insert(END, i)

# attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

mainloop()
'''