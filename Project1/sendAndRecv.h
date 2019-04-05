#ifndef SENDANDRECV_H
#define SENDANDRECV_H
#include<stdio.h>
#include<string.h>
#include<WinSock2.h>
#include<conio.h>
#include<iostream>
#include<string>
#include<fstream>
#include<Windows.h>
#define BUFLEN 200000
#pragma warning(disable:4996)
using namespace std;
enum MessageType
{
	NOTHING = 0,
	END = 1,
	BYE = 2
};
bool sendFile(SOCKET sock);
bool recvFile(SOCKET sock, int other);
bool sendMessage(SOCKET sock, MessageType type);
bool input(char& ans, int other);
#endif // !SENDANDRECV_H
