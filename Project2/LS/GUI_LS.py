from router import router
from LSGraph import LSGraph
from tkinter import *
import threading
import time
lock = threading.RLock() 
if __name__ == "__main__":
    root = Tk()

    my_name = 'E'
    my_ip = '192.168.199.102'
    Graph = LSGraph()
    name_ip = Graph.get_name_ip()
    init_topo = Graph.get_init_topo()
    neibour = Graph.get_neighbour(my_name)
    down_st = Graph.get_down_status(my_name)
    my_router = router(my_name,my_ip,neibour,name_ip,init_topo,down_st)

    print('router topo:',my_router.topo)
    print('router neibour:',my_router.neighbour)
    print('router name_ip:',my_router.name_to_ip)

    my_router.LS_algorithm()
    print('router cost:',my_router.cost)
    print('router next jump:',my_router.next_jump)
    my_router.broadcast()

    label_ip = Label(root,text="my ip address")
    label_name = Label(root,text="my name")
    label_ip.pack()
    label_name.pack()