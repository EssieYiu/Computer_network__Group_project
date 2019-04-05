#include"sendAndRecv.h"
bool input(char& ans,int other)
{
	cout << "�����Client" << other << "������Ϣ��(��������Y,����N,�˳�Q):\n";
	scanf("%c", &ans);
	getchar();
	if (ans == 'Y' || ans == 'N' || ans == 'n' || ans == 'y'||ans=='q'||ans=='Q')
	{
		ans = toupper(ans);
		return true;
	}
	return false;
}
bool sendFile(SOCKET sock)
{
	char sendBuf[BUFLEN + 1];
	string path;
	int cc;
	long count = 0;
	printf("�����뷢���ļ���·��:\n");
	cin >> path;
	getchar();
	ifstream infile(path, ios::in | ios::binary);	// �Զ����Ʒ�ʽ��
	if (infile.is_open() != true)
	{
		cout << "can not open " << endl;
		system("pause");
		exit(1);
	}

	char form[10];
	int j = 0;
	for (int i = path.find('.')+1;i < path.size();i++)
	{
		form[j] = path[i];
		j++;
	}
	form[j] = '-';
	form[j + 1] = '\0';
	//��ȡ�ļ���С
	infile.seekg(0, ios::end);	// ��ָ�붨λ���ļ���β��
	long size = infile.tellg();
	infile.seekg(0, ios::beg);	// ��ָ��ص��ļ���ʼ��
	char Size[10000];
	itoa(size, Size, 10);
	strcpy(sendBuf, form);
	strcat(sendBuf, Size);
	cc = send(sock, sendBuf, strlen(sendBuf), 0);	//	���ʹ�С�͸�ʽ

	while (1)
	{
		memset(sendBuf, 0, sizeof(sendBuf));
		infile.read(sendBuf, BUFLEN);	// ����������С���ļ�����sendBuf
		int bytes = infile.gcount();	// ʵ�ʶ���sendBuf���ֽ�
		int pos = infile.tellg();		// ��ȡָ��λ��
		cc = send(sock, sendBuf, bytes, 0);	//	�������������ļ�
		if (cc == SOCKET_ERROR)
		{
			printf("���ʹ���: %d\n", WSAGetLastError());
			return false;
		}
		else
		{
			count += cc;
		}
		if (pos == -1)					// ָ���ѵ����ļ�β��
		{
			break;			// ���������ļ����
		}
		Sleep(5);
	}
	printf("-------------------------------\n");
	string s = "�ѷ���";
	char num[100];
	itoa(count, num, 10);
	s += num;
	s += "���ֽ�����\n";
	cout << s;
	printf("-------------------------------\n\n");
	return true;
}
bool sendMessage(SOCKET sock, MessageType type)
{
	char sendBuf[BUFLEN + 1];
	memset(sendBuf, 0, sizeof(sendBuf));
	switch (type)
	{
	case NOTHING:
		strcpy(sendBuf, "NOTHING");
		break;
	case END:
		strcpy(sendBuf, "EOF");
		break;
	case BYE:
		strcpy(sendBuf, "BYE");
		break;
	}
	int cc = send(sock, sendBuf, strlen(sendBuf) + 1, 0);
	if (cc == SOCKET_ERROR)
	{
		printf("���ʹ���: %d\n", WSAGetLastError());
		return false;
	}
	return true;

}
bool recvFile(SOCKET sock,int other)
{
	char recvBuf[BUFLEN + 1];
	int cc;	// ÿ�ν��յ��ֽ���

	memset(recvBuf, 0, sizeof(recvBuf));
	cc = recv(sock, recvBuf, BUFLEN, 0);                // ���շ�����ת��Client2����Ϣ���ڶ�������ָ�򻺳���������������Ϊ��������С(�ֽ���)�����ĸ�����һ������Ϊ0������ֵ:(>0)���յ����ֽ���,(=0)�Է��ѹر�,(<0)���ӳ���
	if (cc == SOCKET_ERROR)                          // ����������ر��׽���sock
	{
		printf("���մ���: %d\n", GetLastError());
		return false;
	}
	else
	{
		if (!strcmp(recvBuf, "BYE"))
		{
			printf("�Է����˳�,���˳�!\n");
			return false;
		}
		if (strcmp(recvBuf, "NOTHING"))
		{
			long count = 0;	// �ܹ��յ����ֽ���
			string info = recvBuf;
			int pos = info.find('-');
			string form, size;
			long Size;
			form = info.substr(0, pos);
			size = info.substr(pos + 1, info.size() - pos - 1);
			Size = atol(size.c_str());
			printf("--------------------------------------\n");
			printf("Client%d����%s�ļ�(%ld�ֽ�)\n", other, form.c_str(),Size);
			printf("--------------------------------------\n");
			printf("����������ļ���·��:\n");
			string path;	// ·��
			cin >> path;
			getchar();
			ofstream outfile;
			outfile.open(path, ios::out | ios::binary);//��Ҫ������ļ�
			if (outfile.is_open() != true)
			{
				cout << "can not open" << endl;
				system("pause");
				exit(1);
			}
			while (1)
			{
				memset(recvBuf, 0, sizeof(recvBuf));
				cc = recv(sock, recvBuf, BUFLEN, 0);
				if (cc == SOCKET_ERROR)                          // ����
				{
					printf("���մ���: %d\n", GetLastError());
					return false;
				}
				//cout << "����" << cc << endl;
				count += cc;
				//cout << count <<" "<< Size << endl;
				//д���ļ�
				if (count <= Size)
				{
					outfile.write(recvBuf, cc);
				}
				if (cc == 4 && recvBuf[0] == 'E'&&recvBuf[1] == 'O'&&recvBuf[2] == 'F')
				{
					count -= 4;
					break;
				}
				if (count>Size)
				{
					count -= 4;
					outfile.write(recvBuf, cc-4);
					break;
				}
				
			}
			printf("-------------------------------\n");
			cout << "�ɹ�����" << count << "���ֽ�����\n";
			printf("-------------------------------\n\n");
		}
	}
	return true;
}