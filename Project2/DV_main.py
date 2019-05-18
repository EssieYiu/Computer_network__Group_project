from node import Node
from TopoGraph import TopoGraph
import threading
import time
def sendDV_period(node):
    while 1:
        node.send_DV()
        print(node.table)
        time.sleep(10)
def change_period(node):
    while 1:
        time.sleep(20)
        node.change_route()
        print("after change:",node.neighbour)
def sendMessage(node):
    while 1:
        node.send_message()
def recv(node):
    while 1:
        node.recv()
    #my_ip = input('Please enter your ip address')
    #my_name = input('Please enter your name')
my_ip="192.168.199.102"
my_name='E'
Graph = TopoGraph()
Graph.initialize_graph()
neighbour=Graph.get_allNeighbour(my_name)
down=Graph.get_down(my_name)
changeable=Graph.node_changeable_route(my_ip)
print("changeable route:",changeable)
my_node = Node(my_name,my_ip,neighbour,changeable,down)
my_node.neighbour={'192.168.199.131':34}
my_node.DV['127.0.0.1']=1000000
my_node.DV['127.0.0.2']=1000000

my_thread=[]
    #线程共用的：my_node的sck_output

    #1.周期性发送DV消息
    #send_DV:sendto
DVthread=threading.Thread(target=sendDV_period,args=(my_node,))
my_thread.append(DVthread)
#DVthread.start()

    #2.接收
    #涉及帮忙转发:sendto
Rthread=threading.Thread(target=recv,args=(my_node,))
my_thread.append(Rthread)
#Rthread.start()

    #3.发送消息
    #send_message:sendto
Sthread=threading.Thread(target=sendMessage,args=(my_node,))
my_thread.append(Sthread)
#Sthread.start()
   
    #4.周期性更改链路代价
    #change_route:sendto
Cthread=threading.Thread(target=change_period,args=(my_node,))
my_thread.append(Cthread)
#Cthread.start()
for thread in my_thread:
    time.sleep(3)
    thread.start()

for thread in my_thread:
    thread.join()



    



    #my_node.DV_neighbour=[{},{my_ip:10,'E':1},{},{},{my_ip:2,'B':1}]
    
    #my_node.initial_DV()
    #print(my_node.neighbour)
    #print(my_node.DV_neighbour)
    #print(my_node.DV)
    #print(my_node.table)
    #my_node.recompute_DV()
    #my_node.send_DV()
    #my_node.recv()
   # my_node.recompute_DV()


    
