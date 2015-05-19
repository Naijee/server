import argparse,socket,struct,sys

def recvall2(sock,length):
	data = b''
	while len(data) < length:
		more = sock.recv(length - len(data))
		if not more:
			raise EOFError('was expecting %d bytes but only received %d bytes before the socket closed' %(length,len(data)))
		data += more
	print(repr(data))
	return data
	
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
	
def server(interface , port) :
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind((interface,port))
	sock.listen(1)
	print('Listening at',sock.getsockname())
	while True:
		sc,sockname = sock.accept()
		print('We have accepted a connection from ',sockname)
		print('socket name : ',sc.getsockname())
		print('socket peer : ',sc.getpeername())
		#message = recvall(sc,16)
		message = recv_msg(sc)
		print('User said: ',message.decode("utf-8"))
		msg = input('Server said:')
		msg = msg.encode('utf-8')
		msg = struct.pack('>I', len(msg)) + msg
		sc.sendall(msg)
		sc.close()
		
def client(host,port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((host,port))
	print('Client has been assigned socket name',sock.getsockname())
	#sock.sendall(b'Hi there,server')
	msg = input('You said:')
	msg = msg.encode('utf-8')
	msg = struct.pack('>I', len(msg)) + msg
	sock.sendall(msg)
	#reply = recvall(sock,16)
	reply= recv_msg(sock)
	print('The server said :',reply.decode("utf-8"))
	sock.close()

if __name__ == '__main__':
	choices = {'client':client,'server':server}
	parser = argparse.ArgumentParser(description='Send and receive over TCP')
	parser.add_argument('role',choices=choices , help = 'Which role to play')
	parser.add_argument('host',help='interface the server listen at; host the client send to')
	parser.add_argument('-p',metavar = 'PORT',type = int , default = 1060 , help = 'TCP port (default 1060)')
	args = parser.parse_args()
	function = choices[args.role]
	function(args.host,args.p)