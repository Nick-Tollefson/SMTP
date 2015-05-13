from Tkinter import *
import socket, time
import ast

#--------------------------------------------------------------------------------------------------------------------
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

        while(not done):

            InboxOr220 = self.s.recv(1024)

            if(InboxOr220[:3] == "220"):

                print "\nS: " + InboxOr220
                done = True

            else:

                message = ast.literal_eval(InboxOr220)
                print "\n\n"
                print str(message)

                if(message[5] == True):

                    message[4] = self.decryption(message[4])
                    message[3] = self.decryption(message[3])

                print "--- " + message[2] +  " | " + message[1] + " | " + message[3] + \
                      " | Date: " + message[0] + " | Encryption: " + str(message[5]) + " ---"
                print message[4]


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


#----------------------------------------------------------------------------------------------------------
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
#---------------------------------------------------------

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

def sendingMessage(SMTP):

    def clicked():

        toID = toText.get()
        subjectID = subjectText.get()

        textMessage = textBox.get(1.0, 'end')

        lineOfText = ""
        bodyOfMessage = [] #what needs to be encrypted

        for character in textMessage:

            if(character == "\n"):

                if(lineOfText == ""):

                    bodyOfMessage.append(" ")

                else:

                    bodyOfMessage.append(lineOfText)

                lineOfText = ""

            else:

                lineOfText += character


        #----------------------------------------------
        isEncrypted = False

        if(flag.get() == 1):

            print "send encrypted"

            isEncrypted = True


        elif(flag.get() == 0):

            print "send not encrypted"

            isEncrypted = False
        #----------------------------------------------



        SMTP.sendEmail(username + "@" + serverID, toID, subjectID, bodyOfMessage, isEncrypted)



    def logOut():

        #you were just missing the () Kyle :)
        message.destroy()


    def testing():

        test.destroy


    message = Tk()
    message.title("Compose Message")

#-----------------------------
    test = Tk()
    test.title("HAAW")
#-----------------------------


    fromLabel = Label(message, padx = 30, pady = 10, text="From: " + username + "@" + serverID)
    fromLabel.pack()

    toLabel = Label(message, padx = 30, pady = 10, text = "To: ")
    toLabel.pack()

    toText = Entry(message)
    toText.pack()

    subjectLabel = Label(message, padx = 30, pady = 10, text = "Subject: ")
    subjectLabel.pack()

    subjectText = Entry(message)
    subjectText.pack()

    scrollBar = Scrollbar(message)
    textBox = Text(message, height=20, width=40)
    scrollBar.pack(side=RIGHT, fill=Y)
    textBox.pack()
    scrollBar.config(command=textBox.yview)


#----------------------------------------------------- new encryption stuff
    flag = IntVar()

    encrypted = Radiobutton(message, text = "Encrypted", variable = flag, value = 1)
    encrypted.pack()

    notEncrypted = Radiobutton(message, text = "Not Encrypted", variable = flag, value = 0)
    notEncrypted.pack()
#-----------------------------------------------------


    sendButton = Button(master=message, text="Send", command=clicked)
    sendButton.pack()

    logOutButton = Button(master=message, text="Logout", command=logOut)
    logOutButton.pack()


#-----------------------------
    exitInboxButton = Button(test, text = "Closes just this window, not whole program", command = testing)
    exitInboxButton.pack()

#-----------------------------

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
