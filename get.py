from socket import *
import sys, getopt, os

verbose = True  #for debugging

def vprint(arg):
    #verbose print msg for debugging purposes
    if verbose:
        print arg

def printUsage():
    #prints usage instructions
    print 'usage: python get.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]'
    print 'type "quit" (without quotes) and press enter to end message.'

def main(argv):
    serverName = '192.168.1.6'    #default hostname
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

if __name__ == "__main__":
   main(sys.argv[1:])
