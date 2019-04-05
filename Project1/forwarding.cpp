#include"forwarding.h"
bool forwarding(SOCKET from, sockaddr_in f, SOCKET to, sockaddr_in t)
{
	char recvBuf[BUFLEN + 1];
	memset(recvBuf, 0, sizeof(recvBuf));
	int rc, sc;
	long long rcount = 0;
	long long scount = 0;
	rc = recv(from, recvBuf, BUFLEN, 0);              // 服务器接收要转发给Client2的消息；第二个参数指向缓冲区，第三个参数为缓冲区大小(字节数)，第四个参数一般设置为0，返回值:(>0)接收到的字节数,(=0)对方已关闭,(<0)连接出错
	if (rc == SOCKET_ERROR)                          // 出错。其后必须关闭套接字sock
	{
		printf("接收错误: %d\n", GetLastError());
		return false;
	}
	else
	{
		rcount += rc;
		sc = send(to, recvBuf, rc, 0);
		if (sc == SOCKET_ERROR)                          // 出错
		{
			printf("转发错误: %d\n", GetLastError());
			return false;
		}
		scount += sc;
		if (!strcmp(recvBuf, "BYE"))				//Client发来BYE
		{
			printf("Client%s 已退出!\n", inet_ntoa(f.sin_addr));
			return false;
		}
		if (strcmp(recvBuf, "NOTHING"))				//不是NOTHING,则是文件，第一次收到的是格式+大小信息,要减掉大小（只算文件大小）
		{
			rcount -= rc;
			scount -= sc;
			string info = recvBuf;
			int pos = info.find('-');
			string form, size;
			long Size;
			form = info.substr(0, pos);
			size = info.substr(pos + 1, info.size() - pos - 1);
			Size = atol(size.c_str());				//文件大小
			while (1)
			{
				memset(recvBuf, 0, sizeof(recvBuf));
				rc = recv(from, recvBuf, BUFLEN, 0);	//接收
				if (rc == SOCKET_ERROR)                 // 出错
				{
					printf("接收错误: %d\n", GetLastError());
					return false;
				}
				//cout << "收到" << rc << endl;
				rcount += rc;
				sc = send(to, recvBuf, rc, 0);		//转发
				if (sc == SOCKET_ERROR)            // 出错
				{
					printf("转发错误: %d\n", GetLastError());
					return false;
				}
				scount += sc;
				//cout << "转发" << sc << endl;
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
		printf("收到来自%s: %d字节数据\n", inet_ntoa(f.sin_addr), rcount);
		printf("成功转发到%s: %d字节数据\n", inet_ntoa(t.sin_addr), scount);
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
		rc = recv(from, recvBuf, BUFLEN, 0);//发来的
		if (rc == SOCKET_ERROR)
		{
			printf("接收失败%d\n", GetLastError());
			break;
		}
		cout << "接收" << rc << endl;
		
		sc = send(to, recvBuf, rc, 0);
		cout << "转发" << endl;
		if (sc == SOCKET_ERROR)
		{
			printf("转发失败%d\n", GetLastError());
			break;
		}
		Sleep(5);
		if (rc==4&&recvBuf[0]=='E'&&recvBuf[1]=='O'&&recvBuf[2]=='F')//接收到EOF
		{

			printf("文件结束\n");
			break;
		}
		rcount += rc;
		scount += sc;
		if (!strcmp(recvBuf, "NOTHING"))//接收到NOTHING
			break;
	}*/
	
