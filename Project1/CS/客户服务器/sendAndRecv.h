#ifndef SENDANDRECV_H
#define SENDANDRECV_H
#include<WinSock2.h>
#include<string.h>
#include<stdlib.h>
#include<string>
#include<fstream>
#include<iostream>
#include"MessageType.h"
#define BUFLEN 20000
using namespace std;

#pragma comment(lib,"ws2_32.lib")
//获取用户的功能选择
bool input(int& ans);
//发送用户的请求
bool sendRequest(SOCKET sock, int choice);
//接收服务器发来的文件
bool recvResponse(SOCKET sock)
#endif // !SENDANDRECV_H

