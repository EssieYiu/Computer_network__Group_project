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
    def __init__(self,name='A',ip="127.0.0.1",neigh={},changeable=[],down=False):
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
        self.changeable_route =changeable #存储的是邻居的ip，表示它能够修改自身到这个邻居路径的权重，从拓扑图中获得
        self.down=down
       
        #初始化DV和table
        for dest in IP: #对于所有目的地ip
            print('dest',dest)
            print('self.ip',self.ip)
            if dest==self.ip:   #目的地是自己
                continue
            if dest in self.neighbour.keys():   #目的地是邻居，cost就是相连链路代价
                self.DV[dest]=self.neighbour[dest]
                self.table[dest]=dest
            else:
                self.DV[dest]=INFINITE #目的地不是邻居，cost设为，意味着还没有找到怎么去
                self.table[dest]="DK"

        print("self.DV:",self.DV)
        print("self.neighbour:",self.neighbour)
        print("self.changeable:",self.changeable_route)
        print("self.table:",self.table)
        print("* __init__ end！")
         
    #发送消息
    def send_message(self,message,dest):
        # destIP:string
        # message:string
        #message=input("Please enter the message you want to send:")
        #dest=input("Please enter the destination(A/B/C/D/E):")
        print("dest:",dest)
        print("message:",message)
        if dest==self.name or dest not in ALL:
            return "* Error: please enter another destination\n\n"
        destIP=IP[ALL.index(dest)]
        packed_message=self.pack_message(message,destIP)#打包消息
        print(packed_message)
        nextIP=self.table[destIP]
        if nextIP not in IP:
            return "* Error: cannot reach the destination!\n\n"
        nextNode=ALL[IP.index(nextIP)]
        cost=self.DV[destIP]
        if cost==INFINITE or nextNode=='DK':
           return "* Error: cannot reach the destination!\n\n"
        else:
            self.sck_output.sendto(packed_message,(nextIP,RECVPORT))
            towhere="* Message: "+message+"\n* To:"+dest+" "+destIP+'\n\n'
            first="* Firstly, send message to next node "+nextNode+": \n"+nextIP+'\n'
            if destIP!=nextIP:
                return first+towhere
                print(first+towhere)
            else:
                return towhere
                print(towhere)
           

    def recv(self):
        data,(fhost,fport)=self.sck_input.recvfrom(BUFSIZE)
        index=IP.index(fhost)
        omessage=data.decode()
       
        #接收到的是message
        if omessage[0]=='1':           
            tup=self.unpack_message(omessage)
            message=tup[3]
            destIP=tup[2]
            srcIP=tup[1]
            if destIP==self.ip:#目的地就是自己
                #print("Message:",message)
                print("* Message: "+message+'\n'+'From: '+srcIP+'\n\n')
                return (0,"* Message: "+message+'\n'+'* From: '+ALL[index]+' '+srcIP+'\n\n')
            
            else:#目的地不是自己
                #查路由表，转发
                nextIP=self.table[destIP]
                self.sck_output.sendto(data,(nextIP,RECVPORT))
                print('* Help sent message\n '+ 'Src: '+srcIP+'Dest'+destIP+'\n\n')
                return (1,'* Help sent message\n '+ 'Src: '+srcIP+'Dest'+destIP+'\n\n')

        #接收到的是邻居发来的DV信息
        elif omessage[0]=='0':
            DVneighbour=json.loads(omessage[1:])

            self.DV_neighbour[index]=DVneighbour
            print("* Received DV message from "+fhost+'\n'+'DVneighbour: '+str(DVneighbour)+'\n')
            self.recompute_DV()
            
            return(2,"* Received DV message from "+fhost+'\n'+'DVneighbour: '+str(DVneighbour)+'\n\n')


        #接收到的是邻居发来的link cost改变,更新self.neighbour
        elif omessage[0]=='2':
            new_weight=int((omessage.split(' ',2))[2])    #获得新的权重 ！！
            print("new_weight",new_weight)
            self.neighbour[fhost]=new_weight    #更新
            print("* New local link cost")
            self.recompute_DV() #重计算

            return(3,"* New local link cost to"+ALL[index]+" "+fhost+"\n")

        elif omessage[0]=='4':
            new_weight=int((omessage.split(' ',2))[2])    #获得新的权重 ！！
            print("new_weight",new_weight)
            self.neighbour[fhost]=new_weight    #更新
            print("* Neighbour "+ALL[index]+" "+fhost+" is back!\n")
            self.recompute_DV() #重计算
            return(3,"* Neighbour "+fhost+" is back!\n")
        #接收到邻居发来的
        elif omessage[0]=='3':
            self.neighbour[fhost]=INFINITE
            #self.DV_neighbour[index]={}
            print("* Neighbour "+fhost+" is down!\n")
            self.recompute_DV()
            return(3,"* Neighbour "+ALL[index]+" "+fhost+" is down!\n")


    #重新计算DV信息
    #重新计算DV信息
    def recompute_DV(self):
        #返回:当自己的DV改变了，返回True
        #前提是要有邻居的DV信息
        change=False
        for key in self.DV.keys():   #key为目的ip，value为从自己到目的地的cost  
            next=self.table.get(key,'DK')
            value=INFINITE
            for neigh,linkCost in self.neighbour.items():   #neighbour为邻居的ip，linkCost为自己到邻居的cost
                DVneighbour=self.DV_neighbour[IP.index(neigh)]  #该邻居的DV信息
                if not DVneighbour: #该邻居的DV信息为空，即邻居还没发DV信息，即邻居没上线
                    continue
                
                if value>linkCost+DVneighbour.get(key,0): #当前path cost>到邻居cost+邻居到目的地cost
                    value=linkCost+DVneighbour.get(key,0)
                    next=neigh  #下一跳节点变为这个邻居
                    
            if self.DV[key]!=value:
                change=True
                self.DV[key] = value #add 将修改的value值写回去
                self.table[key]=next #目的地，下一跳节点变化   
        if change==True:
            print("* My DV has changed!")

        print('my DV after recompute:',self.DV)
        print('my_table',self.table)
        return change

    #交换DV信息
    #需要周期性调用
    def send_DV(self):
        DVinfo=json.dumps(self.DV)
        for neigh in self.neighbour.keys():
            #给每一位邻居发送自己的DV信息
            self.sck_output.sendto(('0'+DVinfo).encode(),(neigh,RECVPORT))
        #print(self.DV)
        #return "* Send DV message to all neighbours!\n"


    def pack_message(self,message,destIP):
        message_to_send = '1 '+self.ip+' '+destIP+' '+message
        return message_to_send.encode()

    def unpack_message(self,message):
        #解读消息
        tup = (message).split(' ',3)
        return tup

    #仅仅修改了路径权重和通知邻居，没有调用重新计算DV的函数
    def change_route(self):
        #neibor为ip地址
        for neibor in self.changeable_route:
            new_weight = random.randint(1,50)
            self.neighbour[neibor] = new_weight #修改自身存储的到这个邻居路径的权重
            message = '2 route_weight_change '+str(new_weight)  #!!!信息格式未规范，需要后续修改
            self.sck_output.sendto(message.encode(),(neibor,RECVPORT)) #告知这个邻居
        self.recompute_DV()
        print("* Some link cost has changed!")
        print('my DV after change',self.DV)
        print('my_neighbour:',self.neighbour)
  

    def go_down(self):
        for neibor in self.neighbour.keys():    #告诉所有邻居我down了
           message='3'
           self.neighbour[neibor]=INFINITE
           self.sck_output.sendto(message.encode(),(neibor,RECVPORT))
        self.recompute_DV()
        print("* Down!")
        print('my DV after down',self.DV)
        print('my_neighbour',self.neighbour)

    def recover(self):
        for neibor in self.neighbour.keys():    #告诉所有邻居我back了
           new_weight = random.randint(1,50)
           self.neighbour[neibor] = new_weight #修改自身存储的到这个邻居路径的权重
           message = '4 route_recover '+str(new_weight)  #!!!信息格式未规范，需要后续修改
           self.sck_output.sendto(message.encode(),(neibor,RECVPORT))
        self.recompute_DV() #需要吗？？
        
        print("* Recover!")
        print('my DV after recover',self.DV)
        print('my_neighbour',self.neighbour)

