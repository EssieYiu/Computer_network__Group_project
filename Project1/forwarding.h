#ifndef FORWARDING_H
#define FORWARDING_H
#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<WinSock2.h>
#include<string.h>
#include <fstream>
#include<time.h>
#include<conio.h>
#include<string>
#include<Windows.h>
#define BUFLEN 200000
#pragma warning(disable:4996)
#pragma warning(disable:4716)
using namespace std;
bool forwarding(SOCKET from, sockaddr_in f, SOCKET to, sockaddr_in t);

#endif // !FORWARDING_H

