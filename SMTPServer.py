import socket, os, threading, time, calendar

print "----SERVER ONLINE AT: " + socket.getfqdn() + "----"

def SMTPServer(connection, address):

    #added for the groups, this is the first message before the server sends its openning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            message
    user = connection.recv(1024)
    print "logged in as " + user

    connection.sendall("220 " + str(socket.getfqdn()) + " ESMTP Postfix")


    userInfo = connection.recv(1024)
    clientHello = userInfo.split(" ")

    if(clientHello[0] == "HELO"):

        connection.sendall("250 Hello " + clientHello[1] + ", I am glad to meet you")

    else:

        connection.sendall("500 Command Syntax Error")



    mailFrom = connection.recv(1024)
    gettingFromAddr = mailFrom[mailFrom.find("<") + 1:mailFrom.find(">")]
    checkMailFrom = gettingFromAddr.split("@")

    try:

        socket.gethostbyname(checkMailFrom[1])
        print checkMailFrom[1]

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")
        connection.close()
        return None

    connection.sendall("250 OK")



    mailTo = connection.recv(1024)
    gettingToAddr = mailTo[mailTo.find("<") + 1:mailTo.find(">")]
    checkMailTo = gettingToAddr.split("@")

    try:

        socket.gethostbyname(checkMailTo[1])

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")
        connection.close()


    connection.sendall("250 OK")



    confirmMailStart = connection.recv(1024)
    if(confirmMailStart == "DATA"):

        connection.sendall("354 End data with <CR><LF>.<CR><LF>")

    else:

        connection.sendall("500 Command Syntax Error")



    done = False
    contentOfMail = []

    while(not done):

        nextLine = connection.recv(1024)

        if(nextLine == "."):

            connection.sendall("250 Ok: queued as 12345")

            ending = connection.recv(1024)
            if(ending == "QUIT"):

                connection.sendall("221 Bye")
                connection.close()
                print "message transaction complete"

            done = True

        else:

            contentOfMail.append(nextLine + "\n")


    threading.Thread(target = MailMan, args = (checkMailTo, contentOfMail)).start()



def MailMan(checkMailTo,contentOfMail):

    #change this to check To server vs current running server
    if(socket.gethostbyname(checkMailTo[1]) != socket.gethostbyname(socket.gethostname())):

        print "it made it here"

        save_path = os.getcwd() + "\\" + "Other"

        completeName = os.path.join(save_path, str(calendar.timegm(time.gmtime())) + ".txt")

        writingMessage = open(completeName, "w")

        for eachLine in contentOfMail:

            writingMessage.write(eachLine)



    else:

        save_path = os.getcwd() + "\\" + checkMailTo[0]

        completeName = os.path.join(save_path, str(calendar.timegm(time.gmtime())) + ".txt")

        writingMessage = open(completeName, "w")

        for eachLine in contentOfMail:

            writingMessage.write(eachLine)


        """
        HOST = socket.gethostbyname(checkMailTo[1])
        PORT = 44444
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = s
        s.connect((HOST, PORT))

        #start with a username
        s.sendall(socket.gethostname())

        serverHello = s.recv(1024)
        checkServerHello = serverHello.split(" ")

        if(checkServerHello[0] == "220"):

            print "S: " + serverHello

        else:

            print "S: " + serverHello
            s.close()
            return None



        s.sendall("HELO " + socket.getfqdn())
        print "C: HELO " + socket.getfqdn()


        serverConfirm = s.recv(1024)
        checkServerConfirm = serverConfirm.split(" ")

        if(checkServerConfirm[0] == "250"):

            print "S: " + serverConfirm

        else:

            print "S: " + serverConfirm
            s.close()
            return None



        s.sendall("MAIL FROM:<" + messageSource + ">")
        print "C: MAIL FROM:<" + messageSource + ">"
        mailFromOk = s.recv(1024)
        checkMailFromOk = mailFromOk.split(" ")

        if(checkMailFromOk[0] == "250"):

            print "S: " + mailFromOk

        else:

            print "S: " + mailFromOk
            s.close()
            return None



        s.sendall("RCPT TO:<" + messageDestination + ">")
        print "C: RCPT TO:<" + messageDestination + ">"
        mailToOk = s.recv(1024)
        checkMailToOk = mailToOk.split(" ")

        if(checkMailToOk[0] == "250"):

            print "S: " + mailToOk

        else:

            print "S: " + mailToOk
            s.close()
            return None



        s.sendall("DATA")
        print "C: DATA"
        readyForData = s.recv(1024)
        checkReadyForData = readyForData.split(" ")

        if(checkReadyForData[0] == "354"):

            print "S: " + readyForData

        else:

            print "S: " + readyForData
            s.close()
            return None



        s.sendall('From: "' + clientName + '" <' + messageSource + ">")
        print 'C: From: "' + clientName + '" <' + messageSource + ">"
        time.sleep(0.5)



        name = messageDestination.split("@")
        s.sendall('To: "' + name[0] + '" <' + messageDestination + ">")
        print 'C: To: "' + name[0] + '" <' + messageDestination + ">"
        time.sleep(0.5)



        s.sendall("Date: " + str(time.strftime("%a, %d %b %Y %X")))
        print "C: Date: " + str(time.strftime("%a, %d %b %Y %X"))
        time.sleep(0.5)



        s.sendall("Subject: " + messageSubject + "\n")
        print "C: Subject: " + messageSubject
        time.sleep(0.5)



        for eachLine in messageBodyList:

            s.sendall(eachLine)
            time.sleep(0.5)
            print "C: " + eachLine



        s.sendall(".")
        endOfMessage = s.recv(1024)
        checkEndOfMessage = endOfMessage.split(" ")

        if(checkEndOfMessage[0] == "250"):

            print "S: " + endOfMessage

        else:

            print "S: " + endOfMessage
            s.close()
            return None



        s.sendall("QUIT")
        print "C: QUIT"



        byeBye = s.recv(1024)
        checkByeBye = byeBye.split(" ")

        if(checkByeBye[0] == "221"):

            print "S: " + byeBye
            s.close()

        else:

            print "S: " + byeBye
            .s.close()

        """

    writingMessage.close()
    contentOfMail[:] = []

#--------------------------------------------------------------------------------------------------------------------

def clientConnection():

    print "client socket started"
    HOST = ''
    PORT = 33333
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(1)
    global users
    users = ["Peter", "Nick", "Tyler", "Kyle"]

    finished = False

    while (not finished):

        conn, addr = s.accept()
        print addr
        print str(addr[0]) + ":" + str(addr[1]) + " has connected (this is a client)"
        threading.Thread(target = SMTPServer, args = (conn, addr)).start()


def serverConnection():

    print "relay socket started"
    HOST = ''
    PORT = 44444
    relay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay.bind((HOST,PORT))
    relay.listen(1)
    global users
    users = ["Peter", "Nick", "Tyler", "Kyle"]

    finished = False

    while (not finished):

        conn, addr = relay.accept()
        print str(addr[0]) + ":" + str(addr[1]) + " has connected (this is a server)"
        threading.Thread(target = SMTPServer, args = (conn, addr)).start()




threading.Thread(target = clientConnection).start()
threading.Thread(target = serverConnection).start()