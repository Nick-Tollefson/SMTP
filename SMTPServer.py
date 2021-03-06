"""
Course: ISTE 101 - Computer Problem Solving in the Network Domain II
Project: Final Project - SMTP Server
Description: The SMTP Server, which is multi-threaded and can route mail to any inbox or SMTP server within the course
Authors: Tyler, Nick, Kyle, and Peter
Date: 05/14/2015
"""

import socket, os, threading, time, calendar

print "----SMTP SERVER ONLINE | FQDN: " + socket.getfqdn() + "----"

def SMTPServer(connection, address, checkingClient, QNumber):

    users = ["Peter", "Nick", "Tyler", "Kyle"]
    message = ["time","to","from","subject","body","EncryptionFlag"]

    if(checkingClient == True):

        user = connection.recv(1024)
        print "C: " + user + " (This is the user trying to connect)"

        if(user in users):

            print "\n*NOTICE*: A client [" + user + "] has logged into the server\n"

            readingInbox = open(str(user) + "-inbox.txt", "r")

            for eachLine in readingInbox:

                connection.sendall(str(eachLine.strip()))
                time.sleep(0.3)

            readingInbox.close()

        else:

            connection.sendall("535 Authentication Cred. Invalid")
            print "S: 535 Authentication Cred. Invalid"
            connection.close()
            return None

    else:

        print "*\nNOTICE*: a relay server has logged into the server\n"


    connection.sendall("220 " + str(socket.getfqdn()) + " ESMTP Postfix")
    print "S: " + "220 " + str(socket.getfqdn()) + " ESMTP Postfix"


    userInfo = connection.recv(1024)
    message[0] = str(time.strftime("%a, %d %b %Y %X"))
    clientHello = userInfo.split(" ")

    if(len(clientHello) == 1):

        if(clientHello[0] == "HELO"):

            print "C: " + userInfo
            connection.sendall("250 Hello stranger, I am glad to meet you")
            print "S: 250 Hello stranger, I am glad to meet you"

        elif(clientHello[0] == ""):

            print "user checked its mailbox and logged off..."
            connection.close()
            return None

        else:

            print "C: " + userInfo
            connection.sendall("500 Command Syntax Error - expecting HELO")
            print "S: 500 Command Syntax Error - expecting HELO"
            connection.close()
            return None

    else:

        if(clientHello[0] == "HELO"):
            connection.sendall("250 Hello " + clientHello[1] + ", I am glad to meet you")
            print "S: " + "250 Hello " + clientHello[1] + ", I am glad to meet you"

        else:
            connection.sendall("500 Command Syntax Error - expecting HELO")
            print "S: 500 Command Syntax Error - expecting HELO"
            connection.close()
            return None


    mailFrom = connection.recv(1024)
    print "C: " + mailFrom
    gettingFromAddr = mailFrom[mailFrom.find("<") + 1:mailFrom.find(">")]
    message[2] = str(gettingFromAddr)
    checkMailFrom = gettingFromAddr.split("@")

    try:

        socket.gethostbyname(checkMailFrom[1])

    except socket.gaierror:

        connection.sendall('500 Command Syntax Error - Bad "from" server domain')
        print 'S: 500 Command Syntax Error - Bad "from" server domain'
        connection.close()
        return None


    connection.sendall("250 OK")
    print "S: 250 OK"


    mailTo = connection.recv(1024)
    print "C: " + mailTo
    gettingToAddr = mailTo[mailTo.find("<") + 1:mailTo.find(">")]
    message[1] = str(gettingToAddr)
    checkMailTo = gettingToAddr.split("@")

    try:

        socket.gethostbyname(checkMailTo[1])

    except socket.gaierror:

        connection.sendall('500 Command Syntax Error - Bad "To" server domain')
        print 'S: 500 Command Syntax Error - Bad "To" server domain'
        connection.close()
        return None


    connection.sendall("250 OK")
    print "S: 250 OK"


    confirmMailStart = connection.recv(1024)
    print "C: " + confirmMailStart
    if(confirmMailStart == "DATA"):

        connection.sendall("354 End data with <CR><LF>.<CR><LF>")
        print "S: 354 End data with <CR><LF>.<CR><LF>"

    else:

        connection.sendall("500 Command Syntax Error - Expecting DATA")
        print "S: 500 Command Syntax Error - Expecting DATA"
        connection.close()
        return None


    done = False
    contentOfMail = []
    placeHolder = 1
    messageBody = ""

    while(not done):

        nextLine = connection.recv(1024)
        print "C: " + str(nextLine)

        if(nextLine == "." or nextLine == ".E"):

            connection.sendall("250 Ok: queued as " + str(QNumber))
            print "S: 250 Ok: queued as " + str(QNumber)

            ending = connection.recv(1024)
            print "C: " + ending

            if(ending == "QUIT"):

                connection.sendall("221 Bye")
                print "S: 221 Bye"

                connection.close()

                print "message transaction complete"

                message[4] = messageBody.rstrip()

                if(nextLine == "."):

                    message[5] = False
                    checkEncryption = False

                elif(nextLine == ".E"):

                    message[5] = True
                    checkEncryption = True

            else:

                connection.sendall("500 Command Syntax Error - Expecting QUIT")

            done = True

        else:

            contentOfMail.append(nextLine)

            if(placeHolder == 4):

                message[3] = nextLine[9:]

            elif(placeHolder == 3):

                message[0] = nextLine[6:]

            messageBody += nextLine + "\n"

            placeHolder += 1


    threading.Thread(target = MailMan, args = (mailFrom, mailTo, checkMailTo, contentOfMail, message, checkEncryption)).start()

def MailMan(mailFrom, mailTo, checkMailTo, contentOfMail, inboxMessage, checkEncryption):

    if(socket.gethostbyname(checkMailTo[1]) != socket.gethostbyname(socket.gethostname())):

        save_path = os.getcwd() + "\\" + "Other"

        completeName = os.path.join(save_path, str(calendar.timegm(time.gmtime())) + ".txt")

        writingMessage = open(completeName, "w")

        for eachLine in contentOfMail:

            writingMessage.write(eachLine)


        print "***Relay Process Initiating***"

        HOST = socket.gethostbyname(checkMailTo[1])
        PORT = 44444
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))


        serverHello = s.recv(1024)
        checkServerHello = serverHello.split(" ")

        if(checkServerHello[0] == "220"):

            print "S(them): " + serverHello

        else:

            print "S(them): " + serverHello
            s.close()
            return None


        s.sendall("HELO " + socket.getfqdn())
        time.sleep(0.5)
        print "C(us): HELO " + socket.getfqdn()


        serverConfirm = s.recv(1024)
        checkServerConfirm = serverConfirm.split(" ")

        if(checkServerConfirm[0] == "250"):

            print "S(them): " + serverConfirm

        else:

            print "S(them): " + serverConfirm
            s.close()
            return None


        s.sendall(mailFrom)
        time.sleep(0.5)
        print "C(us): " + mailFrom
        mailFromOk = s.recv(1024)
        checkMailFromOk = mailFromOk.split(" ")

        if(checkMailFromOk[0] == "250"):

            print "S(them): " + mailFromOk

        else:

            print "S(them): " + mailFromOk
            s.close()
            return None


        s.sendall(mailTo)
        time.sleep(0.5)
        print "C(us): " + mailTo
        mailToOk = s.recv(1024)
        checkMailToOk = mailToOk.split(" ")

        if(checkMailToOk[0] == "250"):

            print "S(them): " + mailToOk

        else:

            print "S(them): " + mailToOk
            s.close()
            return None


        s.sendall("DATA")
        time.sleep(0.5)
        print "C(us): DATA"
        readyForData = s.recv(1024)
        checkReadyForData = readyForData.split(" ")

        if(checkReadyForData[0] == "354"):

            print "S(them): " + readyForData

        else:

            print "S(them): " + readyForData
            s.close()
            return None


        for eachLine in contentOfMail:

            s.sendall(eachLine)
            time.sleep(0.5)
            print "C(us): " + eachLine


        if(checkEncryption == False):
            s.sendall(".")
            print "C(us): ."

        elif(checkEncryption == True):
            s.sendall(".E")
            print "C(us): .E"

        time.sleep(0.5)


        endOfMessage = s.recv(1024)
        checkEndOfMessage = endOfMessage.split(" ")

        if(checkEndOfMessage[0] == "250"):

            print "S(them): " + endOfMessage

        else:

            print "S(them): " + endOfMessage
            s.close()
            return None


        s.sendall("QUIT")
        time.sleep(0.5)
        print "C(us): QUIT"


        byeBye = s.recv(1024)
        checkByeBye = byeBye.split(" ")

        if(checkByeBye[0] == "221"):

            print "S(them): " + byeBye
            s.close()
            print "[mail was successfully relayed]"

        else:

            print "S(them): " + byeBye
            s.close()
            print "[mail did not relay properly]"

    else:

        save_path = os.getcwd() + "\\" + checkMailTo[0]

        completeName = os.path.join(save_path, str(calendar.timegm(time.gmtime())) + ".txt")

        writingMessage = open(completeName, "w")

        for eachLine in contentOfMail:

            writingMessage.write(eachLine + "\n")


        writingMessage.close()

        writingToInbox = open(checkMailTo[0] + "-inbox.txt", "a")
        writingToInbox.write(str(inboxMessage) + "\n")
        writingToInbox.close()

    contentOfMail[:] = []

#--------------------------------------------------------------------------------------------------------------------

def clientConnection():

    print "Now listening for clients..."
    queueNumber = 0
    isClient = True
    HOST = ''
    PORT = 33333
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(1)

    finished = False

    while (not finished):

        conn, addr = s.accept()
        print "\n" + str(addr[0]) + ":" + str(addr[1]) + " has connected (this is a client)"
        threading.Thread(target = SMTPServer, args = (conn, addr, isClient, queueNumber)).start()
        queueNumber += 1


def serverConnection():

    print "Now listening for relay servers..."
    queueNumber = 0
    isClient = False
    HOST = ''
    PORT = 44444
    relay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay.bind((HOST,PORT))
    relay.listen(1)

    finished = False

    while (not finished):

        conn, addr = relay.accept()
        print "\n" + str(addr[0]) + ":" + str(addr[1]) + " has connected (this is a server)"
        threading.Thread(target = SMTPServer, args = (conn, addr, isClient, queueNumber)).start()
        queueNumber += 1



threading.Thread(target = clientConnection).start()
threading.Thread(target = serverConnection).start()
