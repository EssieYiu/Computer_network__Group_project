def pack_message(selfIP,message,destIP):
    '''
    # IP无论如何都用15位表示，不够的后面补'.0000'
    addition='00000000'
    if len(destIP)<15:
        need=15-len(destIP)-1#要补的0的个数
        zero=addition[:need-1]#后面要补的0
        dIP=destIP+'.'+zero
    srcIP=self.ip
    if len(srcIP)<15:
        need=15-len(srcIP)-1
        zero=addition[:need-1]
        sIP=srcIP+'.'+zero

    packed_message='1'+sIP+dIP+message   #最前面的'1'代表发送的信息为消息 0 1:15 16:30
    return packed_message.encode()
    '''

    message_to_send = selfIP+' '+destIP+' '+message
    return message_to_send

def unpack_message(message):
    '''
    #解读消息
    tup=(message[1:15],message[16:30],message[31:]) #srcIP,destIP,message
    return tup
    '''
    tup = message.split(' ',3)
    return tup

if __name__ == "__main__":
    packed = pack_message(192.45.44.5","messssssage!!!! dfsfsfdf fd dddd","178.45.67.7")
    print('packed is:',pack_message)
    unpack = unpack_message(packed)
    print('unpacked is:',unpack)
