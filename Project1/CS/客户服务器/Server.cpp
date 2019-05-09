#include"sendAndRecv_S.h"
#define WSVERS MAKEWORD(2,2)
#pragma comment(lib,"ws2_32.lib")

void main(int argc, char* argv[])
{
	char *port = (char*)"50500";//�������˿ں�

	int cc = 0;	//�ַ�����
	SOCKET msock, ssock;//�������׽���
	struct sockaddr_in sAddr;
	struct sockaddr_in cAddr;//�������׽��ֵ�ַ

	WSADATA wsadata;
	WSAStartup(WSVERS, &wsadata);

	msock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

	//���÷������׽��ֵ�ַ
	memset(&sAddr, 0, sizeof(sAddr));
	sAddr.sin_family = AF_INET;
	sAddr.sin_port = htons((u_short)atoi(port));
	sAddr.sin_addr.s_addr = INADDR_ANY;
	bind(msock, (struct sockaddr*)&sAddr, sizeof(sAddr));

	listen(msock, 10);	//����
	printf("Server is ready!\n");
	int sLen = sizeof(struct sockaddr);
	ssock = accept(msock, (struct sockaddr*)&cAddr, &sLen);//����addr��addrlen��ſͻ����ĵ�ַ��Ϣ  client1
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