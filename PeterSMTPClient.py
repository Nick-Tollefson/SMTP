import socket, threading, time

serverName = raw_input("Server: ")
clientName = raw_input("Name: ")

HOST = socket.gethostbyname(serverName)
PORT = 33333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

serverHello = s.recv(1024)
print "\n" + "S: " + serverHello

clientHelloBack = s.sendall("HELO " + clientName)
print "C: HELO " + clientName

serverConfirm = s.recv(1024)
print "S: " + serverConfirm

#-------------------------------------------------------
print"+~~~~~~~~~NEW MESSAGE~~~~~~~~~+"

messageSource = raw_input("From: ")
messageDestination = raw_input("To: ")

s.sendall(messageSource)
print "C: MAIL FROM:<" + messageSource + ">"

print "S: " + str(s.recv(1024))

s.sendall(messageDestination)
print "C: RCPT TO:<" + messageDestination + ">"

print "S: " + str(s.recv(1024))

s.sendall("DATA")
print "C: DATA"

print "S: " + str(s.recv(1024))


done = False

while(not done):

    message = raw_input("C: ")

    if not message:

        s.sendall("_")

    s.sendall(message)

    if(message == "."):

        done = True
        print "S: " + str(s.recv(1024))

        s.sendall("QUIT")
        print "C: QUIT"

        print "S: " + str(s.recv(1024))
        s.close()

