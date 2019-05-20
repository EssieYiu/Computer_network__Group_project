from My_node import *
from TopoGraph import TopoGraph
import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox
import threading
import time


my_ip="192.168.199.102"
my_name='E'
Graph = TopoGraph()
Graph.initialize_graph()
neighbour=Graph.get_allNeighbour(my_name)
changeable=Graph.node_changeable_route(my_ip)
print("changeable route:",changeable)
my_node = Node(my_name,my_ip,neighbour,changeable)
my_node.neighbour={'192.168.199.131':34,'192.168.39.128':34}
#my_node.DV['127.0.0.1']=1000000
my_thread=[]
lock=threading.RLock()
#sendDV线程调用
def sendDV_period(node):
    global DVinfo
    while 1:
        time.sleep(1)
        node.send_DV()
        print(node.neighbour)
        form_DV_list(node)
        time.sleep(12)
#接收线程调用
def recv(node):
    print("thread")
    while 1:
        lock.acquire()
        feedback=node.recv() 
        #print('here')
        lock.release()
        #收到消息
        if feedback[0]==0:
            s_feedback.insert(tk.END,feedback[1])   #插入到消息显示框
        #帮忙转发
        elif feedback[0]==1:
            forwardInfo.insert(tk.END,feedback[1])  #插入到转发框
        #邻居DV
        elif feedback[0]==2:
            form_DV_list(node)  #显示转发表
        #link cost 
        elif feedback[0]==3:
            msg_var.set(feedback[1])#插入到链路状态框
            form_DV_list(node)

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

#send按钮按下时
def hit_sbut(node):
    global s_feedback
    print('my_neighbour',node.neighbour)
    message=message_entry.get() #获取文本框里的消息内容
    dest=dest_entry.get()   #获取目的地
    if not message or not dest: #文本框为空
        tkinter.messagebox.showerror(title='Error',message="Empty message,please try again!\n")
        return
    feedback=node.send_message(message,dest) #发送消息
    message_entry.delete(0,tk.END)  #清空框框
    dest_entry.delete(0,tk.END)
    if "Error" in feedback:
        tkinter.messagebox.showerror(title='Error',message=feedback)
    else:
        s_feedback.insert(tk.END,feedback)

DOWN=False
#change link cost按钮按下
def change(node):
    global DOWN
    if DOWN==False:
        node.change_route()
        msg_var.set('Local link cost has changed!')
        form_DV_list(node)
    else:
        tkinter.messagebox.showerror(title='Error',message="You are not able to change when you are in down status!")
    #linkInfo.insert(tk.END,"* Link cost has changed!\n"+"* neighbour: "+str(node.neighbour)+"\n\n")

#down按钮按下
def go_down(node):
    #if node.down==True:
    global DOWN
    if DOWN==False:
        node.go_down()
        DOWN=True
        msg_var.set('Down!')
        form_DV_list(node)
    else:
        tkinter.messagebox.showerror(title='Error',message="You have already been down!")
    
#recover按钮按下
def recover(node):
    global DOWN
    if DOWN==True:
        node.recover()
        DOWN=False
        msg_var.set('Recover!')
        form_DV_list(node)
    else:
        tkinter.messagebox.showerror(title='Error',message="You have already recovered!")

#形成DV表
def form_DV_list(node):
    global DVinfo
    DVinfo.delete(0,tk.END)
    head="Dest   Cost       Next jump"
    DVinfo.insert(tk.END,head)
    for n in ALL:
        if n!=node.name:
            index=ALL.index(n)
            ip=IP[index]
            next=node.table[ip]
            if next in IP:
                next_name=ALL[IP.index(next)]
            else:
                next_name='None'
            if node.DV[ip]==INFINITE:
                DV='  '+n+'      '+str(node.DV[ip])+'      '+next_name
            else:
                DV='  '+n+'      '+str(node.DV[ip])+'               '+next_name
            DVinfo.insert(tk.END,DV)
#---------------------------------------后台---------------------------------------
window2=tk.Tk()
window2.title('Router')
window2.geometry('600x480')
my_font= tkf.Font(family='Arial',size=10,weight =tkf.BOLD)
#三个显示窗口
#1.DV信息（收到的，周期发出自己的）
DV_hint=tk.Label(window2,font=my_font,text="DV info         ")
DV_hint.grid(row=1,column=0,sticky=tk.E)
DVinfo=tk.Listbox(window2,font=my_font,width=30)
DVinfo.grid(row=1,column=1,pady=8)

#2.转发消息（帮谁转发了消息）
for_hint=tk.Label(window2,text="Forwarding info",font=my_font)
for_hint.grid(row=2,column=0)
forwardInfo=tk.Text(window2,width=50,height=5)
forwardInfo.grid(row=2,column=1,pady=8)

#3.链路cost、down和recover
link_hint=tk.Label(window2,text="      Link and status info",font=my_font)
link_hint.grid(row=0,column=0,sticky=tk.E+tk.W) 
msg_var = tk.StringVar()
link_status=tk.Label(window2,text="Here is the status msg",textvariable = msg_var,font=my_font) #一行，显示链路状态
link_status.grid(row=0,column=1,pady=8)

#三个按钮
#1.更改链路cost
#2.down
#3.recover
changebut=tk.Button(window2,text='Change link cost',width=15,height=2,font=my_font,command=lambda:change(my_node))
changebut.grid(row=4,column=1,pady=2)
downbut=tk.Button(window2,text='Down',width=15,height=2,font=my_font,command=lambda:go_down(my_node))
downbut.grid(row=5,column=1,pady=2)
rebut=tk.Button(window2,text='Recover',width=15,height=2,font=my_font,command=lambda:recover(my_node))
rebut.grid(row=6,column=1,pady=2)

#显示name和ip
ip_hint=tk.Label(window2,font=my_font,text="My ip: "+my_node.ip)
ip_hint.grid(row=4,column=0,sticky=tk.W)
name_hint=tk.Label(window2,font=my_font,text='My name: '+my_node.name)
name_hint.grid(row=5,column=0,sticky=tk.W)

#---------------------------------------前台---------------------------------------
window=tk.Toplevel(height=600,width=300)  #前台
window.title('Host - Message')

s_feedback=tk.Text(window,height=20) #最大的显示窗口
s_feedback.pack(fill=tk.X)   
fm1=tk.Frame(window)
message_hint=tk.Label(fm1,text="Enter message here:",font=my_font)
message_hint.pack(side=tk.LEFT)
message_entry=tk.Entry(fm1)  #要发的消息输入框
message_entry.pack(side=tk.LEFT)
fm1.pack(fill=tk.BOTH)

fm2=tk.Frame(window)
dest_hint=tk.Label(fm2,text="Destination(A/B/C/D/E):",font=my_font)
dest_hint.pack(side=tk.LEFT)
dest_entry=tk.Entry(fm2,show=None)   #目的地名字输入框
dest_entry.pack(side=tk.LEFT)
sbut=tk.Button(fm2,text='Send',width=10,height=1,font=my_font,command=lambda:hit_sbut(my_node))   #发送按钮
sbut.pack(side=tk.LEFT)
fm2.pack(ipadx=15,fill=tk.BOTH)


for thread in my_thread:
    time.sleep(2)
    thread.setDaemon(True)
    thread.start()

window2.mainloop()
