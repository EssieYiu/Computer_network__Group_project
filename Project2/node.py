import socket
import json
import random
BUFSIZE=1024
RECVPORT = 8080
SENDPORT = 8081
IP=["192.168.199.131","127.0.0.2","127.0.0.1","192.168.199.205","192.168.199.102"]   #依次存储A,B,C,D,E的ip
ALL="ABCDE"
INFINITE=1000000
class Node(object):
    def __init__(self,name='A',ip="127.0.0.1",neigh={},down=False):
        #收套接字
        self.sck_input=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_input.bind((ip,RECVPORT))
        #发套接字
        self.sck_output=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_output.bind((ip,SENDPORT))
        
        self.name=name
        self.ip=ip #ip
        self.neighbour=neigh   #邻居->link cost
        self.table={}   #路由表：目的node->应该去的下一跳node
        self.DV={}  #Distance vector：node->最佳路径开销
        self.DV_neighbour=[{},{},{},{},{}]    #存储邻居的DV信息(即邻居的self.DV字典），为list，依次为A,B,C,D,E
        self.changeable_route =[] #存储的是邻居的ip，表示它能够修改自身到这个邻居路径的权重，从拓扑图中获得
        self.down=down

        print(self.neighbour)
        print(self.ip)
        print(self.down)
       
        #初始化DV和table
        for dest in IP: #对于所有目的地ip
            if dest==self.ip:   #目的地是自己
                continue
            if dest in self.neighbour.keys():   #目的地是邻居，cost就是相连链路代价
                self.DV[dest]=self.neighbour[dest]
                self.table[dest]=dest
            else:
                self.DV[dest]=INFINITE #目的地不是邻居，cost设为0，意味着还没有找到怎么去
                self.table[dest]="127.0.0.1"

        print("self.DV:")
        print(self.DV)
        print("self.neighbour:")
        print(self.neighbour)
        print("self.table:")
        print(self.table)
        print("* __init__ end！")
         
    #发送消息
    def send_message(self):
        # destIP:string
        # message:string
        message=input("Please enter the message you want to send:")
        dest=input("Please enter the destination(A/B/C/D/E):")
        while dest==self.name:
            dest=input("You can't send message to yourself, please enter another destination: ")
        destIP=IP[ALL.index(dest)]
        packed_message=self.pack_message(message,destIP)#打包消息

        nextIP=self.table[destIP]
        nextNode=ALL[IP.index(nextIP)]
        cost=self.DV[destIP]
        if cost==INFINITE:
           print("Cannot reach the destination, send failed!")
        else:
            self.sck_output.sendto(packed_message,(nextIP,RECVPORT))
            if destIP!=nextIP:
                print("* Firstly, send message to next node %s: %s"%(nextNode,nextIP))
        print("* Send message to %s: %s"%(dest,destIP))

    def recv(self):
        data,(fhost,fport)=self.sck_input.recvfrom(BUFSIZE)
        index=IP.index(fhost)
        omessage=data.decode()
        print(omessage)
        #接收到的是message
        if omessage[0]=='1':
            
            tup=self.unpack_message(omessage)
            message=tup[2]
            destIP=tup[1]
            srcIP=tup[0]
            print(message)
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
            
            self.DV_neighbour[index]=DVneighbour
            print("Receive DVneighbour:")
            print(DVneighbour)
            self.recompute_DV()
            #if self.recompute_DV(fhost,DVneighbour)==True:
                #self.exchange_DV()

        #接收到的是邻居发来的link cost改变,更新self.neighbour
        elif omessage[0]=='2':
            new_weight=omessage[1:].split(' ',2)    #获得新的权重 ！！！还没修改好
            self.neighbour[fhost]=new_weight    #更新
            self.recompute_DV() #重计算

        #接收到邻居发来的
        elif omessage[0]=='3':
            self.neighbour[fhost]=INFINITE
            #self.DV_neighbour[index]={}
            self.recompute_DV()


    #重新计算DV信息
    #重新计算DV信息
    def recompute_DV(self):
        #返回:当自己的DV改变了，返回True
        #前提是要有邻居的DV信息
        change=False
        for key in self.DV.keys():   #key为目的ip，value为从自己到目的地的cost  
            next=self.table.get(key,'DK')
            value=INFINITE
            for neighbour,linkCost in self.neighbour.items():   #neighbour为邻居的ip，linkCost为自己到邻居的cost
                DVneighbour=self.DV_neighbour[IP.index(neighbour)]  #该邻居的DV信息
                if not DVneighbour:
                    continue
                #add 处理宕掉的情况，若next恰好为邻居，且在邻居的DV表中发现到目的节点的路径为正无穷，那么说明路不通，
                # 在暂时未找到其他路径的情况下，将自己的也修改为正无穷
                #if next == neighbour and DVneighbour[key] >= INFINITE:
                    #value = INFINITE
                #add end
                if value>linkCost+DVneighbour.get(key,0): #当前path cost>到邻居cost+邻居到目的地cost
                    value=linkCost+DVneighbour.get(key,0)
                    next=neighbour  #下一跳节点变为这个邻居
                    change=True

            self.DV[key] = value #add 将修改的value值写回去
            self.table[key]=next #目的地，下一跳节点变化   
        if change==True:
            print("* My DV has changed!")

        print(self.DV)
        return change

    #交换DV信息
    #需要周期性调用
    def send_DV(self):
        DVinfo=json.dumps(self.DV)
        for neigh in self.neighbour.keys():
            #给每一位邻居发送自己的DV信息
            self.sck_output.sendto(('0'+DVinfo).encode(),(neigh,RECVPORT))
        #print(self.DV)
        print("* Send DV message to all neighbours!")


    def pack_message(self,message,destIP):
        message_to_send = '1 '+self.ip+' '+destIP+' '+message
        return message_to_send.encode()

    def unpack_message(self,message):
        #解读消息

        tup = message[1:].split(' ',2)
        return tup

    #仅仅修改了路径权重和通知邻居，没有调用重新计算DV的函数
    def change_route(self):
        #neibor为ip地址
        for neibor in self.changeable_route:
            new_weight = random.randint(0,50)
            self.neighbour[neibor] = new_weight #修改自身存储的到这个邻居路径的权重
            message = '2 route_weight_change '+str(new_weight)  #!!!信息格式未规范，需要后续修改
            self.sck_output.sendto(message.encode(),(neibor,RECVPORT)) #告知这个邻居

    def go_down(self):
        for neibor in self.DV_neighbour:    #告诉所有邻居我down了
           message='3'
           self.sck_output.sendto(message.encode(),(neibor,RECVPORT))

