from Tkinter import *
import socket, time
import ast

#--------------------------------------------------------------------------------------------------------------------

"""

"""



class SMTP:


    serverName = ""
    clientName = ""
    s = ""


    def __init__(self, serverName, clientName):

        self.serverName = serverName
        self.clientName = clientName


    def logIntoServerAndReceiveInbox(self):


        HOST = socket.gethostbyname(self.serverName)
        PORT = 33333
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s = s
        self.s.connect((HOST, PORT))

        s.sendall(self.clientName)

        done = False
        post_office = []
        while(not done):

            InboxOr220 = self.s.recv(1024)


            if(InboxOr220[:3] == "220"):

                print "S: " + InboxOr220
                done = True

            else:
                InboxOr220 = InboxOr220.split(",")
                post_office.append(InboxOr220)
        for line in post_office:
            print(line)
        mailbox(post_office)

    def sendEmail(self, messageSource, messageDestination, messageSubject, messageBodyList):


        self.s.sendall("HELO " + self.clientName)
        print "C: HELO " + self.clientName


        serverConfirm = self.s.recv(1024)
        checkServerConfirm = serverConfirm.split(" ")

        if(checkServerConfirm[0] == "250"):

            print "S: " + serverConfirm

        else:

            print "S: " + serverConfirm
            self.s.close()
            return None



        self.s.sendall("MAIL FROM:<" + messageSource + ">")
        print "C: MAIL FROM:<" + messageSource + ">"
        mailFromOk = self.s.recv(1024)
        checkMailFromOk = mailFromOk.split(" ")

        if(checkMailFromOk[0] == "250"):

            print "S: " + mailFromOk

        else:

            print "S: " + mailFromOk
            self.s.close()
            return None



        self.s.sendall("RCPT TO:<" + messageDestination + ">")
        print "C: RCPT TO:<" + messageDestination + ">"
        mailToOk = self.s.recv(1024)
        checkMailToOk = mailToOk.split(" ")

        if(checkMailToOk[0] == "250"):

            print "S: " + mailToOk

        else:

            print "S: " + mailToOk
            self.s.close()
            return None



        self.s.sendall("DATA")
        print "C: DATA"
        readyForData = self.s.recv(1024)
        checkReadyForData = readyForData.split(" ")

        if(checkReadyForData[0] == "354"):

            print "S: " + readyForData

        else:

            print "S: " + readyForData
            self.s.close()
            return None



        self.s.sendall('From: "' + self.clientName + '" <' + messageSource + ">")
        print 'C: From: "' + self.clientName + '" <' + messageSource + ">"
        time.sleep(0.5)



        name = messageDestination.split("@")
        self.s.sendall('To: "' + name[0] + '" <' + messageDestination + ">")
        print 'C: To: "' + name[0] + '" <' + messageDestination + ">"
        time.sleep(0.5)



        self.s.sendall("Date: " + str(time.strftime("%a, %d %b %Y %X")))
        print "C: Date: " + str(time.strftime("%a, %d %b %Y %X"))
        time.sleep(0.5)



        self.s.sendall("Subject: " + messageSubject)
        print "C: Subject: " + messageSubject
        time.sleep(0.5)



        for eachLine in messageBodyList:

            self.s.sendall(eachLine)
            time.sleep(0.5)
            print "C: " + eachLine



        self.s.sendall(".")
        endOfMessage = self.s.recv(1024)
        checkEndOfMessage = endOfMessage.split(" ")

        if(checkEndOfMessage[0] == "250"):

            print "S: " + endOfMessage

        else:

            print "S: " + endOfMessage
            self.s.close()
            return None



        self.s.sendall("QUIT")
        print "C: QUIT"



        byeBye = self.s.recv(1024)
        checkByeBye = byeBye.split(" ")

        if(checkByeBye[0] == "221"):

            print "S: " + byeBye
            self.s.close()

        else:

            print "S: " + byeBye
            self.s.close()
#--------------------------------------------------------------------------------------------------------------------

def mailbox(post_office):
    """
    message = ast.literal_eval(InboxOr220)
    print message
    print "+++++++++++++++++++++++++++++++++++++++"
    print "--- From: " + message[2] + " | To: " + message[1] + " | Subject: " + message[3] + \
          " | Date: " + message[0] + " ---"
    print message[4]

    print "+++++++++++++++++++++++++++++++++++++++"
    """
    def OnDouble(event):
        widget = event.widget
        selection = widget.curselection()
        T.delete(1.0, 'end')
        T.insert(END, messagelist[int(selection[0])])

    global messagelist
    messagelist = []

    win = Tk()
    win.title("Post Office")

    frame1 = Frame(win)
    frame1.pack()

    frame3 = Frame(win)
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6,width=70)

    for message in post_office:
        print(message[1])
        select.insert(END, "From: " + '{:<20}'.format(message[2]) + " | To: " + '{:<20}'.format(message[1]) + " | Subject: " + message[3])
        messagelist.append(message[4])
    select.bind("<Double-Button-1>", OnDouble)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)


    frame4 = Frame(win)
    S = Scrollbar(frame4)
    T = Text(frame4, height=15, width=70)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """HAMLET: To be, or not to be--that is the question: Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    T.insert(END, quote)
    frame4.pack()


    win.mainloop()

#--------------------------------------------------------------------------------------------------------------------
def sendingMessage(SMTP):

    def clicked():

        toID = toText.get()
        subjectID = subjectText.get()
        textMessage = textBox.get(1.0, 'end')

        lineOfText = ""
        bodyOfMessage = []

        for character in textMessage:

            if(character == "\n"):

                if(lineOfText == ""):

                    bodyOfMessage.append(" ")

                else:

                    bodyOfMessage.append(lineOfText)

                lineOfText = ""

            else:

                lineOfText += character


        SMTP.sendEmail(username + "@" + serverID, toID, subjectID, bodyOfMessage)



    def logOut():

        message.destroy()


    message = Tk()
    message.title("Compose Message")

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

#--------------------------------------------------------------------------------------------------------------------
def clicked():

    global username
    global serverID
    serverID = serverText.get()
    username = userText.get()

    SMTPconnection = SMTP(serverID, username)
    SMTPconnection.logIntoServerAndReceiveInbox()

    loginWindow.destroy()
    sendingMessage(SMTPconnection)


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



#--------------------------------------------------------------------------------------------------------------------

def sendingMessage(SMTP):

    def clicked():

        toID = toText.get()
        subjectID = subjectText.get()
        textMessage = textBox.get(1.0, 'end')

        lineOfText = ""
        bodyOfMessage = []

        for character in textMessage:

            if(character == "\n"):

                if(lineOfText == ""):

                    bodyOfMessage.append(" ")

                else:

                    bodyOfMessage.append(lineOfText)

                lineOfText = ""

            else:

                lineOfText += character


        SMTP.sendEmail(username + "@" + serverID, toID, subjectID, bodyOfMessage)



    def logOut():

        message.destroy()


    message = Tk()
    message.title("Compose Message")

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

#--------------------------------------------------------------------------------------------------------------------

def clicked():

    global username
    global serverID
    serverID = serverText.get()
    username = userText.get()

    SMTPconnection = SMTP(serverID, username)
    SMTPconnection.logIntoServerAndReceiveInbox()

    loginWindow.destroy()
    sendingMessage(SMTPconnection)


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

#--------------------------------------------------------------------------------------------------------------------
