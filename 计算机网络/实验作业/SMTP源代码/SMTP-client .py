import base64
import re
import socket

msg = "\r\n  计算机网络如此精彩！！"
endmsg = "\r\n.\r\n"
# TAG: 服务器地址
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.163.com'  # Fill in start   #Fill in end
port = 25
ssl_port = 994
# mailserver_ip = socket.gethostbyname(mailserver)
src_of_email = "m15983633145@163.com"
passwords = 'FZLEQMYSTNWXDOLR1'  # 授权码，不是密码
dst_of_email = "3123747229@qq.com"
login_id = base64.b64encode(src_of_email.encode()).decode() + '\r\n'
login_pwd = base64.b64encode(passwords.encode()).decode() + '\r\n'

# TAG: 建立连接
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, port))
print('connect成功')

#Fill in end
recv0 = clientSocket.recv(1024).decode()
print(recv0)
if recv0[:3] != '220':
    print('[1]220 reply not received from server.')

# TAG: 1.HELLO
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# TAG: 登录
log_command = 'AUTH LOGIN\r\n'
clientSocket.send(log_command.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
    print('334 login wrong')

clientSocket.send(login_id.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '535':
    print('Login ID wrong')

clientSocket.send(login_pwd.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '535':
    print('Password wrong')

# TAG: 2.MAIL FROM
# Send MAIL FROM command and print server response.
# Fill in start
mailfrom = 'MAIL FROM: <' + src_of_email + '>\r\n'
clientSocket.send(mailfrom.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# TAG: 3.RCPT TO
# Send RCPT TO command and print server response.
# Fill in start
rcptto = 'RCPT TO: <' + dst_of_email + '>\r\n'
clientSocket.send(rcptto.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# TAG: 4.DATA
# Send DATA command and print server response.
# Fill in start
data = 'DATA\r\n'
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end

# TAG: 5.Send message
# Send message data.
# Fill in start
send = "From: " + src_of_email + '\r\n'
send += "To: " + dst_of_email + '\r\n'
send += "Subject: " + 'First Web Mail Test From  陈宇森   \r\n'
send += msg
clientSocket.send(send.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# TAG: 6.QUIT
# Send QUIT command and get server response.
# Fill in start
quit = 'QUIT\r\n'
clientSocket.send(quit.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')
# Fill in end
clientSocket.close()
