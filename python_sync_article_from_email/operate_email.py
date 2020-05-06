#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import poplib
from email.parser import Parser


class OperateEmail:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # 163邮箱服务器
        self.pop3_server = 'pop.163.com'
        self.smtp_server = 'smtp.163.com'
        self.imap_server = 'imap.163.com'

    def recv_email_by_pop3(self):
        # 连接pop3服务器
        server = poplib.POP3(self.pop3_server)

        # 打开调试信息
        server.set_debuglevel(2)

        # 打印pop3服务器的欢迎文字
        print(server.getwelcome())

        # 身份认证
        server.user(self.username)
        server.pass_(self.password)

        # stat return the numbers of the email and the size of space
        print('server.stat()', server.stat())

        # list()返回所有邮件的编号：
        resp, mails, octets = server.list()

        # 查看所有邮件列表
        print("all mails", mails)

        # 获取最新的一封邮件，注意索引从1开始
        index = len(mails)
        resp, lines, octets = server.retr(index)

        print('resp', resp)
        print('lines', lines)
        print('octets', octets)

        # lines 存储了邮件的原始文本的每一行
        # 可以获得整个邮件的原始文本：
        msg_content = b'\r\n'.join(lines).decode('utf-8')

        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)

        # 可以根据邮件索引号直接从服务器删除邮件:
        # server.dele(index)
        # 关闭连接:
        server.quit()


if __name__ == '__main__':
    # 命令行输入三个参数，第1个参数 sys.argv[0] 是脚本名称，第2个是邮箱用户名，第3个是邮箱密码
    while len(sys.argv) != 3:
        print('please input email username and password. ')

    user = sys.argv[1]
    pw = sys.argv[2]
    operate_email = OperateEmail(user, pw)
    operate_email.recv_email_by_pop3()