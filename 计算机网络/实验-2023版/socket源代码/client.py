from socket import*
import time
#客户端调用socket()创建UDP套接字
clientSocket=socket(AF_INET,SOCK_DGRAM)#IPv4,UDP
#使用settimeout函数限制recvfrom()函数的等待时间为1秒（设置套接字超时值1s）
clientSocket.settimeout(1)
count=0#计数接收pong报文失败次数
start=0#第一次成功接收pong报文后用于计算RRT
totaltime=0#用于计算平均RRT
for i in range(10):  #发送10次ping报文
    print("测试"+str(i)) #报文内容
    t1=time.time()#RRT开始计数时间
    clientSocket.sendto("ping".encode("utf-8"),("localhost",10000))#将信息转换为byte后发送到指定服务器端,ADDRESS
    #b"ping" 表示一个字节类型的对象，其中的内容是由字符串 "ping" 经过 UTF-8 编码后的字节序列
    try:
        message,address=clientSocket.recvfrom(1024)#调用recvfrom()函数接收服务器发来的应答数据
        t2 = time.time()  # RRT结束计数时间
        print(message)
    except: #超时处理，等到时间超过1秒，捕获抛出的异常后打印丢失报文，进行下一步操作
        print("打印超时！！")
        count = count+1
        continue
    if(start==0):#计算ping消息的最小、最大和平均RRT，并计算丢包率
        mintime=(t2-t1)/2  ;  maxtime=(t2-t1)/2  ;  start=1
    elif((t2-t1)/2<mintime):
        mintime = (t2-t1)/2
    elif((t2-t1)/2>maxtime):
        maxtime = (t2-t1)/2
    totaltime=totaltime+(t2-t1)/2
    print('%.15f'%((t2-t1)/2))
    #print("flags")
#print调试，发现start==0,count ==10,flags也一直没有出现。
print('最小RRT:'+str(mintime))
print('最大RRT:'+str(maxtime))
print('平均RRT:'+str(totaltime/(10-count)))
print('丢包率 :'+str(count/10))

clientSocket.close()
