#include"sendAndRecv_S.h"
bool recvAndSend(SOCKET sock)
{
	char recvBuf[BUFLEN + 1];
	char name[300];
	int b = recv(sock, recvBuf, BUFLEN, 0);	//接收客户发来的请求
	if (b == SOCKET_ERROR)
	{
		printf("接收错误: %d\n", WSAGetLastError());
		return false;
	}
	//printf("%s", recvBuf);
	switch (recvBuf[0])
	{
	case MTYPE_LIST + '0':	//请求资源列表
		printf("* Client ask for resource list\n");
		if(!sendList(sock))
			return false;
		break;
	case MTYPE_FILE+ '0':	//请求特定文件
		strcpy(name, recvBuf + 1);
		printf("* Client ask for %s\n", name);
		if(!sendFile(sock, name))
			return false;
		break;
	case MTYPE_END+'0':
		printf("* Client quit\n");
		return false;
		break;
	default:
		return false;
		//cout << "default\n";
	}
	return true;
}
bool sendList(SOCKET sock)
{
	char sendBuf[BUFLEN + 1];
	int b;
	string files;
	_finddata_t fileInfo;
	int num = 0;	//文件编号
	string path = "C:\\Users\\galaxy\\Documents\\test-CS\\*.*";	//服务器存储资源的目录
	long Handle = _findfirst(path.c_str(), &fileInfo);	//找到文件
	
	if (Handle == -1L)
	{
		cout << "Handle==-1L" << endl;
		cout << "can not open" << endl;
		return false;
	}
	do
	{
		num++;
		files += to_string(num);	//编号
		files += ".";
		files += fileInfo.name;		//文件名字
		//cout << files << endl;
		files += "\n";
	} while (_findnext(Handle, &fileInfo) == 0);	//循环找文件
	//cout << files << endl;
	strcpy(sendBuf, "0");
	strcat(sendBuf, files.c_str());
	//printf("sendBuf: %s", sendBuf);
	_findclose(Handle);
	b = send(sock, sendBuf, strlen(sendBuf) + 1, 0);	//发送资源列表
	if (b == SOCKET_ERROR)
	{
		printf("Send resource list failed: %d\n", WSAGetLastError());
		return false;
	}
	printf("--------------------------------\n");
	printf("Send resource list successfully!\n");
	printf("--------------------------------\n");
	return true;
}
bool sendFile(SOCKET sock, char* name)
{
	char sendBuf[BUFLEN + 1];
	int cc;
	long count=0;
	string path = "C:\\Users\\galaxy\\Documents\\test-CS\\";	//服务器资源存储的目录
	string fileName = name;
	string toFind= path + name;	//资源路径
	//cout << "toFind: " << toFind << endl;	
	ifstream infile(toFind, ios::in | ios::binary);	// 以二进制方式打开
	if (infile.is_open() != true)
	{
		printf("%s can not open",name);
		strcpy(sendBuf, "2");//消息类型：文件
		strcat(sendBuf, "0");//文件大小为0
		cc = send(sock, sendBuf, strlen(sendBuf) + 1, 0);	//打包发送给客户
		return true;
	}
	infile.seekg(0, ios::end);	// 将指针定位到文件结尾处
	long size = infile.tellg();	// 获得文件大小
	infile.seekg(0, ios::beg);	// 将指针回到文件开始处
	char Size[10000];
	itoa(size, Size, 10);
	itoa(MTYPE_FILE, sendBuf, 10);	// 消息类型	
	strcat(sendBuf, Size);	//文件大小
	cc = send(sock, sendBuf, strlen(sendBuf) + 1, 0);	//打包发送给客户
	if (cc == SOCKET_ERROR)
	{
		printf("Send file failed: %d\n", WSAGetLastError());
		return false;
	}
	while (1)
	{
		memset(sendBuf, 0, sizeof(sendBuf));
		infile.read(sendBuf, BUFLEN);	// 将缓冲区大小的文件读进sendBuf
		int bytes = infile.gcount();	// 实际读进sendBuf的字节
		int pos = infile.tellg();		// 获取指针位置
		cc = send(sock, sendBuf, bytes, 0);	//	给客户发送文件
		if (cc == SOCKET_ERROR)
		{
			printf("Send file failed: %d\n", WSAGetLastError());
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
	strcpy(sendBuf, "EOF");
	send(sock, sendBuf, strlen(sendBuf) + 1, 0);
	printf("--------------------------------\n");
	printf("Send %s successfully\n", name);
	string s = "Sent ";
	char num[100];
	itoa(count, num, 10);
	s += num;
	s += " bytes\n";
	cout << s;
	printf("--------------------------------\n");
	return true;
}
