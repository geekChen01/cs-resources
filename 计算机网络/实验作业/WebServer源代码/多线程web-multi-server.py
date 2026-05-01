from socket import *
import sys, threading


def web_mul(ip, port):
    # 服务器端通过调用socket()创建套接字来启动一个服务器
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_address = ('', port)  # 接收传入的ip地址与端口号
    # 服务器调用bind()绑定指定服务器的套接字地址（IP 地址 + 端口号）
    serverSocket.bind(server_address)

    # 服务器调用listen()做好侦听准备，同时规定好请求队列的长度
    Length = 1024
    try:
        serverSocket.listen(5)
    except socket.error:
        print("fail to listen on port %s" % error)
        sys.exit(1)
    while True:
        print("Ready to server...")
        connectionSocket, addr = serverSocket.accept()
        print('accepted!' + str(addr))
        try:
            # 通过TCP 套接字接收 HTTP 请求
            message = connectionSocket.recv(Length)
            message = message.split()[1]
            msg_de = message.decode('utf-8')
            print('file msg from client: ' + msg_de)
            # 收到客户端断开连接消息
            if msg_de == '\disconnect': break
            # 从服务器的文件系统读取客户端请求的文件
            filename = message
            f = open(filename[1:])
            text = f.read()
            # 被请求文件存在，创建一个由被请求的文件组成的“请求成功”HTTP 响应报文
            output = "HTTP/1.1 200 OK\r\n"
            output += "\r\n"
            output += '\r\n'
            output += msg_de + ' has been successfully received.\n'
            output = output.encode('utf-8')
            print('output: ' + str(output))
            # 通过 TCP 连接将响应报文发回客户端
            connectionSocket.send(output)
            for i in range(0, len(text)):
                connectionSocket.send(text[i].encode('utf-8'))
            print('send!')
        except IOError:
            # 被请求文件不存在，创建“请求目标不存在”HTTP 响应报文
            output = "HTTP/1.1 200 OK\r\n"
            output += "\r\n"
            output += '\r\n'
            output += '         404 not found. \n The request has failed.\n'
            output = output.encode('utf-8')
            print('output: ' + str(output))
            # 通过 TCP 连接将响应报文发回客户端
            connectionSocket.send(output)

    print("finish test, close connect")
    # 通过close()关闭套接字
    connectionSocket.close()
    serverSocket.close()


if __name__ == '__main__':
    t1 = threading.Thread(target=web_mul, args=('127.0.0.1', 4001))
    t2 = threading.Thread(target=web_mul, args=('127.0.0.1', 4002))
    t3 = threading.Thread(target=web_mul, args=('127.0.0.1', 4003))
    t1.start()
    t2.start()
    t3.start()