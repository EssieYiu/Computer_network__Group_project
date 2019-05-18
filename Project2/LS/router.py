import socket
import random
import copy
RECVPORT = 20000
SENDPORT = 30000
INF = 10000000
BUFFSIZE = 4096
TTL = 2
NAMELIST = ['A','B','C','D','E']
class router:
    def __init__(self,name = 'A',ip = "0.0.0.0",neigh = {},name_ip = {},init_topo = [[]],down_st=False):
        self.name_to_ip = name_ip #dict name->ip, neibour info,their name and address
        self.neighbour = copy.deepcopy(neigh) #dict neighbour_name->cost
        self.down_status = down_st
        self.topo = copy.deepcopy(init_topo) #adjacent matrix, store the map

        self.next_jump = {} #dict dst_name->next jump
        self.cost = {} #dict dst_name->cost

        self.sck_input = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_input.bind((ip,RECVPORT))
        self.sck_output = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sck_output.bind((ip,SENDPORT))

        self.name = name
        self.ip = ip


    #use the exsiting topo graph to compute next_jump and cost
    #dijkstra
    def LS_algorithm(self):
        dist = {} #dict node->distance from s,include myself
        prev = {} #dict node->previous node,not include myself
        for node in NAMELIST:
            dist[node] = INF
        dist[self.name] = 0
        queue = ['A','B','C','D','E']
        while len(queue):
            #deletemin
            cur_node = queue[0]
            for n in queue:
                if dist[n] < dist[cur_node]:
                    cur_node = n
            queue.remove(cur_node)
            for i in range(5):
                if dist[chr(i+ord('A'))] > dist[cur_node] + self.topo[ord(cur_node)-ord('A')][i]:
                    dist[chr(i+ord('A'))] = dist[cur_node] + self.topo[ord(cur_node)-ord('A')][i]
                    prev[chr(i+ord('A'))] = cur_node  
        for node in NAMELIST:
            if node != self.name:
                self.cost[node] = dist[node]
                next_temp = node
                while self.neighbour.get(next_temp,0) == 0:
                    next_temp = prev[next_temp]
                self.next_jump[node] = next_temp

    def handle_receive(self):
        data,(fhost,fport) = self.sck_input.recvfrom(BUFFSIZE)
        message = data.decode()
        message = message.split(' ',4)
        #meaningful message, decide whether to send or print
        if message[0] == '0':
            if message[2] == self.ip:
                print("Receive message from",message[1],'debug:',fhost)
                print(message[3])
            else:
                print("Help forward message from",message[1],"to",message[2])
                dst = message[2]
                if dst == "":
                    print('Dst not exist')
                else:
                    self.sck_output.sendto(data,(dst,RECVPORT))
        #broadcast route weight, change topo and neighbour
        elif message[0] == '1':
            host1 = message[1]
            host2 = message[2]
            weight = int (message[3])
            self.topo[ord(host1)-ord('A')][ord(host2)-ord('A')] = weight
            #only receive neibour down or recover info will enter this if
            if host1 == self.ip:
                self.neighbour[host1] = weight
                print('one of my neibour down/recover,my route to it now:',weight)
            #forward out, send to all its neighbour,with TTL -1
            if int(message[4]) > 0:
                message[4] = str(int(message[4]) - 1)
                message = ' '.join(message)
                for node in NAMELIST:
                    if self.neighbour.get(node,0):
                        next_stop = self.next_jump[node]
                        next_stop_ip = self.name_to_ip[next_stop]
                        if next_stop_ip == "":
                            print('Dst not exist')
                        else:
                            self.sck_output.sendto(message.encode(),(next_stop_ip,RECVPORT))

    def send_meaningful_message(self):
        message = input("Please enter your message to send")
        dst = input("Please enter the destination(A/B/C/D/E),but not yourself:")
        if dst not in NAMELIST:
            print("Invalid destionation!")
        elif dst == self.name:
            print("You should not send message to yourself")
        else:
            pack_msg = '0 '+self.ip+' '+self.name_to_ip[dst]+' '+message
            next_stop = self.next_jump[dst]
            if self.cost[dst] >= INF:
                print("Send message failed,destination can not reach")
            else:
                self.sck_output.sendto(pack_msg.encode(),(self.name_to_ip[next_stop],RECVPORT))
                print("Sending message to",dst)
                print("Firstly send to",next_stop)

    #broadcast all the linking route,first send to its neibour
    def broadcast(self):
        for node in NAMELIST:
            if self.neighbour.get(node,0):
                route_info = '1 '+self.name+' '+node+' '+str(self.cost[node])+' '+str(TTL)
                if self.name_to_ip[node] == "":
                    print("Dst not exist")
                else:
                    self.sck_output.sendto(route_info.encode(),(self.name_to_ip[node],RECVPORT))
        print("Broadcast my route info")

    #only change its own topo and neighbour info,
    #can use broadcast to tell others about change
    def change_route(self):
        for node in NAMELIST:
            if self.neighbour.get(node,0):
                new_weight = random.randint(0,50)
                self.neighbour[node] = new_weight
                self.topo[ord(self.name)-ord('A')][ord(node)-ord('A')] = new_weight

    #notice that once if down, can not change route anymore
    def down(self):
        for node in NAMELIST:
            if self.neighbour.get(node,0):
                self.neighbour[node] = INF
                self.topo[ord(node)-ord('A')][ord(self.name)-ord('A')] = INF
                self.topo[ord(self.name)-ord('A')][ord(node)-ord('A')] = INF
                if self.name_to_ip[node] == "":
                    print('Dst not exist')
                else:
                    route_info = '1 '+self.name+' '+node+' '+str(INF)+' '+str(TTL)
                    self.sck_output.sendto(route_info.encode(),(self.name_to_ip[node],RECVPORT))
                    route_info = '1 '+node+' '+self.name+' '+str(INF)+' '+str(TTL)
                    self.sck_output.sendto(route_info.encode(),(self.name_to_ip[node],RECVPORT))

    #recover two edges at the same time
    def recover(self):
        for node in NAMELIST:
            if self.neighbour.get(node,0):
                recover_weight = random.randint(0,50)
                self.neighbour[node] = recover_weight
                self.topo[ord(node)-ord('A')][ord(self.name)-ord('A')] = recover_weight
                self.topo[ord(self.name)-ord('A')][ord(node)-ord('A')] = recover_weight
                if self.name_to_ip[node] == "":
                    print("Dst not exist")
                else:
                    route_info = '1 '+self.name+' '+node+' '+str(recover_weight)+' '+str(TTL)
                    self.sck_output.sendto(route_info.encode(),(self.name_to_ip[node],RECVPORT))
                    route_info = '1 '+node+' '+self.name+' '+str(recover_weight)+' '+str(TTL)
                    self.sck_output.sendto(route_info.encode(),(self.name_to_ip[node],RECVPORT))