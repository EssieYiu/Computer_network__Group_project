from router import router
from LSGraph import LSGraph
from tkinter import *
import threading
import time
NAMELIST =['A','B','C','D','E']
lock = threading.RLock() 
#计算完路由之后及时更新显示表的信息
def compute_LS(routerA,LB):
    while 1:
        time.sleep(2)
        routerA.LS_algorithm()
        LB.delete(0,END)
        head_info = "dest  cost  next jump"
        LB.insert(END,head_info)
        for n in NAMELIST:
            if n != routerA.name:
                route_info = ' '+n+'     '+str(routerA.cost[n])+'       '+routerA.next_jump[n]
                LB.insert(END,route_info)
        print("Recompute LS. cost:",routerA.cost)
        print('next jump:',routerA.next_jump)
def down(routerA, msg_var):
    if routerA.down_status == False:
        msg_var.set("I am going down!")
        routerA.down()
        routerA.down_status = True
    else:
        msg_var.set("I have already gone down!")
def recover(routerA,msg_var):
    if routerA.down_status == True:
        msg_var.set("I now recover!")
        routerA.recover()
        routerA.down_status = False
    else:
        msg_var.set("I am well, no need to recover")
def change_road(routerA,msg_var):
    msg_var.set("I chagne the route")
    routerA.change_route()
def send_message(routerA,msg_send,dst_send):
    msg = msg_send.get()
    dst = dst_send.get()
    routerA.send_meaningful_message(msg,dst)
def receive(routerA,receive_text):
    while 1:
        lock.acquire()
        msg = routerA.handle_receive()
        lock.release()
        receive_text.insert(msg)
def broadcast_route(routerA):
    while 1:
        lock.acquire()
        routerA.broadcast()
        lock.release()
        time.sleep(5)

if __name__ == "__main__":
    root = Tk()

    my_name = 'D'
    #my_ip = '192.168.199.102'
    my_ip = '172.19.73.186'
    Graph = LSGraph()
    name_ip = Graph.get_name_ip()
    init_topo = Graph.get_init_topo()
    neibour = Graph.get_neighbour(my_name)
    down_st = Graph.get_down_status(my_name)
    my_router = router(my_name,my_ip,neibour,name_ip,init_topo,False)

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

    msg_var = StringVar()
    status_msg = Label(root,text="Here is the status msg",textvariable = msg_var)
    status_msg.pack()

    route_info_list = Listbox(root)
    route_info_list.pack()

    down_Btn = Button(root,text="down",command = lambda:down(my_router,msg_var))
    down_Btn.pack()
    recover_Btn = Button(root,text="recover",command = lambda:recover(my_router,msg_var))
    recover_Btn.pack()
    change_route_Btn = Button(root,text="change route",command = lambda:change_road(my_router,msg_var))
    change_route_Btn.pack()

    Label(root,text="msg send").pack()
    msg_send = Entry(root)
    msg_send.pack()

    Label(root,text="dst send").pack()
    dst_send = Entry(root)
    dst_send.pack()

    send_Btn = Button(root,text="send message",command = lambda:send_message(my_router,msg_send,dst_send))
    send_Btn.pack()

    receive_info = Text(root)
    receive_info.pack()

    my_thread = []
    Thread1 = threading.Thread(target=broadcast_route,args=(my_router,))
    my_thread.append(Thread1)
    Thread2 = threading.Thread(target=compute_LS,args=(my_router,route_info_list))
    my_thread.append(Thread2)
    Thread3 = threading.Thread(target=receive,args=(my_router,receive_info))
    my_thread.append(Thread3)

    for t in my_thread:
        t.setDaemon(True)
        t.start()
    root.mainloop()