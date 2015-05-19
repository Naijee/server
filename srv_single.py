import SimpleServer

if __name__ == '__main__':
    address = SimpleServer.parse_command_line('simple single-threaded server')
    listener = SimpleServer.create_srv_socket(address)
    SimpleServer.accept_connections_forever(listener)