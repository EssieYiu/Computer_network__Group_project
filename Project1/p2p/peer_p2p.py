from socket import*

import json

import os
import math
import threading

#SERVER_ADDR = '172.19.109.242'

#SERVER_ADDR = '172.19.39.53'

#SERVER_ADDR = '192.168.199.102'
SERVER_ADDR = '192.168.199.205'

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
			print('into this if:')
			self.id = int(response_from_server[1])
		print(" ".join(response_from_server))
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
		print('friends online:',online_peers)

		my_friend = input('Please enter a friend to chat(ipv4 address)')

		if my_friend in online_peers:

			clientSocket = socket(AF_INET,SOCK_STREAM)

			clientSocket.connect((my_friend,PEER_PORT))

			#this should be a request
			greeting = "2 Hello! I'm chatting with you! If one of us say 'Bye!',the chatting will end."
			clientSocket.send(str.encode(greeting))
			print("Please wait for your friend's response")
			friend_response = clientSocket.recv(4096)
			friend_response = str(friend_response.decode())
			print('my friend',my_friend,":",friend_response)
			while friend_response != 'Bye!':
				greeting = input('Please enter what you want to say:')

				clientSocket.send(str.encode(greeting))

				if greeting == 'Bye!':
					break;
				print("Please wait for your friend's response")
				friend_response = clientSocket.recv(4096)
				friend_response = str(friend_response.decode())
				print('my friend:',my_friend,":",friend_response)

		else:

			print('Sorry, this friend is not online')



	#connect with server

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
		
	#as a client
	def download_resource(self):
		clientSocket = socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((SERVER_ADDR,SERVER_PORT))
		print('download')
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
				filenum = self.download_helper(request_file,peer_have_resource[0],1,2)
				self.download_helper(request_file,peer_have_resource[1],2,2)
			else:
				filenum = self.download_helper(request_file,peer_have_resource[0],1,1)
			self.combine_file(request_file,filenum)



	def download_helper(self,filename,dst_ip,seq,total):

		download_socket = socket(AF_INET,SOCK_STREAM)

		download_socket.connect((dst_ip,PEER_PORT))

		download_socket.send(str.encode('1 '+filename+' '+str(seq)+' of '+str(total)))
		
		filenum = download_socket.recv(4096)
		filenum = filenum.decode()
		print('filenum',filenum,' type:',type(filenum))
		filenum = int(filenum)
		download_socket.send(str.encode("ok"))
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
			i = i+1
			print('file',new_file_name,'write successful')

		download_socket.close()
		return filenum


	#as a server

	def handle_download(self,connectionSocket,conaddr,filename,seq,total):

		filenum = self.split_file(filename)

		if filenum == None:

			return

		connectionSocket.send(str.encode(str(filenum)))
		connectionSocket.recv(4096)

		group_member = math.ceil(filenum/total)

		start_num = group_member*(seq-1)+1

		end_num = group_member*seq

		if end_num > filenum:

			end_num = filenum

		i = start_num

		while i <= end_num:

			new_file_name = filename+'_part_'+str(i)

			f = open(new_file_name,'rb')

			while True:

				content = f.read(4096)

				if content:

					connectionSocket.send(content)

				else:

					f.close()

					break
			i = i+1
			print(new_file_name,'sent successful')



	#as a server

	def handle_chat(self,connectionSocket,con_addr):
		print(con_addr,'is connecting with me')
		print(con_addr[0],'is connected with you. Please enter your response. When you say "Bye!",the coversation ends.')
		print('Enter your response:')
		my_response = input()

		connectionSocket.send(str.encode(my_response))
		print("Please wait for your friend's response")
		other_greeting = connectionSocket.recv(4096)
		other_greeting = str(other_greeting.decode())
		print('con_addr[0]:',other_greeting)
		while other_greeting != 'Bye!':

			my_response = input('Enter you response:')
			connectionSocket.send(str.encode(my_response))
			if my_response == 'Bye!':
				break;
			print("Please wait for your friend's response")
			other_greeting = connectionSocket.recv(4096)
			other_greeting = str(other_greeting.decode())
			print('con_addr[0]:',other_greeting)



	def handle_file_transport(self,connectionSocket,con_addr):

		pass

	#as a server

	def listening_to_others(self):

		while True:

			connectionSocket, con_addr = self.peer_socket.accept()

			request_from_others = connectionSocket.recv(4096)

			request_from_others = str(request_from_others.decode())

			request_from_others = request_from_others.split(' ',4)
			print('request from others:',request_from_others)

			if request_from_others[0] == '1':
				print('I am going to handle download')

				filename = request_from_others[1]

				seq = request_from_others[2]
				seq = int(seq)
				total = request_from_others[4]
				total = int(total)
				self.handle_download(connectionSocket,con_addr,filename,seq,total)

			#chat with others

			elif request_from_others[0] == '2':
				print('I am going to handle chat')

				self.handle_chat(connectionSocket,con_addr)

			elif request_from_others[0] == '3':

				self.handle_file_transport(connectionSocket,con_addr)

			connectionSocket.close()



	def sending_out_request(self):

		print('What you want to do?')

		print('1.download_resource')

		print('2.chat with others')

		while True:

			print('What you want to do?')

			act = input()

			if act == '1':
				print('download')
				self.download_resource()

			elif act == '2':

				self.chat_with_sb()

			elif act == '3':

				pass
			else:
				print('Sorry, this is invalid')
		

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

		for i in range(filenum):

			file_split_name = filename+'_part_'+str(i+1)

			infile = open(file_split_name,'rb')

			data = infile.read()

			outfile.write(data)

			infile.close()

		outfile.close()



if __name__ == '__main__':

	my_peer = Peer('192.168.199.205',PEER_PORT)

	my_peer.register()
	my_peer.update_resource()
	try:
		t1 = threading.Thread(target = my_peer.listening_to_others)
		t2 = threading.Thread(target = my_peer.sending_out_request)
	except:
		print('Error:Unable to start thread')
	t1.start()
	t2.start()
	#my_peer.handle_peer()
	#my_peer.download_resource()
	#my_peer.listening_to_others()
	input()