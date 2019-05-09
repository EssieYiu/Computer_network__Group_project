#include"forwarding.h"

#define WSVERS MAKEWORD(2,2)
using namespace std;
//调用2.2版本Winsock 高位字节副版本号，低位字节主版本号

#pragma comment(lib,"ws2_32.lib")

void main(int argc, char* argv[])
{
	char *port = (char*)"50500";//服务器端口号

	int cc = 0;	//字符数量
	SOCKET msock, ssock1,ssock2;//服务器套接字
	struct sockaddr_in sAddr;
	struct sockaddr_in cAddr1,cAddr2;//服务器套接字地址
	char* pts;	//时间字符串指针
	time_t now;	//时间

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
	printf("服务器已启动!\n");
	int sLen = sizeof(struct sockaddr);
	ssock1 = accept(msock, (struct sockaddr*)&cAddr1, &sLen);//参数addr和addrlen存放客户方的地址信息  client1
	printf("与Client1建立连接成功\n");
	ssock2 = accept(msock, (struct sockaddr*)&cAddr2, &sLen);//client2
	printf("与Client2建立连接成功\n\n");
	while (1)
	{
		if (!forwarding(ssock1, cAddr1, ssock2, cAddr2))
		{
			printf("请退出服务器\n");
			break;
		}
		//cout << 1 << endl;
		if (!forwarding(ssock2, cAddr2, ssock1, cAddr1))
		{
			printf("请退出服务器\n");
			break;
		}
		//cout << 2 << endl;
	}


	closesocket(ssock1);
	closesocket(ssock2);
	closesocket(msock);
	WSACleanup();       	          /* 卸载某版本的DLL */
	printf("\n任意键退出...\n");
	getchar();

}