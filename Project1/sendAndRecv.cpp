#include"sendAndRecv.h"
bool input(char& ans,int other)
{
	cout << "您想给Client" << other << "发送信息吗(是则输入Y,否则N,退出Q):\n";
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
	printf("请输入发送文件的路径:\n");
	cin >> path;
	getchar();
	ifstream infile(path, ios::in | ios::binary);	// 以二进制方式打开
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
	//获取文件大小
	infile.seekg(0, ios::end);	// 将指针定位到文件结尾处
	long size = infile.tellg();
	infile.seekg(0, ios::beg);	// 将指针回到文件开始处
	char Size[10000];
	itoa(size, Size, 10);
	strcpy(sendBuf, form);
	strcat(sendBuf, Size);
	cc = send(sock, sendBuf, strlen(sendBuf), 0);	//	发送大小和格式

	while (1)
	{
		memset(sendBuf, 0, sizeof(sendBuf));
		infile.read(sendBuf, BUFLEN);	// 将缓冲区大小的文件读进sendBuf
		int bytes = infile.gcount();	// 实际读进sendBuf的字节
		int pos = infile.tellg();		// 获取指针位置
		cc = send(sock, sendBuf, bytes, 0);	//	给服务器发送文件
		if (cc == SOCKET_ERROR)
		{
			printf("发送错误: %d\n", WSAGetLastError());
			return false;
		}
		else
		{
			count += cc;
		}
		if (pos == -1)					// 指针已到达文件尾部
		{
			break;			// 发送整个文件完成
		}
		Sleep(5);
	}
	printf("-------------------------------\n");
	string s = "已发送";
	char num[100];
	itoa(count, num, 10);
	s += num;
	s += "个字节数据\n";
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
		printf("发送错误: %d\n", WSAGetLastError());
		return false;
	}
	return true;

}
bool recvFile(SOCKET sock,int other)
{
	char recvBuf[BUFLEN + 1];
	int cc;	// 每次接收的字节数

	memset(recvBuf, 0, sizeof(recvBuf));
	cc = recv(sock, recvBuf, BUFLEN, 0);                // 接收服务器转发Client2的消息；第二个参数指向缓冲区，第三个参数为缓冲区大小(字节数)，第四个参数一般设置为0，返回值:(>0)接收到的字节数,(=0)对方已关闭,(<0)连接出错
	if (cc == SOCKET_ERROR)                          // 出错。其后必须关闭套接字sock
	{
		printf("接收错误: %d\n", GetLastError());
		return false;
	}
	else
	{
		if (!strcmp(recvBuf, "BYE"))
		{
			printf("对方已退出,请退出!\n");
			return false;
		}
		if (strcmp(recvBuf, "NOTHING"))
		{
			long count = 0;	// 总共收到的字节数
			string info = recvBuf;
			int pos = info.find('-');
			string form, size;
			long Size;
			form = info.substr(0, pos);
			size = info.substr(pos + 1, info.size() - pos - 1);
			Size = atol(size.c_str());
			printf("--------------------------------------\n");
			printf("Client%d发来%s文件(%ld字节)\n", other, form.c_str(),Size);
			printf("--------------------------------------\n");
			printf("请输入接收文件的路径:\n");
			string path;	// 路径
			cin >> path;
			getchar();
			ofstream outfile;
			outfile.open(path, ios::out | ios::binary);//打开要输出的文件
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
				if (cc == SOCKET_ERROR)                          // 出错
				{
					printf("接收错误: %d\n", GetLastError());
					return false;
				}
				//cout << "接收" << cc << endl;
				count += cc;
				//cout << count <<" "<< Size << endl;
				//写入文件
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
			cout << "成功接收" << count << "个字节数据\n";
			printf("-------------------------------\n\n");
		}
	}
	return true;
}