# 计算机网络Project1 report document
## introduction
本项目分别实现了C/S和p2p两种不同模式的通信。采用的是TCP通信协议。
C/S使用C语言，实现了客户端与服务器间的通信：服务器端程序监听客户端向服务端发出的请求，并返回数据给客户端。以及客户端之间的通信：实现客户端之间交换信息。

## design
### C/S
### P2P

## setup and deploy
### C/S
### P2P
主要由3个模块组成：server、peer_server、peer_client
1.server
是p2p体系中的服务器，负责管理所有peer的信息。加入此p2p系统中的每一个peer的信息（如ip地址、id号）以及这些peer各自所拥有的资源服务器都能知道。服务器负责管理这些信息，并且对各个peer的请求做出相对应的回应，返回一定的信息。
2.peer_client
是peer的客户端部分，是发起请求的主动方。给服务器发去请求。并且主动和其他peer建立连接。
3.peer_server
是peer的服务器部分，监听其他peer给它发来的请求，并且处理这些请求。作出相对应的回应。

主要实现的功能有两个
1.p2p文件下载
- peer A向服务器发出请求[request_server]，提出要下载文件F
- 服务器查询资源列表，返回具有文件F的peer信息给A
- 断开服务器和A的连接
- A同时和这些peer建立连接，向这些peer发出请求[request_peer]，下载这个文件的不同部分（使用多线程）
- 下载完毕，断开连接
- peer再次和服务器建立连接，发出请求[request_server]，更新自己的资源信息
- 断开连接
2.p2p任意两个peer之间的聊天
- 想要聊天的peer向服务器发出请求[request_server]，服务器返回在线的peer列表给它
- 这个peer选择一个在线好友，像它发出请求[request_peer]，建立tcp连接，可以开始通信
- 任意一方说了'Bye!'则通信结束
- 断开连接

部分自定义的通信协议如下：
- peer向服务器发起的请求，记作[request_server]，格式如下
    1.注册自己的信息 "1 register" 
    2.更新自己拥有的资源 "2 update"
    3.下载文件 "3 filename"
    4.和其他peer聊天（get peers online） "4 chat"
- peer向其他peer发起的请求，记作[request_peer]，格式如下
    1.下载文件 "1 filename m of n 
    2.聊天 "2 chat"

## result
### C/S
### P2P

## project management record
