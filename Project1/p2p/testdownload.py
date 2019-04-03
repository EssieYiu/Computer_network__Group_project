from socket import*
import os
class Peer:
	def __init__(self,peer_ip,peer_port):
		self.ip = peer_ip
		self.port = peer_port
		self.peer_socket = socket(AF_INET,SOCK_STREAM)
		self.peer_socket.bind(('',peer_port))
		self.listen(5)

	def __del__(self):
		self.peer_socket.close()

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

				#self.chat_with_sb()

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

