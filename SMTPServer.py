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