from Tkinter import *
from SMTPClientChopped import SMTP

def sendingMessage(testing):

    def clicked():

        toID = toText.get()
        subjectID = subjectText.get()
        textMessage = textBox.get(1.0, 'end')

        testing.sendEmail(username + "@" + serverID, toID, subjectID, textMessage)

    def logOut():

        message.destroy


    message = Tk()
    message.title("Compose Message")

    fromLabel = Label(master=message, padx = 30, pady = 10, text="From: ")
    fromLabel.pack()

    fromLabelControl = StringVar()
    fromLabelControl.set(username + "@" + serverID)
    fromMessage = Label(message, textvariable = fromLabelControl)
    fromMessage.pack()

    toLabel = Label(master=message, padx = 30, pady = 10, text="To: ")
    toLabel.pack()

    toText = Entry(master=message)
    toText.pack()

    subjectLabel = Label(master=message, padx = 30, pady = 10, text="Subject: ")
    subjectLabel.pack()

    subjectText = Entry(master=message)
    subjectText.pack()

    scrollBar = Scrollbar(message)
    textBox = Text(message, height=20, width=40)
    scrollBar.pack(side=RIGHT, fill=Y)
    textBox.pack()
    scrollBar.config(command=textBox.yview)

    sendButton = Button(master=message, text="Send", command=clicked)
    sendButton.pack()

    logOutButton = Button(master=message, text="Logout", command=logOut)
    logOutButton.pack()

    message.mainloop()

#-------------------------------------------------------------------------------

def clicked():

    global username
    global serverID
    serverID = serverText.get()
    username = userText.get()

    loginWindow.destroy()

    test = SMTP(serverID, username)
    sendingMessage(test)


loginWindow = Tk()
loginWindow.title("Login")

serverLabel = Label(master=loginWindow, padx = 30, pady = 10, text="Server ID: ")
serverLabel.pack()

serverText = Entry(master=loginWindow)
serverText.pack()

userLabel = Label(master=loginWindow, padx = 30, pady = 10, text="Username: ")
userLabel.pack()

userText = Entry(master=loginWindow)
userText.pack()

loginButton = Button(master=loginWindow, text="Login", command=clicked)
loginButton.pack()

loginWindow.minsize(width=300, height=300)
loginWindow.resizable(width=FALSE, height=FALSE)

loginWindow.mainloop()
