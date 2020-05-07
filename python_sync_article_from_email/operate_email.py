#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import poplib
import smtplib
import email.utils
from email.parser import Parser


class OperateEmail:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # 163邮箱服务器
        self.pop3_server = 'pop.163.com'
        self.smtp_server = 'smtp.163.com'
        self.imap_server = 'imap.163.com'
        self.email = 'imeixi@163.com'

    def send_mail_by_smtp(self):
        _from = self.email
        _to = self.email
        _tos = _to.split(';')
        _subj = "test smtp send"
        _date = email.utils.formatdate()

        # 标准提头，后面是空行，然后是文本
        head = 'From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n' % (_from, _to, _subj, _date)
        message = 'this is a test email sended from python program.'
        content = head + message

        print('Connecting...\n' + '-' * 80)
        print(content + '\n' + '-' * 80 + '\n')
        server = smtplib.SMTP(self.smtp_server)
        server.login(self.username, self.password)
        result = server.sendmail(_from, _tos, content)

        if result:
            print("Failed recipients:", result)
        else:
            print('No errors.')

        server.quit()
        print('bye\n' + '-' * 80)

    def rec_email_by_pop3(self):
        input('Ready fo receive emails?')
        print('Connecting...')
        # 连接pop3服务器  # 身份认证
        server = poplib.POP3(self.pop3_server)
        server.user(self.username)
        server.pass_(self.password)

        # 打开调试信息
        server.set_debuglevel(0)

        try:
            # 打印pop3服务器的欢迎文字
            print(server.getwelcome())
            msg_count, msg_bytes = server.stat()
            print('There are %s mail messages in %s' % (msg_count, msg_bytes))

            print(server.list())
            print('-' * 80)
            input('[Press Enter to Continue]')

            for i in range(msg_count):
                hdr, message, octets = server.retr(i+1)  # octets 是字节数
                for line in message:
                    print(line.decode('utf-8'))
                print('-' * 80)
                if i < msg_count-1:
                    input('[Press Enter to Continue]')

            # 可以根据邮件索引号直接从服务器删除邮件:
            server.dele(msg_count)

        finally:
            # 关闭连接:
            server.quit()


if __name__ == '__main__':
    # 命令行输入三个参数，第1个参数 sys.argv[0] 是脚本名称，第2个是邮箱用户名，第3个是邮箱密码
    while len(sys.argv) != 3:
        print('please input email username and password. ')

    user = sys.argv[1]
    pw = sys.argv[2]
    operate_email = OperateEmail(user, pw)
    operate_email.send_mail_by_smtp()
    operate_email.rec_email_by_pop3()