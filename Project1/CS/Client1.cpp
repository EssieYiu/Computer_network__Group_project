#include"sendAndRecv.h"

#define WSVERS MAKEWORD(2,2)
#pragma comment(lib,"ws2_32.lib")
char HOST[16] = "127.0.0.1";//172.26.7.102

void main(int argc, char* argv[])
{
	char* host = HOST;	//������ip��ַ
	char* port = (char*)"50500";	//�������˿ں�
	struct sockaddr_in sAddr;	//�������׽��ֵ�ַ
	int cc;	//�ַ�����

	SOCKET sock;	//�ͻ����׽���

	WSADATA wsadata;
	WSAStartup(WSVERS, &wsadata);

	sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);//���������������ֽ�����TCP����Э��ţ�TCP��
													 //���÷������׽��ֵ�ַ
	memset(&sAddr, 0, sizeof(sAddr));
	sAddr.sin_family = AF_INET;
	sAddr.sin_port = htons((u_short)atoi(port));
	sAddr.sin_addr.s_addr = inet_addr(host);
	int con_status = connect(sock, (SOCKADDR*)&sAddr, sizeof(sAddr));	//	�����������
	if (con_status == SOCKET_ERROR)
	{
		printf("����ʧ��: %d\n", WSAGetLastError());
		printf("������������������\n������˳�...\n");
		getchar();
		return;
	}
	else
	{
		printf("���ӳɹ�!\n");
	}
	while (1)
	{
		char ans;
		while (1)
		{
			if (input(ans, 2))
				break;
			printf("����Ƿ�, ����������!\n\n");
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
		if (!recvFile(sock, 2))
			break;
	}

	closesocket(sock);
	WSACleanup();       	          //	ж��ĳ�汾��DLL
	printf("\n������˳�...\n");
	//getchar();
	getchar();
}