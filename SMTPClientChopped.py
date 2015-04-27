import socket, time

class SMTP:

    serverName = ""
    clientName = ""
    s = ""

    def __init__(self, serverName, clientName):

        self.serverName = serverName
        self.clientName = clientName

        HOST = socket.gethostbyname(self.serverName)
        PORT = 33333
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        self.s = s

        serverHello = s.recv(1024)
        print "\n" + "S: " + serverHello

        s.sendall("HELO " + self.clientName)
        print "C: HELO " + self.clientName

        serverConfirm = s.recv(1024)
        print "S: " + serverConfirm


    def sendEmail(self, messageSource, messageDestination, messageSubject, messageBody):


        self.s.sendall(messageSource)
        print "C: MAIL FROM:<" + messageSource + ">"

        print "S: " + str(self.s.recv(1024))

        self.s.sendall(messageDestination)
        print "C: RCPT TO:<" + messageDestination + ">"

        print "S: " + str(self.s.recv(1024))

        self.s.sendall("DATA")
        print "C: DATA"

        print "S: " + str(self.s.recv(1024))

        self.s.sendall('From: "' + self.clientName + '" <' + messageSource + ">")
        self.s.recv(1024)

        name = messageDestination.split("@")
        self.s.sendall('To: "' + name[0] + '" <' + messageDestination + ">")
        self.s.recv(1024)

        self.s.sendall("Date: " + str(time.strftime("%a, %d, %b, %Y, %H:%M:%S")))
        self.s.recv(1024)

        self.s.sendall("Subject: " + messageSubject + "\n")
        self.s.recv(1024)

        self.s.sendall(messageBody)
        self.s.recv(1024)

        self.s.sendall(".")
        print "S: " + str(self.s.recv(1024))

        self.s.sendall("QUIT")
        print "C: QUIT"

        print "S: " + str(self.s.recv(1024))
        self.s.close()
