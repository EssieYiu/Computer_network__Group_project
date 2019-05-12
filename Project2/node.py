import socket
import json
import random
BUFSIZE=1024
RECVPORT = 20000
SENDPORT = 30000
IP=["","","","",""]   #依次存储A,B,C,D,E的ip
class Node(object):
    def __init__(self,name='A',IP="127.0.0.1"):
        #收套接字
        self.sck_input=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_input.bind((IP,RECVPORT))
        #发套接字
        self.sck_output=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_output.bind((IP,SENDPORT))
        
        self.ip=IP  #ip
        self.neighbour={}   #邻居->link cost
        self.table={}   #路由表：目的node->应该去的下一跳node
        self.DV={}  #Distance vector：node->最佳路径开销
        self.DV_neighbour=[{},{},{},{},{}]    #存储邻居的DV信息(即邻居的self.DV字典），为list，依次为A,B,C,D,E
        self.changeable_route =[] #存储的是邻居的ip，表示它能够修改自身到这个邻居路径的权重，从拓扑图中获得

    #发送消息
    def send_message(self):
        # destIP:string
        # message:string
        message=input("Please enter the message you want to send:")
        destIP=input("Please enter the destination IP:")
        packed_message=self.pack_message(message,destIP)#打包消息

        #如果destIP就是邻居，直接发送
        if destIP in self.neighbour.keys():
            self.sck_output.sendto(packed_message,(destIP,RECVPORT))
        #不是邻居，查找路由表，送到下一跳node
        else:
            nextNode=self.table[destIP]
            self.sck_output.sendto(packed_message,(nextNode,RECVPORT))
            print("Firstly, send message to next node:%s"%nextNode)

        print("Send message to %s"%destIP)

    def recv(self):
        data,(fhost,fport)=self.sck_input.recvfrom(BUFSIZE)
        #接收到的是message
        omessage=data.decode()
        if omessage[0]=='1':
            tup=self.unpack_message(omessage)
            message=tup[2]
            destIP=tup[1]
            srcIP=tup[0]
            if(destIP==self.ip):#目的地就是自己
                print("* Message from %s: %s"%(srcIP,message))
            else:#目的地不是自己
                #查路由表，转发
                nextIP=self.table[destIP]
                self.sck_output.sendto(message,(nextIP,RECVPORT))
                print("* Help sent message from %s"%srcIP)

        #接收到的是邻居发来的DV信息
        elif omessage[0]=='0':
            DVneighbour=json.loads(omessage[1:])
            print("* Received DV message from %s"%fhost)
            index=IP.find(fhost)
            self.DV_neighbour[index]=DVneighbour
            if self.recompute_DV(fhost,DVneighbour)==True:
                self.exchange_DV()



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
            self.sck_output.sendto(('0'+DVinfo).encode(),(neigh,RECVPORT))

        print("* Send DV message to all neighbours!")


    def pack_message(self,message,destIP):
        '''
        # IP无论如何都用15位表示，不够的后面补'.0000'
        addition='00000000'
        if len(destIP)<15:
            need=15-len(destIP)-1#要补的0的个数
            zero=addition[:need-1]#后面要补的0
            dIP=destIP+'.'+zero
        srcIP=self.ip
        if len(srcIP)<15:
            need=15-len(srcIP)-1
            zero=addition[:need-1]
            sIP=srcIP+'.'+zero

        packed_message='1'+sIP+dIP+message   #最前面的'1'代表发送的信息为消息 0 1:15 16:30
        return packed_message.encode()
        '''
        
        message_to_send = '1 '+self.ip+' '+destIP+' '+message
        return message_to_send

    def unpack_message(self,message):
        '''
        #解读消息
        tup=(message[1:15],message[16:30],message[31:]) #srcIP,destIP,message
        return tup
        '''
        tup = message[1:].split(' ',2)
        return tup

    #仅仅修改了路径权重和通知邻居，没有调用重新计算DV的函数
    def change_route(self):
        #neibor为ip地址
        for neibor in self.changeable_route:
            new_weight = random.randint(0,50)
            self.neighbour[neibor] = new_weight #修改自身存储的到这个邻居路径的权重
            message = '2 route_weight_change '+str(new_weight)  #!!!信息格式未规范，需要后续修改
            self.sck_output.sendto(message,neibor) #告知这个邻居



