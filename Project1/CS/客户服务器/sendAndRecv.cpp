#include"sendAndRecv.h"
//获取用户的功能选择
bool input(int& ans)
{
	printf("\n--------------------------------------------------------\n");
	printf("1.Get a resource list\n");
	printf("2.Download a file with its name\n");
	printf("3.Display help menu\n");
	printf("4.Quit\n");
	while (1)
	{
		printf("Please enter your choice: ");
		string Ans;
		cin >> Ans;
		ans = atoi(Ans.c_str());
		if (ans == 1 || ans == 2 || ans == 3 || ans == 4)
			return true;
		else
		{
			printf("Invalid!\n");
		}
	}
	return false;
}
//发送用户的请求
bool sendRequest(SOCKET sock, int choice)
{
	char sendBuf[300];
	char name[270];
	string Name = " ";
	switch (choice)
	{
	case 1:
		strcpy(sendBuf, "0");
		break;
	case 2:
		do
		{
			printf("Please enter the name of the file to download: ");
			scanf("%s", name);
			Name = name;
		} while (Name.find('.') == -1);
		strcpy(sendBuf, "1");
		strcat(sendBuf, name);
		//printf("%s\n", sendBuf);
		break;
	case 4:
		strcpy(sendBuf, "2");
		break;
	default:
		return false;
	}
	int b = send(sock, sendBuf, strlen(sendBuf) + 1, 0);
	if (b == SOCKET_ERROR)
	{
		printf("Send request failed: %d", GetLastError());
		return false;
	}
	return true;
}
//接收服务器发来的文件或者列表
bool recvResponse(SOCKET sock)
{
	char recvBuf[BUFLEN + 1];
	int cc = recv(sock, recvBuf, BUFLEN, 0);
	long count = 0;	//总共接收的数据字节数
	//cout << "cc: " << cc << endl;
	//cout << "recvBuf[0]: "<<recvBuf[0] << endl;
	if (cc == SOCKET_ERROR)
	{
		printf("Receive failed: %d", GetLastError());
		return false;
	}
	if (recvBuf[0] == MTYPE_LIST + '0')	//收到服务器发来的文件列表
	{
		printf("RESOURCE LIST:\n");
		printf("%s", recvBuf+1);
		return true;
	}
	if (recvBuf[0] == MTYPE_FILE + '0')	//收到服务器发来的文件
	{
		long size = atol(recvBuf + 1);
		if (size == 0)
		{
			printf("* File you ask for doesn't exist! Please try again!\n");
			return true;
		}
		char path[BUFLEN + 1];
		printf("Please enter the path you want to save this file: ");
		scanf("%s", &path);
		ofstream outfile;
		outfile.open(path, ios::out | ios::binary);//打开要输出的文件
		if (outfile.is_open() != true)
		{
			cout << "Can not open" << endl;
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
			//cout << count <<" "<<size << endl;
			//写入文件
			if (count <= size)
			{
				outfile.write(recvBuf, cc);
			}
			if (cc == 4 && recvBuf[0] == 'E'&&recvBuf[1] == 'O'&&recvBuf[2] == 'F')
			{
				count -= 4;
				break;
			}
			if (count>size)
			{
				count -= 4;
				outfile.write(recvBuf, cc - 4);
				break;
			}
		}
		printf("------------------------------------\n");
		cout << "Receive " << count << " bytes successfully!\n";
		printf("------------------------------------\n\n");
	}

}
