from socket import *
import random
# 创建一个 UDP 套接字（SOCK_DGRAM）
#服务端通过调用socket创建套接字来启动服务器
serverSocket = socket(AF_INET, SOCK_DGRAM)
#服务器调用 bind( ) 指定服务器的套接字地址
serverSocket.bind(('localhost', 10000))#127.0.01.1 或者使用本机的10.129.144.1
count = 0  # 已回复的次数
while True:
    rand = random.randint(1, 10)
    #print("随机数：： ",rand)
    # 服务端调用recvfrom()等待接收数据，此时阻塞
    message, address = serverSocket.recvfrom(1024)
    # 成功接收消息后继续运行
    print(message)
    message = message.upper()#Q:目的？
    count += 1
    # 模拟 30% 的数据包丢失。
    if rand < 4:
        continue
    #服务器接收到客户端发来的数据后，调用sendto()向客户发送应答数据
    serverSocket.sendto(message, address)
    if count == 10:  # 进行10次，退出循环以结束服务器
        break
serverSocket.close()