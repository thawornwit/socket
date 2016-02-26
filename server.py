#*******************************************************#
#	Calvin Lee, CS352 Assignment 3
#*******************************************************#

from socket import *
import sys, getopt, thread, time

#verbose = False

#messages = { 'groupName' : [('address', 'username', 'timestamp', 'message')]}
messages = dict()

#def vprint(arg):
#	if verbose:
#		print arg

def printUsage():
	#prints usage instructions
	print 'usage: python server.py [-p port#(optional)]'

def isValidString(msg):
	import string
	trans = string.maketrans('','')
	allowed = string.printable
	return not msg.translate(trans, allowed)

def clientHandler(connSocket, clientAddr):
	global messages
	cmd = connSocket.recv(1024)
	#*******************************************************#
	#this is the POST handler
	if cmd.startswith('post '):
#	    vprint( 'this is a post command!')	#debug
	    groupName = cmd[5:]
#	    vprint( 'received groupname: '+groupName)	#debug
	    if isValidString(groupName):
		    reply = 'ok'
#		    vprint( 'groupname is ok!')	#debug
		    connSocket.send(reply)
		    cmd2 = connSocket.recv(1024)
#		    vprint( cmd2 )	#debug
		    if cmd2.startswith('id '):
#			    vprint( 'this is an id command!')	#debug
			    userName = cmd2[3:]
#			    vprint( 'received username: '+userName)	#debug
			    if isValidString(userName):
					reply2 = 'ok'
#					vprint( 'username is ok!')	#debug
					connSocket.send(reply2)
					msg = connSocket.recv(1024)	#receives message
					timestamp = time.strftime("%a %c %Y")
#					vprint("received message: \n" + msg)	#debug
					print("received message: \n" + msg)
					if groupName not in messages:
						messages[groupName] = [( (clientAddr, userName, timestamp, msg) )]
					else:
						messages[groupName].append( (clientAddr, userName, timestamp, msg) )
#					vprint( "messages: \n")	#debug
#					vprint( messages )	#debug
#					vprint( "message count for group " + groupName + ": \n")	#debug
#					vprint( len(messages[groupName]) )	#debug
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
#		    vprint( 'invalid group name!')	#debug
		    connSocket.send(reply)
		    connSocket.close()
		    return;

	#*******************************************************#
	#this is the GET handler
	elif cmd.startswith('get '):
#		vprint( 'this is a get command!')	#debug
		groupName = cmd[4:]
#		vprint( 'received groupname: '+groupName)	#debug
		if isValidString(groupName):	#if group name is a valid printable string
			if groupName in messages:	#and it exists in messages
#				vprint( 'groupname is ok!')	#debug
				reply = 'ok'
				connSocket.send(reply)
				count = len(messages[groupName])
				msgCount = "messages: " + str(count)
#				vprint("sending: " + msgCount)
				connSocket.send(msgCount)
				for row in messages[groupName]:
					while 1:	#accepts header
						reply = connSocket.recv(64)
					 	if reply == 'header':
							header = "from " + str(row[1]) + " /" + str(row[0][0]) + ":" + str(row[0][1]) + " " + str(row[2]) + "\n"
#							vprint( "header: \n" + header )
							connSocket.send(header)
							break;
					while 1:	#accepts body
						reply = connSocket.recv(64)
						if reply == "body":
							msg = "" + str(row[3]) + "\n"
#							vprint(" message: \n" + msg )
							connSocket.send(msg)
							break;
#				vprint("end of messages.")
				connSocket.close()
				sys.exit(0)

		reply = 'error: invalid group name'
		connSocket.send(reply)
		connSocket.close()
		return;
	#*******************************************************#
	else:
		reply = 'error: invalid command'
#		vprint( 'neither post nor get!')	#debug
#		vprint( 'replying with: '+reply)	#debug
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
		thread.start_new_thread(clientHandler, (connSocket, clientAddr))

if __name__ == "__main__":
	main(sys.argv[1:])
