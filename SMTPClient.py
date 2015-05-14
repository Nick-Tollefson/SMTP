"""
Course: ISTE 101 - Computer Problem Solving in the Network Domain II
Project: Final Project - SMTP Client
Description: The SMTP Client which can connect to any SMTP Server within the course and send it an e-mail.
Authors: Tyler, Nick, Kyle, and Peter
Date: 05/14/2015
"""

from Tkinter import *
import socket, time
import ast

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

                print "\nS: " + InboxOr220
                done = True

            else:

                message = ast.literal_eval(InboxOr220)

                if len(message) == 5:

                    message.append(False)

                if message[5] is True:

                    message[0] = self.decryption(message[0])
                    message[4] = self.decryption(message[4])
                    message[3] = self.decryption(message[3])

                post_office.append(message)

        mailbox(post_office, self)

    def sendEmail(self, messageSource, messageDestination, messageSubject, messageBodyList, isEncrypted):

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


        if(isEncrypted == True):

            self.s.sendall(self.encryption('From: "' + self.clientName + '" <' + messageSource + ">"))
            print "C: " + self.encryption('From: "' + self.clientName + '" <' + messageSource + ">")
            time.sleep(0.5)

            name = messageDestination.split("@")
            self.s.sendall(self.encryption('To: "' + name[0] + '" <' + messageDestination + ">"))
            print "C: " + self.encryption('To: "' + name[0] + '" <' + messageDestination + ">")
            time.sleep(0.5)

            self.s.sendall(self.encryption("Date: " + str(time.strftime("%a, %d %b %Y %X"))))
            print "C: " + self.encryption("Date: " + str(time.strftime("%a, %d %b %Y %X")))
            time.sleep(0.5)

            self.s.sendall(self.encryption("Subject: " + messageSubject))
            print "C: " + self.encryption("Subject: " + messageSubject)
            time.sleep(0.5)

            for eachLine in messageBodyList:

                self.s.sendall(self.encryption(eachLine))
                time.sleep(0.5)
                print "C: " + self.encryption(eachLine)

            self.s.sendall(".E")
            print "C: .E"


        elif(isEncrypted == False):

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
            print "C: ."


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
            print "[mail was successfully sent to the server]"
            self.s.close()

        else:

            print "S: " + byeBye
            print "[mail did not make it to server properly]"
            self.s.close()

    def encryption(self, line, off_set = 1):

        finalMessage = ""

        for eachline in line:

            for eachChar in eachline:

                decimalValue = ord(eachChar)

                newValue = decimalValue - 32

                step4 = newValue + off_set

                if(step4 > 95):

                    step4 -= 95

                finalValue = step4 + 32
                finalMessage += chr(finalValue)

        return finalMessage

    def decryption(self, line, off_set = 1):

        finalDecryptedValue = ""

        for eachline in line:

            for eachChar in eachline:

                if(ord(eachChar) == 10):

                   finalDecryptedValue += eachChar

                else:

                    newDecimalValue = ord(eachChar)

                    newNewValue = newDecimalValue - 32

                    KeyOutput = newNewValue - off_set

                    if(KeyOutput < 0):

                        KeyOutput += 95

                    KeyOutput += 32

                    finalDecryptedValue += chr(KeyOutput)

        return finalDecryptedValue


#--------------------------------------------------------------------------------------------------------------------



def mailbox(post_office, smtp):

    def OnDouble(event):

        widget = event.widget

        selection = widget.curselection()

        T.delete(1.0, 'end')
        T.insert(END, messagelist[int(selection[0])])

    def closing():
        win.destroy()


    global messagelist
    messagelist = []

    win = Toplevel(loginWindow)
    win.title("Post Office")

    frame1 = Frame(win)
    frame1.pack()

    frame3 = Frame(win)
    frame3.pack()

    scroll = Scrollbar(frame3, orient=VERTICAL)

    select = Listbox(frame3, yscrollcommand=scroll.set, height=6,width=70)


    for message in post_office:

        select.insert(END," | Subject: " + message[3] +  " |From: " + '{:<20}'.format(message[2]) + \
                      "Date: " + '{:<20}'.format(message[0]))
        messagelist.append(message[4])


    select.bind("<Double-Button-1>", OnDouble)
    scroll.config(command=select.yview)

    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)

    frame4 = Frame(win)

    S = Scrollbar(frame4)
    T = Text(frame4, height = 15, width = 70)

    S.pack(side = RIGHT, fill = Y)
    T.pack(side = LEFT, fill = Y)

    S.config(command = T.yview)
    T.config(yscrollcommand = S.set)

    T.insert(END, "")

    frame4.pack()

    testingButton = Button(win, text="Logout", command = closing)
    testingButton.pack()

    win.after(sendingMessage(smtp))

    win.mainloop()



#--------------------------------------------------------------------------------------------------------------------



def sendingMessage(SMTP):

    def sendEncrypted():
        sendEmail(True)

    def sendUnencrypted():
        sendEmail(False)

    def sendEmail(isEncrypted):

        toID = toText.get()
        subjectID = subjectText.get()
        fromID = username + "@" + serverID
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

        SMTP.sendEmail(fromID, toID, subjectID, bodyOfMessage, isEncrypted)

    def logOut():
        message.destroy()


    message = Tk()
    message.title("Compose Message")

    fromLabel = Label(message, padx = 30, pady = 10, text = "From: " + username + "@" + serverID)
    toLabel = Label(message, padx = 30, pady = 10, text = "To: ")
    toText = Entry(message)
    subjectLabel = Label(message, padx = 30, pady = 10, text = "Subject: ")
    subjectText = Entry(message)
    scrollBar = Scrollbar(message)
    textBox = Text(message, height = 20, width = 40)
    encryptButton = Button(message, text = "Send Encrypted", command = sendEncrypted)
    dontEncryptButton = Button(message, text = "Send Without Encryption", command = sendUnencrypted)
    logOutButton = Button(message, text = "Logout", command = logOut)

    fromLabel.pack()
    toLabel.pack()
    toText.pack()
    subjectLabel.pack()
    subjectText.pack()
    scrollBar.pack(side = RIGHT, fill = Y)
    textBox.pack()
    scrollBar.config(command = textBox.yview)
    encryptButton.pack()
    dontEncryptButton.pack()
    logOutButton.pack()

    message.mainloop()



#--------------------------------------------------------------------------------------------------------------------



def ConnectToServer():

    global username
    global serverID

    serverID = serverText.get()
    username = userText.get()

    SMTPconnection = SMTP(serverID, username)

    try:

        SMTPconnection.logIntoServerAndReceiveInbox()
        loginWindow.destroy()

    except TclError:

        pass



loginWindow = Tk()
loginWindow.title("Login")

serverLabel = Label(loginWindow, padx = 30, pady = 10, text = "Server ID: ")
serverText = Entry(loginWindow)
userLabel = Label(loginWindow, padx = 30, pady = 10, text = "Username: ")
userText = Entry(loginWindow)
loginButton = Button(loginWindow, text = "Login", command = ConnectToServer)

serverLabel.pack()
serverText.pack()
userLabel.pack()
userText.pack()
loginButton.pack()

loginWindow.minsize(width=300, height=300)
loginWindow.resizable(width=FALSE, height=FALSE)

loginWindow.mainloop()
