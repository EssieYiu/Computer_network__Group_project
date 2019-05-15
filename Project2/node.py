import socket
import json
import random
BUFSIZE=1024
RECVPORT = 20000
SENDPORT = 30000
IP=["","","","",""]   #依次存储A,B,C,D,E的ip
INFINITE = 1000000
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
            self.recompute_DV(fhost,DVneighbour)
            #if self.recompute_DV(fhost,DVneighbour)==True:
                #self.exchange_DV()



    #重新计算DV信息
    def recompute_DV(self):
        #返回:当自己的DV改变了，返回True
        #此处针对一个邻居的DV变化
        change=False
        for key,value in self.DV:   #key为目的ip，value为从自己到目的地的cost
            next=self.table[key]
            for neighbour,linkCost in self.neighbour:   #neighbour为邻居的ip，linkCost为自己到邻居的cost
                DVneighbour=self.DV_neighbour[IP.index(neighbour)]  #该邻居的DV信息

                #add 处理宕掉的情况，若next恰好为邻居，且在邻居的DV表中发现到目的节点的路径为正无穷，那么说明路不通，
                # 在暂时未找到其他路径的情况下，将自己的也修改为正无穷
                if next == neighbour and DVneighbour[key] >= INFINITE:
                    value = INFINITE
                #add end

                if value>linkCost+DVneighbour[key]: #当前path cost>到邻居cost+邻居到目的地cost
                    value=linkCost+DVneighbour[key]
                    next=neighbour  #下一跳节点变为这个邻居
                    change=True
            self.neighbour[key] = value #add 将修改的value值写回去
            self.table[key]=next #目的地，下一跳节点变化
        
        if change==True:
            print("* My DV has changed!")
        return change

    #交换DV信息
    def send_DV(self):
        DVinfo=json.dumps(self.DV)
        for neigh in self.neighbour.keys():
            #给每一位邻居发送自己的DV信息
            self.sck_output.sendto(('0'+DVinfo).encode(),(neigh,RECVPORT))

        print("* Send DV message to all neighbours!")


    def pack_message(self,message,destIP):
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



