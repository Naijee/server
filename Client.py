import argparse,socket,random ,Server

def client(address , cause_error=False,Username = 'guest'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(address)
	Users = list(Server.Users)
	if cause_error :
		sock.sendall(Users[0][:-1])
		return
	for Users in random.sample(Users,3) :
		sock.sendall(Users)
		print(Users.decode("utf-8"),Server.recv_until(sock,b'.').decode("utf-8"))
	sock.close()

if __name__=='__main__' :
	parser = argparse.ArgumentParser(description = 'Example client')
	parser.add_argument('host',help = 'IP or hostname')
	parser.add_argument('Username',help = 'User Name')
	parser.add_argument('-e',action = 'store_true', help = 'cause an error')
	parser.add_argument('-p',metavar='port',type = int , default = 1060,help = 'TCP port (default 1060)')
	args = parser.parse_args()
	address = (args.host,args.p)
	client(address,args.e,args.Username)