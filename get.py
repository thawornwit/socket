#*******************************************************#
#	Calvin Lee, CS352 Assignment 3
#*******************************************************#

from socket import *
import sys, getopt, os

#verbose = False  #for debugging

#def vprint(arg):
#    verbose print msg for debugging purposes
#    if verbose:
#        print arg

def printUsage():
    #prints usage instructions
    print 'usage: python get.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]'

def main(argv):
    serverName = 'localhost'    #default hostname
    serverPort = 12000          #default port number

    #parsing arguments/options for hostname, port#
    try:
        opts, args = getopt.getopt(argv,"h:p:") #valid options
        if len(sys.argv) not in (2,4,6,):   #must have 2, 4, or 6 option/argument tokens
            print 'error: invalid arguments'
            printUsage()
            sys.exit(1)
    except getopt.GetoptError:
        print 'error: invalid arguments'
        printUsage()
        sys.exit(1)

    #changing hostname/port to argument options
    for opt, arg in opts:
        if opt == '-h':
            serverName = arg
        elif opt == '-p':
            serverPort = int(arg)

    #getting groupname from appropriate last argument array element
    groupName = sys.argv[ len(sys.argv) - 1 ]

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    #********************************************#
#    vprint( 'host: '+serverName+": "+str(serverPort) )
#    vprint( "group name: "+groupName )
    #********************************************#

    group = "get "+groupName    #post msg with group name
    clientSocket.send(group)

    reply = clientSocket.recv(1024)
#    vprint( "From Server: "+reply)     #debug

    if reply == 'ok':
#        vprint("group is ok! getting message count")
        msgCount = clientSocket.recv(1024) #receive message count
        count = int(msgCount[10:])
        print("\n" + str(count) + " messages\n")

        for x in xrange(0, count):

            clientSocket.send("header")
            header = clientSocket.recv(1024)
            print header
            clientSocket.send("body")
            body = clientSocket.recv(1024)
            print body

#        vprint("end of messages")
        clientSocket.close()
        sys.exit(0)


    elif reply.startswith('error'):
#        vprint( reply )  #debug
        print reply
        clientSocket.close()
        sys.exit(1)
    else:
        print "server error"
        clientSocket.close()
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
