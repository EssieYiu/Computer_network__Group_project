import socket
import json
BUFSIZE=1024
class Node():
    def __init__(self,name='A',IP="127.0.0.1", port1=50500,port2=50501):
        #收套接字
        self.sck_input=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sck_input.bind((IP,port1))
        #发套接字
        self.sck_output=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sck_output.bind((IP,port2))
        
        self.ip=IP  #ip
        self.neighbour={}   #邻居->link cost
        self.table={}   #路由表：目的node->应该去的下一跳node
        self.DV={}  #Distance vector：node->最佳路径开销

    #发送消息
    def send_message(self):
        # destIP:string
        # message:string
        message=input("Please enter the message you want to send:")
        destIP=input("Please enter the destination IP:")
        packed_message=pack_message(self,message,destIP)#打包消息

        #如果destIP就是邻居，直接发送
        if destIP in self.neighbour.keys():
            sck_output.sendto(packed_message,(destIP,recvPort))
        #不是邻居，查找路由表，送到下一跳node
        else:
            nextNode=self.table[destIP]
            sck_output.sendto(packed_message,(nextNode,recvPort))
            print("Firstly, send message to next node:%s"%nextNode)

        print("Send message to %s"%destIP)

    def recv(self):
        data,(fhost,fport)=sck_input.recvfrom(BUFSIZE)
        #接收到的是message
        omessage=data.decode()
        if omessage[0]=='1':
            tup=unpack_message(omessage)
            message=tup[2]
            destIP=tup[1]
            srcIP=tup[0]
            if(destIP==self.ip):#目的地就是自己
                print("* Message from %s: %s"%(srcIP,message))
            else:#目的地不是自己
                #查路由表，转发
                nextIP=self.table[destIP]
                self.sck_output.sendto(message,(nextIP,recvPort))
                print("* Help sent message from %s"%srcIP)

        #接收到的是邻居发来的DV信息
        elif omessage[0]=='0':
            DVneighbour=json.loads(omessage[1:])
            print("* Received DV message from %s"%fhost)
            if recompute_DV(self,fhost,DVneighbour)==True:
                exchange_DV(self)



    #重新计算DV信息
    def recompute_DV(self,neigh,DVneigh):
        #neigh:邻居的IP
        #DVneigh:邻居的DV信息 key是邻居可达node的IP，value是路径开销
        #返回:当自己的DV改变了，返回True

        change=False
        cost=self.neighbour[neigh]  #到邻居的开销
        for key,value in DVneigh:
            if self.DV.get(key,1000000)>cost+value:
                self.DV[key]=cost+value
                change=True
        
        if change==True:
            print("* My DV has changed!")
        return change

    #交换DV信息
    def exchange_DV(self):
        DVinfo=json.dumps(self.DV)
        for neigh in self.neighbour.keys():
            #给每一位邻居发送自己的DV信息
            sck_output.sendto(('0'+DVinfo).encode(),(neigh,recvPort))

        print("* Send DV message to all neighbours!")


    def pack_message(self,message,destIP):
        # IP无论如何都用15位表示，不够的后面补'.0000'
        addition='00000000'
        if len(destIP)<15:
            need=15-len(destIP)-1#要补的0的个数
            zero=addition[:need-1]#后面要补的0
            dIP=destIP+'.'+zero
        srcIP=self.ip
        if len(srcip)<15:
            need=15-len(srcIP)-1
            zero=addition[:need-1]
            sIP=srcIP+'.'+zero

        packed_message='1'+sIP+dIP+message   #最前面的'1'代表发送的信息为消息 0 1:15 16:30
        return packed_message.encode()

    def unpack_message(self,message):
        #解读消息
        tup=(message[1:15],message[16:30],message[31:]) #srcIP,destIP,message
        return tup



