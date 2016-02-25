from socket import *
import thread

def printUsage():
	#prints usage instructions
	print 'usage: python server.py [-p port#(optional)]'

def main(argv):
	serverPort = 12000	#default port number
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)
	print 'The server is ready to receive'
	while 1:
	    connectionSocket, addr = serverSocket.accept()
	    sentence = connectionSocket.recv(1024)
	    print 'received message: ', sentence
	    capitalizedSentence = sentence.upper()
	    print 'replying: ', capitalizedSentence
	    connectionSocket.send(capitalizedSentence)
	    connectionSocket.close()
