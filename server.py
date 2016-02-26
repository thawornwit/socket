from socket import *
import sys, getopt, thread

verbose = True

messages = { 'groupName' : [('address', 'port', 'username', 'timestamp', 'message')]}

def vprint(arg):
	if verbose:
		print arg

def printUsage():
	#prints usage instructions
	print 'usage: python server.py [-p port#(optional)]'

def isValidString(msg):
	import string
	trans = string.maketrans('','')
	allowed = string.printable
	return not msg.translate(trans, allowed)

def clientHandler(connSocket, clientAddr, serverPort):
	global messages
	cmd = connSocket.recv(1024)
	if cmd.startswith('post '):
	    vprint( 'this is a post command!')	#debug
	    groupName = cmd[5:]
	    vprint( 'received groupname: '+groupName)	#debug
	    if isValidString(groupName):
		    reply = 'ok'
		    vprint( 'groupname is ok!')	#debug
		    connSocket.send(reply)

		    #if groupName not in messages:
			#	messages[groupName] = [('address', 'port', 'username', 'timestamp', 'message')]}

			#	print "messages: \n", messages

		    cmd2 = connSocket.recv(1024)
		    vprint( cmd2 )	#debug
		    if cmd2.startswith('id '):
			    vprint( 'this is an id command!')	#debug
			    userName = cmd2[3:]
			    vprint( 'received username: '+userName)	#debug
			    if isValidString(userName):
					reply2 = 'ok'
					vprint( 'username is ok!')	#debug
					connSocket.send(reply2)
					msg = connSocket.recv(1024)	#receives message
					print "the message: \n", msg
					if groupName not in messages:
						messages[groupName] = [( (clientAddr, serverPort, userName, 'timestamp', msg) )]
					else:
						messages[groupName].append( (clientAddr, serverPort, userName, 'timestamp', msg) )
					vprint( "messages: \n" + messages )
					connSocket.close()
					return;
			    else:
					reply = 'error: invalid user name'
					connSocket.send(reply)
					connSocket.close()
					return;
		    else:
				reply = 'error: invalid command'
				connSocket.send(reply)
				connSocket.close()
				return;
	    else:
		    reply = 'error: invalid group name'
		    vprint( 'invalid group name!')	#debug
		    connSocket.send(reply)
		    connSocket.close()
		    return;
	elif cmd.startswith('get '):
		reply = 'ok'
		vprint( 'this is a get command!')	#debug
		vprint( 'replying with: '+reply)	#debug
		connSocket.send(reply)
		connSocket.close()
		return;
	else:
		reply = 'error: invalid command'
		vprint( 'neither post nor get!')	#debug
		vprint( 'replying with: '+reply)	#debug
		connSocket.send(reply)
		connSocket.close()
		return;

def main(argv):
	serverPort = 12000	#default port number

	try:
		opts, args = getopt.getopt(argv, "p:")
		if len(sys.argv) not in (1, 3):
			print 'error: invalid command'
			printUsage()
			sys.exit(1)
	except getopt.GetoptError:
		print 'error: invalid command'
		printUsage()
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-p':
			serverPort = int(arg)


	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(5)
	print 'The server is ready to receive'
	while 1:
		connSocket, clientAddr = serverSocket.accept()
		thread.start_new_thread(clientHandler, (connSocket, clientAddr, serverPort))

if __name__ == "__main__":
	main(sys.argv[1:])
