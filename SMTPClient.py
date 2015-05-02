from Tkinter import *
import socket, time

#--------------------------------------------------------------------------------------------------------------------

class SMTP:


    serverName = ""
    clientName = ""
    s = ""


    def __init__(self, serverName, clientName):

        self.serverName = serverName
        self.clientName = clientName



    def isAllowed(self):

        users = ["Peter", "Nick", "Tyler", "Kyle"]

        if(self.clientName in users):

            return True

        else:

            return False



    def sendEmail(self, messageSource, messageDestination, messageSubject, messageBodyList):


        HOST = socket.gethostbyname(self.serverName)
        PORT = 33333
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s = s
        self.s.connect((HOST, PORT))

        #start with a username
        s.sendall(self.clientName)

        serverHello = self.s.recv(1024)
        checkServerHello = serverHello.split(" ")

        if(checkServerHello[0] == "220"):

            print "S: " + serverHello

        else:

            print "S: " + serverHello
            self.s.close()
            return None



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



        self.s.sendall("Subject: " + messageSubject + "\n")
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

def sendingMessage(testing):

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


        testing.sendEmail(username + "@" + serverID, toID, subjectID, bodyOfMessage)



    def logOut():

        message.destroy


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

    test = SMTP(serverID, username)

    loginWindow.destroy()
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

#--------------------------------------------------------------------------------------------------------------------