from socket import*

import json

import os

import threading

#SERVER_ADDR = '172.19.109.242'

SERVER_ADDR = '172.19.39.53'

#SERVER_ADDR = '192.168.199.102'

SERVER_PORT = 15000

PEER_PORT = 10086

MEGABYTE = 1024*1024

CHUNKSIZE = 50*MEGABYTE

'''

each peer has its own ip_addr and port to listen to 

others' requests

'''

class Peer:

	def __init__(self,peer_ip,peer_port):

		self.ip = peer_ip

		self.port = peer_port
		self.id = -1
		self.peer_socket = socket(AF_INET, SOCK_STREAM)

		self.peer_socket.bind(('',peer_port))

		self.peer_socket.listen(5)



	def __del__(self):

		self.peer_socket.close()



#peer send its ip_addr and port to server for registration

	def register(self):

		clientSocket = socket(AF_INET,SOCK_STREAM)

		clientSocket.connect((SERVER_ADDR,SERVER_PORT))

		peer_info = '1 '+str(self.ip)+' '+str(self.port)

		clientSocket.send(str.encode(peer_info))

		response_from_server = clientSocket.recv(4096)
		response_from_server = response_from_server.decode()
		response_from_server = response_from_server.split(' ',2)
		if self.id == -1:
			self.id = int(response_from_server[1])
		print(str(response_from_server))
		print('my id is',self.id)
		clientSocket.close()

	#as a client

	def update_resource(self):

		path = os.getcwd()

		own_resource = os.listdir(path)

		clientSocket = socket(AF_INET,SOCK_STREAM)

		clientSocket.connect((SERVER_ADDR,SERVER_PORT))

		clientSocket.send(str.encode('2 update_resource'))

		response_from_server = clientSocket.recv(4096)

		print(response_from_server)
		clientSocket.send(str.encode(str(self.id)))
		clientSocket.recv(4096)
		own_resource = ";".join(own_resource)
		clientSocket.send(str.encode(own_resource))

		#response_from_server = clientSocket.recv(4096)

		#print(str(response_from_server))

		clientSocket.close()



	#as a client

	def chat_with_sb(self):

		online_peers = self.get_peers_online()

		my_friend = raw_input('Please enter a friend to chat(ipv4 address)')

		if my_friend in online_peers:

			clientSocket = socket(AF_INET,SOCK_STREAM)

			clientSocket.connect((my_friend,PEER_PORT))

			#this should be a request

			clientSocket.send("2 Hello! I'm chatting with you! If one of us say 'Bye!',the chatting will end.")

			friend_response = clientSocket.recv(4096)

			while str(friend_response) != 'Bye!':

				greeting = raw_input('Please enter what you want to say:')

				clientSocket.send(greeting)

				if str(greeting == 'Bye!'):

					break;

				friend_response = clientSocket.recv()

		else:

			print('Sorry, this friend is not online')



	#connect with server

	def get_peers_online(self):

		clientSocket = socket(AF_INET,SOCK_STREAM)

		clientSocket.connect((SERVER_ADDR,SERVER_PORT))

		my_request = '3 get_peers_online'

		clientSocket.send(str.encode(my_request))

		online_peers_json = clientSocket.recv(4096)

		online_peers = json.loads(online_peers_json)

		clientSocket.close()

		return online_peers



	def handle_peer(self):

		threads = []

		t1 = threading.Thread(self.listening_to_others)

		t2 = threading.Thread(self.sending_out_request)

		threads.append(t1)

		threads.append(t2)

	#as a client

	def download_resource(self):
		clientSocket = socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((SERVER_ADDR,SERVER_PORT))
		request_file = input('Please enter filename you want to download,notice that filename should not contain spaces')
		my_request = '3 '+request_file
		clientSocket.send(str.encode(my_request))
		peer_have_resource = clientSocket.recv(4096)
		peer_have_resource = peer_have_resource.decode()
		if len(peer_have_resource) == 0:
			pass
		else:
			peer_have_resource = peer_have_resource.split(";")
		print('peer_have_resource',peer_have_resource)
		clientSocket.close()

		if len(peer_have_resource) == 0:
			print('Sorry, the file does not exist in the peer system')

		else:
			if len(peer_have_resource) >= 2:
				self.download_helper(request_file,peer_have_resource[0],1,2)
				self.download_helper(request_file,peer_have_resource[1],2,2)
			else:
				self.download_helper(request_file,peer_have_resource[0],1,1)
			self.combine_file(request_file)



	def download_helper(self,filename,dst_ip,seq,total):

		download_socket = socket(AF_INET,SOCK_STREAM)

		download_socket.connect((dst_ip,PEER_PORT))

		download_socket.send(str.encode('1 '+filename+' '+str(seq)+' of '+str(total)))

		filenum = download_socket.recv(4096)

		filenum = int(filenum)

		group_member = math.ceil(filenum/total)

		start_num = group_member*(seq-1)+1

		end_num = group_member*seq

		if end_num>filenum:

			end_num = filenum

		i = start_num

		while i <= end_num:

			new_file_name = filename+'_part_'+str(i)

			f = open(new_file_name,'wb+')

			while True:

				content = download_socket.recv(4096)

				if content:

					f.write(content)

				else:

					f.close()

					break;

			print('file',new_file_name,'write successful')

		download_socket.close()



	#as a server

	def handle_download(self,connectionSocket,conaddr,filename,seq,total):

		filenum = self.split_file(filename)

		if filenum == None:

			return

		group_member = math.ceil(filenum/total)

		start_num = group_member*(seq-1)+1

		end_num = group_member*seq

		if end_num > filenum:

			end_num = filenum

		i = start_num

		while i <= end_num:

			new_file_name = filename+'_part_'+_str(i)

			f = open(new_file_name,'rb')

			while True:

				content = f.read(4096)

				if content:

					connectionSocket.send(content)

				else:

					f.close()

					break

			print(new_file_name,'sent successful')



	#as a server

	def handle_chat(self,connectionSocket,con_addr):

		my_response = raw_input(con_addr[0],'is connected with you. Please enter your response. When you say "Bye!",the coversation ends.')

		self.peer_socket.send(my_response)

		other_greeting = self.peer_socket.recv(4096)

		while str(other_greeting) != 'Bye!':

			my_response = raw_input('Enter you response:')

			self.peer_socket.send(my_response)

			if str(my_response) == 'Bye!':

				break;

			self.peer_socket.recv(4096)



	def handle_file_transport(self,connectionSocket,con_addr):

		pass

	#as a server

	def listening_to_others(self):

		while True:

			connectionSocket, con_addr = self.peer_socket.accept()

			request_from_others = self.peer_socket.recv(4096)

			request_from_others = str(request_from_others)

			request_from_others = request_from_others.split(' ',3)

			if request_from_others[0] == 1:

				filename = request_from_others[1]

				seq = request_from_others[2]

				total = request_from_others[3]

				self.handle_download(connectionSocket,con_addr,filename,seq,total)

			#chat with others

			elif request_from_others[0] == 2:

				self.handle_chat(connectionSocket,con_addr)

			elif request_from_others[0] == 3:

				self.handle_file_transport(connectionSocket,con_addr)

			connectionSocket.close()



	def sending_out_request(self):

		print('What you want to do?')

		print('1.download_resource')

		print('2.chat with others')

		while True:

			print('What you want to do?')

			act = input()

			if act == 1:

				self.download_resource()

			elif act == 2:

				self.chat_with_sb()

			elif act == 3:

				pass

		

	def split_file(self,filename):

		try:

			f = open(filename,'rb')

			f.close()

		except IOError:

			print('File is not accessible')

			return

		partnum = 0

		inputfile = open(filename,'rb')

		while True:

			chunk = inputfile.read(CHUNKSIZE)

			if not chunk:

				break

			partnum = partnum + 1

			file_split_name = filename+'_part_'+str(partnum)

			fileobj = open(file_split_name,'wb')

			fileobj.write(chunk)

			fileobj.close()

		return partnum



	def combine_file(self,filename,filenum):

		outfile = open(filename,'wb')

		for i in filenum:

			file_split_name = filename+'_part_'+i+1

			infile = open(file_split_name,'rb')

			data = infile.read()

			outfile.write(data)

			infile.close()

		outfile.close()



if __name__ == '__main__':

	my_peer = Peer('192.168.199.102',PEER_PORT)

	my_peer.register()

	my_peer.update_resource()

	my_peer.download_resource()

	input()