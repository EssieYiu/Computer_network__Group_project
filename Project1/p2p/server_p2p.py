from socket import*
import json
SERVER_PORT = 15000
CONNCTION_LIST=[]
RESOURCES=[]
class Server:
	def __init__(self):
		self.serverSocket = socket(AF_INET, SOCK_STREAM)
		self.serverSocket.bind(('',SERVER_PORT))
		self.serverSocket.listen(5)
		print('Server is listening')
		
	def __del__(self):
		self.serverSocket.close()

	def handle_server(self):
		while True:
			connectionSocket, addr = self.serverSocket.accept()
			request_from_client = connectionSocket.recv(4096)
			print('client addr is',addr)
			print('request from client:',request_from_client)
			request_from_client = request_from_client.decode()
			request_from_client = request_from_client.split(' ',2)
			print('after split:',request_from_client)
			#register
			if request_from_client[0] == '1':
				if addr[0] not in CONNCTION_LIST:
					CONNCTION_LIST.append(addr[0])
					connectionSocket.send(str.encode("Register successfully!"))
				else:
					connectionSocket.send(str.encode("You have previously registered."))
			#update resources
			elif request_from_client[0] == '2':
				connectionSocket.send(str.encode('You are updating your resources'))
				print('peer',addr[0],'updates its resources')
				connectionSocket.send(str.encode('You are updating your resources'))
				renew_str = connectionSocket.recv(4096)
				renew_str = renew_str.decode()
				renew = renew_str.split(";")
				RESOURCES[addr[0]] = renew 
				print(RESOURCES[addr[0]])
				#connectionSocket.send(str.encode("Update resources successfully!"))
			#download resources
			elif request_from_client[0] == '3':
				peer_have_resource = []
				for peer in CONNCTION_LIST:
					for data in RESOURCES[peer]:
						if data == request_from_client[2]:
							peer_have_resource.append(peer)
				connectionSocket.send(json.dumps(peer_have_resource))
			#chatting with sb get peers online
			elif request_from_client[0] == '4':
				online_peers = ";".join(CONNCTION_LIST)
				connectionSocket.send(str.encode(online_peers))
			elif request_from_client[0] == '5':
				pass
			connectionSocket.close()
			print('socket close')

if __name__ == '__main__':
	my_server = Server()
	my_server.handle_server()
	input()