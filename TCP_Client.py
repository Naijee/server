import TCP_Server
import argparse,socket,struct,sys ,time
from threading import Thread
from getpass import getpass 

host = ''

def client(host,port,UserName):
	EXIT = False
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(address)
	if(user(sock,UserName) == True) :
		print('Client has been assigned socket name',sock.getsockname())
		t = (sock,)
		Thread(target=recvmessage, args=t).start()
		while True :
			if(EXIT == False):
				msg = input('')
				if(msg == '\logout'):
					EXIT = True
				msg = msg.encode('utf-8')
				msg = struct.pack('>I', len(msg)) + msg
				sock.sendall(msg)
			else :
				break
	#time.sleep(1)
	
	#while True:
	#	msg = input('You said:')
	#	msg = msg.encode('utf-8')
	#	msg = struct.pack('>I', len(msg)) + msg
	#	sock.sendall(msg)
	#reply = recvall(sock,16)
	#reply= TCP_Server.recv_msg(sock)
	#print(sock.getpeername(),'said :',reply.decode("utf-8"))
		
def recvmessage(sock):
		#print('Recive')
		while True :

				reply= TCP_Server.recv_msg(sock)
				if (reply == None):
					break
				else:
					print(reply.decode("utf-8"))
		sys.exit()




def user(sock,UserName):
		#passwd = input('請輸入密碼:')
		passwd = getpass()
		user = UserName.encode('utf-8')
		user = struct.pack('>I', len(user)) + user
		sock.sendall(user)
		while True:
			reply= TCP_Server.recv_msg(sock)
			if(reply.decode("utf-8") == 'pass'):
				passwd = passwd.encode('utf-8')
				passwd = struct.pack('>I', len(passwd)) + passwd
				sock.sendall(passwd)
				while True :
					reply= TCP_Server.recv_msg(sock)
					if(reply.decode("utf-8") == 'pass') :
						print('Hello ' + UserName)
						return True
					else:
						print('You input a wrong passwd')
						return False
		
		
if __name__=='__main__' :
	parser = argparse.ArgumentParser(description = 'Example client')
	parser.add_argument('host',help = 'IP or hostname')
	parser.add_argument('UserName',help = 'User name')
	parser.add_argument('-e',action = 'store_true', help = 'cause an error')
	parser.add_argument('-p',metavar='port',type = int , default = 1060,help = 'TCP port (default 1060)')
	args = parser.parse_args()
	address = (args.host,args.p)
	client(address,args.e,args.UserName)