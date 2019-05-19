from router import router
from LSGraph import LSGraph
import threading
import time
lock = threading.RLock()

def broadcast_route(routerA):
    while 1:
        routerA.broadcast()
        time.sleep(5)
    
def change_road(routerA):
    while 1:
        print('I change the route')
        routerA.change_route()
        time.sleep(20)

def send_message(routerA):
    while 1:
        msg = input('Please enter the msg to send')
        dst = input('Please enter the destination:(A/B/C/D/E),but not yourself:')
        routerA.send_meaningful_message(msg,dst)
    
def receive(routerA):
    while 1:
        lock.acquire()
        routerA.handle_receive()
        lock.release()

def down_and_recover(routerA):
    time.sleep(60)
    if routerA.down_status == True:
        lock.acquire()
        print("I am going down!")
        routerA.down()
        lock.release()
        time.sleep(60)
        lock.acquire()
        print("I now recover!")
        routerA.recover()
        lock.release()

def compute_LS(routerA):
    while 1:
        time.sleep(2)
        routerA.LS_algorithm()
        print("Recompute LS. cost:",routerA.cost)
        print('next jump:',routerA.next_jump)

if __name__ == "__main__":
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

    
    my_thread = []
    #Thread 1: 周期性广播路径的信息
    Bthread = threading.Thread(target=broadcast_route,args=(my_router,))
    my_thread.append(Bthread)
    #Thread 2: 处理接受到的消息
    Rthread = threading.Thread(target=receive,args=(my_router,))
    my_thread.append(Rthread)
    #Thread 3: 主动发送消息
    Sthread = threading.Thread(target=send_message,args=(my_router,))
    my_thread.append(Sthread)
    #Thread 4：周期性更改链路的代价
    Cthread = threading.Thread(target=change_road,args=(my_router,))
    my_thread.append(Cthread)
    #Thread 5：节点down掉和recover
    Dthread = threading.Thread(target=down_and_recover,args=(my_router,))
    my_thread.append(Dthread)
    #Thread 6：运行LS路由算法
    LThread = threading.Thread(target=compute_LS,args=(my_router,))
    my_thread.append(LThread)

    for thr in my_thread:
        thr.start()
    
    for thr in my_thread:
        thr.join()
    