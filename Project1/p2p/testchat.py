
from socket import*
import os
SERVER_ADDR = '192.168.199.102'
SERVER_ADDR = '172.19.39.53'
PEER_PORT = 10086
SERVER_PORT = 15000
class Peer:
	def __init__(self,peer_ip,peer_port):
		self.ip = peer_ip
		self.port = peer_port
		self.id = -1
		#self.peer_socket = socket(AF_INET, SOCK_STREAM)
		#self.peer_socket.bind(('',peer_port))
		#self.peer_socket.listen(5)

	def chat_with_sb(self):

		online_peers = self.get_peers_online()
		print('friends online:',online_peers)

		my_friend = input('Please enter a friend to chat(ipv4 address)')

		if my_friend in online_peers:

			clientSocket = socket(AF_INET,SOCK_STREAM)

			clientSocket.connect((my_friend,PEER_PORT))

			#this should be a request
			greeting = "2 Hello! I'm chatting with you! If one of us say 'Bye!',the chatting will end."
			clientSocket.send(str.encode(greeting))

			friend_response = clientSocket.recv(4096)

			while str(friend_response) != 'Bye!':

				greeting = input('Please enter what you want to say:')

				clientSocket.send(str.encode(greeting))

				if str(greeting == 'Bye!'):

					break;

				friend_response = clientSocket.recv()

		else:

			print('Sorry, this friend is not online')


	def get_peers_online(self):

		clientSocket = socket(AF_INET,SOCK_STREAM)

		clientSocket.connect((SERVER_ADDR,SERVER_PORT))

		my_request = '4 get_peers_online'

		clientSocket.send(str.encode(my_request))

		online_peers = clientSocket.recv(4096)

		online_peers = online_peers.decode()
		online_peers = online_peers.split(";")

		clientSocket.close()

		return online_peers

if __name__ == '__main__':

	my_peer = Peer('172.19.39.53',PEER_PORT)

	#my_peer.register()

	#my_peer.update_resource()

	#my_peer.download_resource()
	my_peer.chat_with_sb()

	input()
