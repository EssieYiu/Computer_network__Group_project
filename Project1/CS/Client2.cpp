#include"\Users\galaxy\Documents\大二下\计算机网络\CS\Client1\Client1\sendAndRecv.h"
#pragma warning(disable:4996)
#define WSVERS MAKEWORD(2,2)
#pragma comment(lib,"ws2_32.lib")

char HOST[16] = "127.0.0.1";

void main(int argc, char* argv[])
{
	char* host = HOST;	//服务器ip地址
	char* port = (char*)"50500";	//服务器端口号
	struct sockaddr_in sAddr;	//服务器套接字地址
	int cc;	//字符数量

	SOCKET sock;	//客户端套接字

	WSADATA wsadata;
	WSAStartup(WSVERS, &wsadata);

	sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);//参数：因特网、字节流（TCP）、协议号（TCP）
													 //设置服务器套接字地址
	memset(&sAddr, 0, sizeof(sAddr));
	sAddr.sin_family = AF_INET;
	sAddr.sin_port = htons((u_short)atoi(port));
	sAddr.sin_addr.s_addr = inet_addr(host);
	int con_status = connect(sock, (SOCKADDR*)&sAddr, sizeof(sAddr));	//	与服务器连接
	if (con_status == SOCKET_ERROR)
	{
		printf("连接失败: %d\n", WSAGetLastError());
		printf("请重启服务器后重试\n任意键退出...\n");
		getchar();
		return;
	}
	else
		printf("连接成功!\n");

	while (1)
	{
		if (!recvFile(sock, 1))
			break;
		char ans;
		while (1)
		{
			if (input(ans, 1))
				break;
			printf("输入非法, 请重新输入!\n\n");
		}
		if (ans == 'Y')
		{
			sendFile(sock);
			Sleep(100);
			sendMessage(sock, END);
		}
		else if (ans == 'Q')
		{
			sendMessage(sock, BYE);
			break;
		}
		else
		{
			
			sendMessage(sock, NOTHING);
		}
	}

	closesocket(sock);
	WSACleanup();       	          //	卸载某版本的DLL
	printf("\n任意键退出...\n");
	getchar();
}