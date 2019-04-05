#include"forwarding.h"
bool forwarding(SOCKET from, sockaddr_in f, SOCKET to, sockaddr_in t)
{
	char recvBuf[BUFLEN + 1];
	memset(recvBuf, 0, sizeof(recvBuf));
	int rc, sc;
	long long rcount = 0;
	long long scount = 0;
	rc = recv(from, recvBuf, BUFLEN, 0);              // ����������Ҫת����Client2����Ϣ���ڶ�������ָ�򻺳���������������Ϊ��������С(�ֽ���)�����ĸ�����һ������Ϊ0������ֵ:(>0)���յ����ֽ���,(=0)�Է��ѹر�,(<0)���ӳ���
	if (rc == SOCKET_ERROR)                          // ����������ر��׽���sock
	{
		printf("���մ���: %d\n", GetLastError());
		return false;
	}
	else
	{
		rcount += rc;
		sc = send(to, recvBuf, rc, 0);
		if (sc == SOCKET_ERROR)                          // ����
		{
			printf("ת������: %d\n", GetLastError());
			return false;
		}
		scount += sc;
		if (!strcmp(recvBuf, "BYE"))				//Client����BYE
		{
			printf("Client%s ���˳�!\n", inet_ntoa(f.sin_addr));
			return false;
		}
		if (strcmp(recvBuf, "NOTHING"))				//����NOTHING,�����ļ�����һ���յ����Ǹ�ʽ+��С��Ϣ,Ҫ������С��ֻ���ļ���С��
		{
			rcount -= rc;
			scount -= sc;
			string info = recvBuf;
			int pos = info.find('-');
			string form, size;
			long Size;
			form = info.substr(0, pos);
			size = info.substr(pos + 1, info.size() - pos - 1);
			Size = atol(size.c_str());				//�ļ���С
			while (1)
			{
				memset(recvBuf, 0, sizeof(recvBuf));
				rc = recv(from, recvBuf, BUFLEN, 0);	//����
				if (rc == SOCKET_ERROR)                 // ����
				{
					printf("���մ���: %d\n", GetLastError());
					return false;
				}
				//cout << "�յ�" << rc << endl;
				rcount += rc;
				sc = send(to, recvBuf, rc, 0);		//ת��
				if (sc == SOCKET_ERROR)            // ����
				{
					printf("ת������: %d\n", GetLastError());
					return false;
				}
				scount += sc;
				//cout << "ת��" << sc << endl;
				/*if (rcount <= Size)
				{
					continue;
				}*/
				if ((rc == 4 && recvBuf[0] == 'E'&&recvBuf[1] == 'O'&&recvBuf[2] == 'F')||rcount>Size)
				{
					rcount -= 4;
					scount -= 4;
					break;
				}
			}	
		}
		printf("-------------------------------------\n");
		printf("�յ�����%s: %d�ֽ�����\n", inet_ntoa(f.sin_addr), rcount);
		printf("�ɹ�ת����%s: %d�ֽ�����\n", inet_ntoa(t.sin_addr), scount);
		printf("--------------------------------------\n\n");
	}
}
	/*char recvBuf[BUFLEN + 1];
	int rc, sc;
	long long rcount = 0;
	long long scount = 0;
	while (1)
	{
		memset(recvBuf, 0, sizeof(recvBuf));
		rc = recv(from, recvBuf, BUFLEN, 0);//������
		if (rc == SOCKET_ERROR)
		{
			printf("����ʧ��%d\n", GetLastError());
			break;
		}
		cout << "����" << rc << endl;
		
		sc = send(to, recvBuf, rc, 0);
		cout << "ת��" << endl;
		if (sc == SOCKET_ERROR)
		{
			printf("ת��ʧ��%d\n", GetLastError());
			break;
		}
		Sleep(5);
		if (rc==4&&recvBuf[0]=='E'&&recvBuf[1]=='O'&&recvBuf[2]=='F')//���յ�EOF
		{

			printf("�ļ�����\n");
			break;
		}
		rcount += rc;
		scount += sc;
		if (!strcmp(recvBuf, "NOTHING"))//���յ�NOTHING
			break;
	}*/
	
