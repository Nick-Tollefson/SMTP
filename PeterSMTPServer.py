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

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")

    connection.sendall("250 OK")


    mailTo = connection.recv(1024)
    global checkMailTo
    checkMailTo = mailTo.split("@")

    try:

        socket.gethostbyname(checkMailTo[1])

    except socket.gaierror:

        connection.sendall("500 Command Syntax Error")


    connection.sendall("250 OK")




    confirmMailStart = connection.recv(1024)
    if(confirmMailStart == "DATA"):

        connection.sendall("354 End data with <CR><LF>.<CR><LF>")

    else:

        connection.sendall("500 Command Syntax Error")


    done = False
    global contentOfMail
    contentOfMail = []

    while(not done):

        nextLine = connection.recv(1024)

        if(nextLine == "."):

            connection.sendall("250 Ok: queued as 12345")

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
    lock.release()


#--------------------------------------------------------------------

finished = False
i = 0
while (not finished):

    conn, addr = s.accept()
    threading.Thread(target = SMTPServer, args = (conn, addr)).start()

    if(i == 0):

        threading.Thread(target = MailMan).start()

    i = 1
#