import socket
import json
import random
BUFSIZE=1024
RECVPORT = 8080
SENDPORT = 8081
IP=["192.168.199.131","192.168.199.165","127.0.0.1","192.168.199.205","192.168.199.102"]   #依次存储A,B,C,D,E的ip
ALL="ABCDE"
INFINITE=200
class Node(object):
    def __init__(self,name='A',ip="127.0.0.1",neigh={},changeable=[]):
        print("* Node __init__ begins！")
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
       
        #初始化DV和table
        for dest in IP: #对于所有目的地ip
            if dest==self.ip:   #目的地是自己
                continue
            if dest in self.neighbour.keys():   #目的地是邻居，cost就是相连链路代价
                self.DV[dest]=self.neighbour[dest]
                self.table[dest]=dest
            else:
                self.DV[dest]=INFINITE #目的地不是邻居，cost设为，意味着还没有找到怎么去
                self.table[dest]="None"
        
        print("self.DV:",self.DV)
        print("self.neighbour:",self.neighbour)
        print("self.changeable:",self.changeable_route)
        print("self.table:",self.table)
        print("* Node __init__ ends！")
         
    #发送消息
    def send_message(self,message,dest):
        # destIP:string
        # message:string
        #message=input("Please enter the message you want to send:")
        #dest=input("Please enter the destination(A/B/C/D/E):")
        print("\nsend message:")
        print("dest:",dest)
        print("message:",message)
        if dest==self.name or dest not in ALL:
            return "Error: please enter another destination\n\n"
        destIP=IP[ALL.index(dest)]
        packed_message=self.pack_message(message,destIP)#打包消息

        print("packed_message:",packed_message)
        nextIP=self.table[destIP]
        if nextIP not in IP:
            return "Error: cannot reach the destination!\n\n"
        nextNode=ALL[IP.index(nextIP)]
        cost=self.DV[destIP]
        if cost>=INFINITE or nextNode=='None':
           return "Error: cannot reach the destination!\n\n"
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
        #index=IP.index(fhost)
        #fname=ALL[index]
        omessage=data.decode()
       
        #接收到的是message
        if omessage[0]=='1':           
            tup=self.unpack_message(omessage)
            message=tup[3]
            destIP=tup[2]
            srcIP=tup[1]
            src_name=ALL[IP.index(srcIP)]
            dest_name=ALL[IP.index(destIP)]
            if destIP==self.ip:#目的地就是自己
                #print("Message:",message)
                print("\n* Message: "+message+'\n'+'* From: '+srcIP+'\n\n')
                return (0,"* Message: "+message+'\n'+'* From: '+src_name+' '+srcIP+'\n\n')
            
            else:#目的地不是自己
                #查路由表，转发
                nextIP=self.table[destIP]
                self.sck_output.sendto(data,(nextIP,RECVPORT))
                print('\n* Help sent message\n '+ 'Src: '+srcIP+' Dest: '+destIP+'\n\n')
                return (1,'* Help sent message\n '+ 'Src: '+src_name+' Dest: '+dest_name+'\n\n')

        #接收到的是邻居发来的DV信息
        elif omessage[0]=='0':
            tup=omessage.split(' ',2)
            DVneighbour=json.loads(tup[2])
            tmp_name=tup[1]
            tmp_index=ALL.index(tmp_name)
            tmp_ip=IP[tmp_index]
            self.DV_neighbour[tmp_index]=DVneighbour
            print("\n* Received DV message from "+tmp_name+' '+tmp_ip+'\n'+'DVneighbour: '+str(DVneighbour)+'\n')
            self.recompute_DV()
            return(2,"")


        #接收到的是邻居发来的link cost改变,更新self.neighbour
        elif omessage[0]=='2':
            tup=omessage.split(' ',2)
            tmp_name=tup[1]
            tmp_index=ALL.index(tmp_name)
            tmp_ip=IP[tmp_index]
            new_weight=int(tup[2])    #获得新的权重 ！！
            print("new_weight",new_weight)
            self.neighbour[tmp_ip]=new_weight    #更新
            print("\n* New local link cost\n")
            self.recompute_DV() #重计算
            return(3,"New local link cost to"+tmp_name)
   
        #接收到邻居发来的down
        elif omessage[0]=='3':
            tup=omessage.split(' ',1)
            tmp_name=tup[1]
            tmp_index=ALL.index(tmp_name)
            tmp_ip=IP[tmp_index]
            self.neighbour[tmp_ip]=INFINITE
            print("\n* Neighbour "+tmp_name+" is down!\n")
            self.recompute_DV()
            return(3,"Neighbour "+tmp_name+" is down!")

        #接收到邻居发来的recover
        elif omessage[0]=='4':
            tup=omessage.split(' ',2)
            tmp_name=tup[1]
            tmp_index=ALL.index(tmp_name)
            tmp_ip=IP[tmp_index]
            new_weight=int(tup[2])    #获得新的权重 ！！      
            print("new_weight",new_weight)
            self.neighbour[tmp_ip]=new_weight    #到这个邻居的cost 更新
            print("\n* Neighbour "+tmp_name+" "+tmp_ip+" is back!\n")
            self.recompute_DV() #重计算
            return(3,"Neighbour "+tmp_name+" is back!")

    #重新计算DV信息
    #重新计算DV信息
    def recompute_DV(self):
        #返回:当自己的DV改变了，返回True
        #前提是要有邻居的DV信息
        change=False
        for key in self.DV.keys():   #key为目的ip，value为从自己到目的地的cost  
            next=self.table.get(key,'None')
            value=INFINITE
            for neigh,linkCost in self.neighbour.items():   #neighbour为邻居的ip，linkCost为自己到邻居的cost
                DVneighbour=self.DV_neighbour[IP.index(neigh)]  #该邻居的DV信息
                if not DVneighbour: #该邻居的DV信息为空，即邻居还没发DV信息，即邻居没上线
                    continue
                
                if value>linkCost+DVneighbour.get(key,0): #当前path cost>到邻居cost+邻居到目的地cost
                    value=linkCost+DVneighbour.get(key,0)
                    next=neigh  #下一跳节点变为这个邻居
                    
            #if self.DV[key]!=value:
            change=True
            self.DV[key] = value #add 将修改的value值写回去
            self.table[key]=next #目的地，下一跳节点变化   
        if change==True:
            print("* My DV has changed!")

        print('my DV after recompute:',self.DV)
        print('my_table',self.table)
        print('\n\n')
        return change

    #交换DV信息
    #需要周期性调用
    def send_DV(self):
        DVinfo=json.dumps(self.DV)
        for neigh in self.neighbour.keys():
            #给每一位邻居发送自己的DV信息
            self.sck_output.sendto(('0 '+self.name+' '+DVinfo).encode(),(neigh,RECVPORT))
        print("\n* Send DV message to all neighbours!")
        print("my_DV",self.DV)
        print("my_table",self.table)
        print('my neighbour',self.neighbour)
        #return "* Send DV message to all neighbours!\n"


    def pack_message(self,message,destIP):
        message_to_send = '1 '+self.ip+' '+destIP+' '+message   #类型_自己ip_目的ip_消息
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
            message = '2 '+self.name+' '+str(new_weight)  #类型_名字_新权重
            self.sck_output.sendto(message.encode(),(neibor,RECVPORT)) #告知这个邻居
        self.recompute_DV()
        print("* Some link cost has changed!")
        print('my DV after change',self.DV)
        print('my_neighbour:',self.neighbour)
  

    def go_down(self):
        for neibor in self.neighbour.keys():    #告诉所有邻居我down了
           message='3 '+self.name   #类型_名字
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
           message = '4 '+self.name+' '+str(new_weight)  #类型_名字_新权重
           self.sck_output.sendto(message.encode(),(neibor,RECVPORT))
        self.recompute_DV() #需要吗？？
        
        print("* Recover!")
        print('my DV after recover',self.DV)
        print('my_neighbour',self.neighbour)

