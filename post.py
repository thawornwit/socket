from socket import *
import sys, getopt, os

verbose = False  #for debugging

def vprint(arg):
    #verbose print msg for debugging purposes
    if verbose:
        print arg

def printUsage():
    #prints usage instructions
    print 'usage: python post.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]'
    print 'type "quit" (without quotes) and press enter to end message.'


def getUserId():
	#returns user id
	import getpass
	user = getpass.getuser()
	return user

def main(argv):
    userId = getUserId()
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
    vprint( 'host: '+serverName+": "+str(serverPort) )
    vprint( "group name: "+groupName )
    vprint( "user id: "+userId )
    #********************************************#

    group = "post "+groupName    #post msg with group name

    clientSocket.send(group)
    reply = clientSocket.recv(1024)
    vprint( "From Server: "+reply)     #debug

    if reply == 'ok':
        vprint( 'group is ok! continuing with id...')   #debug
        username = 'id '+userId
        clientSocket.send(username)
        reply2 = clientSocket.recv(1024)
        vprint( "from Server: "+reply2)    #debug

        if reply2 == 'ok':
            vprint( 'id is ok! continuing with msg...') #debug

            print 'Please enter your message: (quit to exit)'

            msg = ""
            sentinel = 'quit'   #type quit and press enter to exit message
            for line in iter(raw_input, sentinel):
                msg += line + "\n"
            clientSocket.send(msg)
            clientSocket.close()
            print "message sent successfully."
            sys.exit(0)

        elif reply2.startswith('error'):
            vprint( reply2 )     #debug
            clientSocket.close()
            sys.exit(1)
        else:
            print "server error"
            clientSocket.close()
            sys.exit(1)


    elif reply.startswith('error'):
        vprint( reply )  #debug
        clientSocket.close()
        sys.exit(1)
    else:
        print "server error"
        clientSocket.close()
        sys.exit(1)




if __name__ == "__main__":
   main(sys.argv[1:])
