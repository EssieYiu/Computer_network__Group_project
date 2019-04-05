# P2P 通信及其实现

## 主要功能
1.实现p2p文件下载
2.实现任意两个peer之间的通信
3.实现任意两个peer之间的文件传输

# 对象和类
1.server
是服务器，负责管理所有在这个网络里面的peer的信息
2.peer
节点，在p2p通信中既能做服务器，也能做客户端

# 主要过程
所有的peer在加入这个网络的初期，都必须向服务器注册登记自己的信息[request_server]，提供自己的Ip地址和端口号给服务器，以及将自己所拥有的文件资源告诉服务器
1.p2p文件下载
- peer A向服务器发出请求[request_server]，提出要下载文件F
- 服务器查询资源列表，返回具有文件F的peer信息给A
- 断开服务器和A的连接
- A同时和这些peer建立连接，向这些peer发出请求[request_peer]，下载这个文件的不同部分（使用多线程）
- 下载完毕，断开连接
- peer再次和服务器建立连接，发出请求[request_server]，更新自己的资源信息
- 断开连接

2.任意两个peer之间的通信
- 想要聊天的peer向服务器发出请求[request_server]，服务器返回在线的peer列表给它
- 这个peer选择一个在线好友，像它发出请求[request_peer]，建立tcp连接，可以开始通信
- 任意一方说了'Bye!'则通信结束
- 断开连接

3.peer之间文件传输

# 具体实现
1.server
- 成员变量 serverSocket：用于监听其他peer给它发来的请求，并对此做出回应
- handle_server()：服务器处在监听请求状态，一旦收到请求，先判断这个peer是否在列表中，不在则添加。之后便对此请求做出处理，并返回相应的信息
- 全局变量 CONNECTION_LIST存储在线的peer
- RESOURCES 存储peer们的资源

2.peer（客户端和服务器使用多线程）
初始的时候先register一下
- 作为客户端
    - 接受来自命令行的指令，
    - 根据指令的不同给服务器先发去请求，新建一个套接字
    - 断开和服务器连接
    - 处理返回值数据
    - 再和其他peer建立连接，向其他peer发去请求
    - 断开连接
- 作为服务器
    - 成员变量 peer_socket 用于监听其他peer给它发过来的连接
    - 处在监听的状态，listening_to_others()。一旦收到请求，建立和客户的数据连接套接字，判断这个请求是什么类型，然后执行相对应操作
    - 完成后断开连接

# 通信协议
peer用于监听其他peer的请求的端口为10086 服务器的端口为15000
- request_server 其他人给服务器发去的请求
    1.注册自己的信息 "1 register" 
    2.更新自己拥有的资源 "2 update"
    3.下载文件 "3 filename"
    4.和其他peer聊天（get peers online） "4 chat"
    5.和其他peer互传文件（get peers online）"5 send"
- request_peer peer给peer发去的请求
    1.下载文件 "1 filename m of n 
    2.聊天 "2 chat"
    3.互传文件 "3 filename"?
- peer分割文件的时候按照相同的规则划分，能够得到同样数量的part，再自己根据ID号，选择要传输的部分

# 几点注意事项
- 使用套接字传list的时候使用json，dumps & loads
- 使用套接字传字符串的时候要encode一下，解读的时候str一下
