# socket
a simple set of TCP messaging applications, written in Python.
all three applications require Python to be installed on the machine.
if unspecified, default server host name is 'localhost', and default
port is '12000'.

SERVER
The 'server.py' program runs a messaging server application that waits for messages 
to be posted to the IP address of the corresponding machine.

usage: open cmd or terminal, go to the directory with 'server.py' file, and run:
python server.py [-p port#(optional)]
ex: python server.py -p 12345

CLIENT (post)
Run 'post.py' to post a message to a machine running the 'server.py' application for
a designated group, identified by groupname.

usage: open cmd or terminal, go to the directory with 'post.py', and run:
python post.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]
ex: python post.py -h 192.168.1.2 12345 Group1

Then enter the message you'd like to post. type "quit" (without quotes) on a new line
and press enter to quit.

CLIENT (get)
Run 'get.py' to retrieve posted messages to a message from the server for a designated
group, identified by groupname.

usage: open cmd or terminal, go to the directory with 'get.py', and run:
python get.py [-h hostname(optional)] [-p port#(optional)] [groupname(REQUIRED)]
ex: python get.py Group2
