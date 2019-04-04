from socket import*
import os
class Peer:
	def __init__(self,peer_ip,peer_port):
		self.ip = peer_ip
		self.port = peer_port
		#self.peer_socket = socket(AF_INET,SOCK_STREAM)
		#self.peer_socket.bind(('',peer_port))
		#self.listen(5)

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


	def sending_out_request(self):

		print('What you want to do?')

		print('1.download_resource')

		print('2.chat with others')

		while True:

			print('What you want to do?')

			act = input()

			if act == 1:

				self.download_resource()

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

if __name__ == '__man__':
	my_peer = Peer('',PEER_PORT)
	my_peer.sending_out_request()