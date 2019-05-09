#include"forwarding.h"

#define WSVERS MAKEWORD(2,2)
using namespace std;
//����2.2�汾Winsock ��λ�ֽڸ��汾�ţ���λ�ֽ����汾��

#pragma comment(lib,"ws2_32.lib")

void main(int argc, char* argv[])
{
	char *port = (char*)"50500";//�������˿ں�

	int cc = 0;	//�ַ�����
	SOCKET msock, ssock1,ssock2;//�������׽���
	struct sockaddr_in sAddr;
	struct sockaddr_in cAddr1,cAddr2;//�������׽��ֵ�ַ
	char* pts;	//ʱ���ַ���ָ��
	time_t now;	//ʱ��

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
	printf("������������!\n");
	int sLen = sizeof(struct sockaddr);
	ssock1 = accept(msock, (struct sockaddr*)&cAddr1, &sLen);//����addr��addrlen��ſͻ����ĵ�ַ��Ϣ  client1
	printf("��Client1�������ӳɹ�\n");
	ssock2 = accept(msock, (struct sockaddr*)&cAddr2, &sLen);//client2
	printf("��Client2�������ӳɹ�\n\n");
	while (1)
	{
		if (!forwarding(ssock1, cAddr1, ssock2, cAddr2))
		{
			printf("���˳�������\n");
			break;
		}
		//cout << 1 << endl;
		if (!forwarding(ssock2, cAddr2, ssock1, cAddr1))
		{
			printf("���˳�������\n");
			break;
		}
		//cout << 2 << endl;
	}


	closesocket(ssock1);
	closesocket(ssock2);
	closesocket(msock);
	WSACleanup();       	          /* ж��ĳ�汾��DLL */
	printf("\n������˳�...\n");
	getchar();

}