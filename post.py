from socket import *
import sys, getopt, os

def printUsage():
    #prints usage instructions
    print 'usage: python post.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]'

def getUserId():
	#returns user id
	import getpass
	user = getpass.getuser()
	return user

def main(argv):
    userId = getUserId()
    serverName = '192.168.1.6'    #default hostname
    serverPort = 12000          #default port number
    print "user ID: ", userId

    #parsing arguments/options for hostname, port#
    try:
        opts, args = getopt.getopt(argv,"h:p:")
        if len(sys.argv) not in (2,4,6,):   #must have 2, 4, or 6 option/argument tokens
            print 'error: invalid command'
            printUsage()
            sys.exit(1)
    except getopt.GetoptError:
        print 'error: invalid command'
        printUsage()
        sys.exit(1)

    #changing hostname/port to argument options
    for opt, arg in opts:
        if opt == '-h':
            print "hostname: ", arg
            serverName = arg

        elif opt == '-p':
            print "port#: ", arg
            serverPort = int(arg)
        else:   #if option is neither -h nor -p
            print 'error: invalid command'
            printUsage()
            sys.exit(1)

    #getting groupname from appropriate last argument array element
    groupName = sys.argv[ len(sys.argv) - 1 ]

    print serverName, ": ", serverPort
    print "group name: ", groupName
    print "user id: ", userId

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    post = "post "+groupName
    print "post message: ", post
    clientSocket.send(post.encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024)
    print( "From Server:")
    print(modifiedSentence)
    clientSocket.close()

if __name__ == "__main__":
   main(sys.argv[1:])
