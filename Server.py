import argparse,socket,time

Users = {b'Naijee' : b'good',
		b'Lisa?' : b'very good.',
		b'Amy?' : b'normal.'}
			 
def get_answer(User):
	time.sleep(0)
	return Users.get(User,b'Error.')
	
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
		print('Accepted connection from {}'.format(address))
		handle_conversation(sock,address)

def handle_conversation(sock,address):
	try:
		while True:
			handle_request(sock)
	except EOFError :
		print('Client socket to {} has closed'.format(address))
	except Exception as e:
		print('Client {} error:{}'.format(address,e))
	finally :
		sock.close()
		
def handle_request(sock):
	User = recv_until(sock,b'?')
	#answer = get_answer(User)
	UserList = list(Users)
	answer = UserList.index(User)
	#answer_str = str(answer) + "."
	sock.sendall(bytes(str(answer) + ".","ascii"))
	
def recv_until(sock,suffix):
	message = sock.recv(4096)
	if not message :
		raise EOFError('Socket closed')
	while not message.endswith(suffix) :
		data = sock.recv(4096)
		if not data : 
			raise IOError('received {!r} then socket closed'.format(message))
		if message == message + data :
			break
		message += data
	return message

