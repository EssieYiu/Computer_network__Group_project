from node import Node
from TopoGraph import TopoGraph
import threading
import time
def sendDV_period(node):
    while 1:
        node.send_DV()
        time.sleep(10)
def change_period(node):
    while 1:
        time.sleep(180)
        node.change_route()
        
    #my_ip = input('Please enter your ip address')
    #my_name = input('Please enter your name')
my_ip="172.19.112.247"
my_name='A'
Graph = TopoGraph()
Graph.initialize_graph()
neighbour=Graph.get_allNeighbour(my_name)
down=Graph.get_down(my_name)
my_node = Node(my_name,my_ip,neighbour,down)

    #线程共用的：my_node的sck_output
    #1.周期性发送DV消息
    #send_DV:sendto
my_thread=[]
DVthread=threading.Thread(target=sendDV_period,args=(my_node,))
my_thread.append(DVthread)
#DVthread.start()

    #2.接收
    #涉及帮忙转发:sendto
Rthread=threading.Thread(target=my_node.recv,args=())
my_thread.append(Rthread)
#Rthread.start()

    #3.发送消息
    #send_message:sendto
Sthread=threading.Thread(target=my_node.send_message,args=())
my_thread.append(Sthread)
#Sthread.start()
   
    #4.周期性更改链路代价
    #change_route:sendto
Cthread=threading.Thread(target=change_period,args=(my_node,))
my_thread.append(Cthread)
#Cthread.start()
for thread in my_thread:
    thread.start()

for thread in my_thread:
    thread.join()



    



    #my_node.DV_neighbour=[{},{my_ip:10,'E':1},{},{},{my_ip:2,'B':1}]
    #my_node.neighbour={'E':2,'B':10}
   # my_node.initial_DV()
    #print(my_node.neighbour)
    #print(my_node.DV_neighbour)
    #print(my_node.DV)
    #print(my_node.table)
    #my_node.recompute_DV()
    #my_node.send_DV()
    #my_node.recv()
   # my_node.recompute_DV()


    
