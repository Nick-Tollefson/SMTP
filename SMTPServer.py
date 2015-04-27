import socket, os, threading

HOST = ''
PORT = 33333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
users = ["Peter", "Nick", "Tyler", "Kyle"]
lock = threading.Lock()

def SMTPServer(connection, address):

    lock.acquire()

    connection.sendall("220 " + str(socket.getfqdn()) + " ESMTP Postfix")

    userInfo = connection.recv(1024)
    searchName = userInfo.split(" ")

    if(searchName[1] in users):

        connection.sendall("250 Hello " + searchName[1] + ", I am glad to meet you")

    else:

        connection.sendall("ERROR")


    mailFrom = connection.recv(1024)
    checkMailFrom = mailFrom.split("@")

    try:

        socket.gethostbyname(checkMailFrom[1])
        connection.sendall("250 OK")

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")

    mailTo = connection.recv(1024)
    global checkMailTo
    checkMailTo = mailTo.split("@")

    try:

        socket.gethostbyname(checkMailTo[1])
        connection.sendall("250 OK")

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")

    confirmMailStart = connection.recv(1024)
    if(confirmMailStart == "DATA"):

        connection.sendall("354 End data with <CR><LF>.<CR><LF>")

    else:

        connection.sendall("500 Command Syntax Error")


    done = False
    global contentOfMail
    contentOfMail = []
    i = 1

    while(not done):

        nextLine = connection.recv(1024)
        print str(i) + " " + str(nextLine)

        if(nextLine == "."):

            connection.sendall("250 Ok: queued as 12345")
            print "it sent the OK queued"

            ending = connection.recv(1024)
            if(ending == "QUIT"):

                connection.sendall("221 Bye")
                connection.close()
                lock.release()

            done = True


        elif(nextLine == "_"):

            contentOfMail.append("\n")


        else:

            contentOfMail.append(nextLine + "\n")
            connection.sendall("I got code")

        i += 1

def MailMan():

    lock.acquire()

    if(checkMailTo[0] in users):

        save_path = os.getcwd() + "\\" + checkMailTo[0]

        completeName = os.path.join(save_path, "test.txt")

        writingMessage = open(completeName, "w")

    global contentOfMail
    for eachLine in contentOfMail:

        writingMessage.write(eachLine)


    writingMessage.close()
    contentOfMail[:] = []
    lock.release()


#--------------------------------------------------------------------

finished = False
i = 0
while (not finished):

    conn, addr = s.accept()
    print str(addr) + " has connected"
    threading.Thread(target = SMTPServer, args = (conn, addr)).start()
    threading.Thread(target = MailMan).start()

