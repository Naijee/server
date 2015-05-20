import argparse,socket,struct,sys
import time

CONNECTION_LIST = {}
UserList = {'Alice':'aaaa','Bob':'bbbb','Cindy':'cccc'}
messagepool = {}
coversation_LIST = {}

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data	

def parse_command_line(description):
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('host', help = 'IP or hostname')
	parser.add_argument('-p', metavar='port',type = int , default = 1060,help = 'TCP port (default 1060)')
	args = parser.parse_args()
	address = (args.host,args.p)
	return address	

def create_srv_socket(address):
	listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	listener.bind(address)
	listener.listen(64)
	print('Listening at {}.'.format(address))
	return listener

def accept_connections_forever(listener):
	while True:
		sock,address = listener.accept()
		if(checkuser(sock) == False):
			break
		#CONNECTION_LIST.append(sock)
		print(CONNECTION_LIST)
		print('\nAccepted connection from {}'.format(address))
		print('socket name : ',sock.getsockname())
		print('socket peer : ',sock.getpeername())
		handle_conversation(sock,address)

def handle_conversation(sock,address):
	Isconnect = True
	try:
		while Isconnect:
			Isconnect = handle_request(sock)
	except EOFError :
		print('Client socket to {} has closed'.format(address))
	except Exception as e:
		print('Client {} error:{}'.format(address,e))
	finally :
		sock.close()
		
def handle_request(sock):
	message = recv_msg(sock)
	#print(GetUserName(sock) ,'said: ',message.decode("utf-8"))
	#print('talkto' in message.decode("utf-8"))
	print('A conversation : ' , GetUserName(sock) in coversation_LIST)
	if(GetUserName(sock) in coversation_LIST) :
		if('\exit' in message.decode("utf-8")):
			BreakConversation(sock)
			return True
		else : 
			print('coversation_LIST : ' , coversation_LIST)
			AConversation(sock,message)
			return True
	else : 
		print(coversation_LIST)
		if('\list' in message.decode("utf-8")):
				sendlist(sock)
				return True
		elif('\logout' in message.decode("utf-8")):
			closescock(sock)
			return False
		elif('talkto' in message.decode("utf-8")):
			talkto(sock,message)
			return True
		elif('makecon' in message.decode("utf-8")):
			MakeConversation(sock,message)
			print('We make a conversation!!')
			return True
		else :
			fromuser = GetUserName(sock)
			message = message.decode("utf-8")
			message = '(Broadcast message from ' + fromuser + ')' + message
			message = message.encode("utf-8")
			message = struct.pack('>I', len(message)) + message
			broadcast_data(sock,message)
			return True
		
def broadcast_data (sock, message):
	for user in CONNECTION_LIST:
		if CONNECTION_LIST[user] != sock:
			try : 
				print(message.decode("utf-8"))
				CONNECTION_LIST[user].sendall(message)
			except :
				CONNECTION_LIST[user].close()
				del CONNECTION_LIST[user]
		
def checkuser(sock):
	user = recv_msg(sock)
	if(user.decode("utf-8") in UserList):
		msg = b'pass'
		msg = struct.pack('>I', len(msg)) + msg
		print(user.decode("utf-8"))
		sock.sendall(msg)
		while True :
			passwd = recv_msg(sock)
			if(UserList[user.decode("utf-8")] == passwd.decode("utf-8")):
				msg = b'pass'
				msg = struct.pack('>I', len(msg)) + msg
				sock.sendall(msg)
				print(user.decode("utf-8")+'is log in')
				CONNECTION_LIST[user.decode("utf-8")] = sock
				OffLineMessage(sock)
				return True
			else:
				msg = b'fail'
				msg = struct.pack('>I', len(msg)) + msg
				sock.sendall(msg)
				return False
	else:
		msg = b'fail'
		msg = struct.pack('>I', len(msg)) + msg
		sock.sendall(msg)
		return False
	#print(UserList[user.decode("utf-8")])
	
def sendlist(sock):
	str = ' '
	for user in CONNECTION_LIST:
		if (str == ' ') :
			str = user + str
		else :
			str = str + ' & ' + user + ' '
	print(str)
	str = str + 'is online'
	str = str.encode("utf-8")
	str = struct.pack('>I', len(str)) + str
	print(sock.getpeername())
	sock.sendall(str)

def talkto(sock,message) :
	str = ''
	fromuser = ''
	message = message.decode("utf-8")
	tmp = message.strip().split(' ')
	msg = len(tmp[1]) + 8
	msg = message[msg:]
	fromuser = GetUserName(sock)
	msg = fromuser + ' say : ' + msg
	msg = msg.encode("utf-8")
	msg = struct.pack('>I', len(msg)) + msg
	if(tmp[1] in CONNECTION_LIST):
		print(tmp[1])
		for user in CONNECTION_LIST:
			if user == tmp[1]:
				try : 
					print(GetUserName(sock) ,'say to', GetUserName(CONNECTION_LIST[user]) , ' : ' , msg.decode("utf-8"))
					CONNECTION_LIST[user].sendall(msg)
				except :
					CONNECTION_LIST[user].close()
					del CONNECTION_LIST[user]
	else:
		messagepool[msg] = tmp[1]
		print(messagepool)
	
				
def closescock(sock) :
	delscok = ''
	for user in CONNECTION_LIST:
		if(CONNECTION_LIST[user] == sock):
			delscok = user
	CONNECTION_LIST[delscok] = ''
	del CONNECTION_LIST[delscok] 
	sock.close()
	print(delscok + ' log out!!!!')

def GetUserName(sock) :
	for user in CONNECTION_LIST:
		if(CONNECTION_LIST[user] == sock):
			Name = user
	return Name
	
def OffLineMessage(sock):
	delmessage = []
	for message in messagepool : 
		if messagepool[message] == GetUserName(sock) :
			sock.sendall(message)
			delmessage.append(message)
	for message in delmessage :
		del messagepool[message] 
		
def MakeConversation(sock,message):
	str = ''
	touser = ''
	message = message.decode("utf-8")
	tmp = message.strip().split(' ')
	for user in CONNECTION_LIST:
		if user == tmp[1]:
			try : 
				print(GetUserName(sock) ,'make a conversation to', GetUserName(CONNECTION_LIST[user]))
				coversation_LIST[GetUserName(sock)] =  GetUserName(CONNECTION_LIST[user])
			except :
				print('error')
				CONNECTION_LIST[user].close()
				del CONNECTION_LIST[user]
				
def AConversation(sock,message):
	message = message.decode("utf-8")
	fromuser = GetUserName(sock)
	msg = fromuser + ' say : ' + message
	msg = msg.encode("utf-8")
	msg = struct.pack('>I', len(msg)) + msg
	Touser = coversation_LIST[GetUserName(sock)]
	if(Touser in CONNECTION_LIST):
		print(Touser)
		for user in CONNECTION_LIST:
			if user == Touser:
				try : 
					print(GetUserName(sock) ,'talk to', GetUserName(CONNECTION_LIST[user]) , ' : ' , msg.decode("utf-8"))
					CONNECTION_LIST[user].sendall(msg)
				except :
					print('error')
					CONNECTION_LIST[user].close()
					del CONNECTION_LIST[user]
	else:
		messagepool[msg] = Touser
		print(messagepool)
	
def BreakConversation(sock):
	user = GetUserName(sock)
	print(user,'colse the conversation to ', coversation_LIST[user])
	del coversation_LIST[user] 