#include"sendAndRecv_S.h"
#define WSVERS MAKEWORD(2,2)
#pragma comment(lib,"ws2_32.lib")

void main(int argc, char* argv[])
{
	char *port = (char*)"50500";//服务器端口号

	int cc = 0;	//字符数量
	SOCKET msock, ssock;//服务器套接字
	struct sockaddr_in sAddr;
	struct sockaddr_in cAddr;//服务器套接字地址

	WSADATA wsadata;
	WSAStartup(WSVERS, &wsadata);

	msock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

	//设置服务器套接字地址
	memset(&sAddr, 0, sizeof(sAddr));
	sAddr.sin_family = AF_INET;
	sAddr.sin_port = htons((u_short)atoi(port));
	sAddr.sin_addr.s_addr = INADDR_ANY;
	bind(msock, (struct sockaddr*)&sAddr, sizeof(sAddr));

	listen(msock, 10);	//监听
	printf("Server is ready!\n");
	int sLen = sizeof(struct sockaddr);
	ssock = accept(msock, (struct sockaddr*)&cAddr, &sLen);//参数addr和addrlen存放客户方的地址信息  client1
	printf("Connect with Client%s successfully!\n", inet_ntoa(cAddr.sin_addr));

	while (1)
	{
		if (!recvAndSend(ssock))
		{
			printf("End!\n");
			break;
		}
	}
	closesocket(ssock);
	closesocket(msock);
	WSACleanup();
	printf("\nPress any to quit...\n");
	getchar();
	return;
}