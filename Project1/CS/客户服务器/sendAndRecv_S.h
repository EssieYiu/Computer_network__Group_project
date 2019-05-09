#ifndef SENDANDRECV_S_H
#define SENDANDRECV_S_H
#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<WinSock2.h>
#include<string.h>
#include <fstream>
#include<string>
#include<io.h>
#include"MessageType.h"
#define BUFLEN 20000
using namespace std;
//监听客户请求并返回请求的数据
bool recvAndSend(SOCKET sock);
//发送服务器资源文件列表
bool sendList(SOCKET sock);
//发送文件
bool sendFile(SOCKET sock,char* name);
#endif // !SENDANDRECV_S_H
