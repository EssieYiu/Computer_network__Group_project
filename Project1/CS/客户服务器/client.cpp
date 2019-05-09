#include"sendAndRecv.h"
#define WSVERS MAKEWORD(2,2)
#pragma comment(lib,"ws2_32.lib")
char HOST[16] = "127.0.0.1";//172.26.7.102

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
		printf("Connect failed: %d\n", WSAGetLastError());
		printf("Please try again!\n");
		printf("Press any to quit...\n");
		getchar();
		return;
	}
	else
	{
		printf("Connect successfully!\n");
	}
	int ans;
	while (1)
	{
		if (!input(ans))
			continue;
		switch (ans)
		{
		case 1:
		case 2:
			sendRequest(sock, ans);
			recvResponse(sock);
			break;
		case 3://help
			printf("HELP MENU:\n");
			printf("1. Resource list is a list of names of the files you can download from the server \n");
			printf("2. A file name should be like this: test.mp4 \n");
			printf("3. A path should be like this: C:\\\\Users\\\\Pictures\\\\test.jpg\n");
			break;
		case 4:
			sendRequest(sock, 4);
			printf("Quit successfully!\n");
			getchar();
			return;
		default:
			break;
		}
	}
	closesocket(sock);
	WSACleanup();
	printf("\nPress any to quit...\n");
	getchar();
	return;
}
