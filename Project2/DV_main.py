from node import Node
from TopoGraph import TopoGraph
import tkinter as tk
import tkinter.messagebox
import threading
import time

my_ip="192.168.199.205"
my_name='D'
Graph = TopoGraph()
Graph.initialize_graph()
neighbour=Graph.get_allNeighbour(my_name)
down=Graph.get_down(my_name)
changeable=Graph.node_changeable_route(my_ip)
print("changeable route:",changeable)
my_node = Node(my_name,my_ip,neighbour,changeable,down)
#my_node.neighbour={'192.168.199.102':34,'192.168.199.205':34}
my_node.neighbour={'192.168.199.131':30}
my_node.DV['127.0.0.1']=1000000
my_thread=[]
lock=threading.RLock()

#send按钮按下时
def hit_sbut(node):
    global s_feedback
    print('my_neighbour',node.neighbour)
    message=message_entry.get() #获取文本框里的消息内容
    dest=dest_entry.get()   #获取目的地

    if not message or not dest:
        tkinter.messagebox.showerror(title='Error',message="Empty message, try again!\n")
        return
    feedback=node.send_message(message,dest) #发送消息
    message_entry.delete(0,tk.END)  #清空框框
    dest_entry.delete(0,tk.END)
    if "Error" in feedback:
        tkinter.messagebox.showerror(title='Error',message=feedback)
    else:
        tkinter.messagebox.showinfo(title='Status',message=feedback)

    s_feedback.insert(tk.END,feedback)
    #sendMessage(my_node,message,dest)

#change link cost按钮按下
def change(node):
    node.change_route()
    linkInfo.insert(tk.END,"* Link cost has changed!\n"+"* neighbour: "+str(node.neighbour)+"\n\n")

#down按钮按下
def go_down(node):
    #lock.acquire()
    if node.down==True:
        node.go_down()
        linkInfo.insert(tk.END,"* Down!\n\n")
    #lock.release()
#recover按钮按下
def recover(node):
    if node.down==True:
        node.recover()
        linkInfo.insert(tk.END,"* Recover!\n"+"* neighbour: "+str(node.neighbour)+"\n\n")
    
window2=tk.Tk()#后台
window2.title('Router')
window2.geometry('800x600')

#三个显示窗口
#1.DV信息（收到的，周期发出自己的）
fm3=tk.Frame(window2)
dest_hint=tk.Label(fm3,text="DV info        ")
dest_hint.pack(side=tk.LEFT)
DVinfo=tk.Text(fm3,width=80,height=10)
DVinfo.pack(side=tk.LEFT)
fm3.pack(pady=10)
#2.转发消息（帮谁转发了消息）
fm4=tk.Frame(window2)
for_hint=tk.Label(fm4,text="Forwarding info")
for_hint.pack(side=tk.LEFT)
forwardInfo=tk.Text(fm4,width=80,height=5)
forwardInfo.pack(side=tk.LEFT)
fm4.pack(pady=10)
#3.链路cost、down和recover
fm5=tk.Frame(window2)
link_hint=tk.Label(fm5,text="Link and status info")
link_hint.pack(side=tk.LEFT)
linkInfo=tk.Text(fm5,width=80,height=8)
linkInfo.pack()
fm5.pack(pady=10)

window=tk.Toplevel(height=600,width=300)  #前台
window.title('Host - Message')
#window.geometry('600x350')

s_feedback=tk.Text(window,height=20) #最大的显示窗口
s_feedback.pack(fill=tk.X)   
fm1=tk.Frame(window)
message_hint=tk.Label(fm1,text="Enter message here:")
message_hint.pack(side=tk.LEFT)
message_entry=tk.Entry(fm1)  #要发的消息输入框
message_entry.pack(side=tk.LEFT)
fm1.pack(fill=tk.BOTH)

fm2=tk.Frame(window)
dest_hint=tk.Label(fm2,text="Destination(A/B/C/D/E):")
dest_hint.pack(side=tk.LEFT)
dest_entry=tk.Entry(fm2,show=None)   #目的地名字输入框
dest_entry.pack(side=tk.LEFT)
sbut=tk.Button(fm2,text='Send',width=10,height=1,command=lambda:hit_sbut(my_node))   #发送按钮
sbut.pack(side=tk.LEFT)

fm2.pack(ipadx=15,fill=tk.BOTH)
#sendDV线程调用
def sendDV_period(node):
    global DVinfo
    while 1:
        time.sleep(1)
        node.send_DV()
        show="* Send DV message to all neighbours!\n"
        my_dv=str(node.DV)
        my_table=str(node.table)
        DVinfo.insert(tk.END,show+'my_dv'+my_dv+'\n'+'my_table'+my_table+'\n\n')
        time.sleep(12)
#接收线程调用
def recv(node):
    print("thread")
    while 1:
        lock.acquire()
        feedback=node.recv() 
        print('here')
        lock.release()
        #收到消息
        if feedback[0]==0:
            s_feedback.insert(tk.END,feedback[1])
        #帮忙转发
        elif feedback[0]==1:
            forwardInfo.insert(tk.END,feedback[1])
        #邻居DV
        elif feedback[0]==2:
            DVinfo.insert(tk.END,feedback[1])
        #link cost 
        elif feedback[0]==3:
            linkInfo.insert(tk.END,feedback[1])
#线程共用的：my_node的sck_output

    #1.周期性发送DV消息
    #send_DV:sendto
DVthread=threading.Thread(target=sendDV_period,args=(my_node,))
my_thread.append(DVthread)
#DVthread.start()

    #2.接收
    #recv:sendto、recompute
Rthread=threading.Thread(target=recv,args=(my_node,))
my_thread.append(Rthread)

def thread_start():
    global my_thread
    for thread in my_thread:
        time.sleep(2)
        thread.setDaemon(True)
        thread.start()


#三个按钮
#1.更改链路cost
#2.down
#3.recover
fm6=tk.Frame(window2)
tbut=tk.Button(fm6,text='On',width=15,height=2,command=thread_start)   #thread开始按钮
tbut.pack()
changebut=tk.Button(fm6,text='Change link cost',width=15,height=2,command=lambda:change(my_node))
changebut.pack()
downbut=tk.Button(fm6,text='Down',width=15,height=2,command=lambda:go_down(my_node))
downbut.pack()
rebut=tk.Button(fm6,text='Recover',width=15,height=2,command=lambda:recover(my_node))
rebut.pack()
fm6.pack(pady=15)

window2.mainloop()
