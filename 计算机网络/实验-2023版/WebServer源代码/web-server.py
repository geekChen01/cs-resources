from socket import *
import sys
def web_server(ip, port):
    # 服务器端通过调用socket()创建套接字来启动一个服务器
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)# 是一种设置套接字选项的方法，用于在服务器关闭后能够快速地重新启动。
    # SOL_SOCKET表示要设置的是套接字级别的选项,SO_REUSEADDR：表示要设置的选项是重用地址。这个选项允许在服务器关闭后立即重新启动服务器时，可以重用之前使用过的地址,1表示启用选项。
    server_address = ('', port)  # 接收传入的ip地址与端口号 # 将地址绑定到套接字后，它将能够接收到发送到该端口的数据包。无论数据包来自于哪个具体的网络接口，服务器都会接收它们。
    # 服务器调用bind()绑定指定服务器的套接字地址（IP 地址 + 端口号）
    serverSocket.bind(server_address)
    # 服务器调用listen()做好侦听准备，同时规定好请求队列的长度
    Length = 1024
    try:
        serverSocket.listen(5)#5:监听队列的最大长度，即同时可以排队等待处理的连接请求的最大数量
    except socket.error:
        print("fail to listen on port %s" % error)
        sys.exit(1)#来终止程序的执行，并返回一个非零的退出码（1）表示程序异常终止。
    while True:
        print("Ready to server...")
        connectionSocket, addr = serverSocket.accept()
        print('accepted!' + str(addr))
        try:
            # 通过TCP 套接字接收 HTTP 请求
            message = connectionSocket.recv(Length)
            message = message.split()[1]#改为A,作为纠错，分清下面的open(message/A)区别
            # print("msg: ",message) ,output:   msg:  b'/HelloWorld.html'
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
            output += msg_de + ' has been successfully received  ,good job  chen !!.\n   '
            output = output.encode('utf-8')
            print('output: ' + str(output))
            # 通过 TCP 连接将响应报文发回客户端
            connectionSocket.send(output)
            # for i in range(0, len(text)):
            #     connectionSocket.send(text[i].encode('utf-8'))
            print('send!')
        except IOError: #IOError 是 Python 中的一个标准异常类，用于表示输入/输出操作过程中的错误。它通常用于处理文件读写或网络通信等涉及输入/输出的操作。
            # 被请求文件不存在，创建“请求目标不存在”HTTP 响应报文
            output = "HTTP/1.1 200 OK\r\n"
            output += "\r\n"
            output += '\r\n'
            output += '             404 not found.   \n The request has failed.\n'
            output = output.encode('utf-8')
            print('output: ' + str(output))
            # 通过 TCP 连接将响应报文发回客户端
            connectionSocket.send(output)
    print("finish test, close connect")
    # 通过close()关闭套接字
    connectionSocket.close()
    serverSocket.close()
if __name__ == '__main__':
    web_server('127.0.0.1', 12000)