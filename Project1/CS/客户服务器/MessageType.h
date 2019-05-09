#ifndef MESSAGETYPE_H
#define MESSAGETYPE_H
#pragma warning(disable:4996)
enum MessageType {
	MTYPE_LIST = 0,			//客户：请求列表	服务器：返回列表
	MTYPE_FILE= 1,			//客户：所请求文件的名字
	MTYPE_END=2
};

#endif // !MESSAGETYPE_H


