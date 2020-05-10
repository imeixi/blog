#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import smtplib
# sending_from_file
# Import the email modules we'll need
from email.message import EmailMessage
# Parser Header
from email.parser import BytesParser, Parser
from email.policy import default


class EmailHandler():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # 163邮箱服务器
        self.pop3_server = 'pop.163.com'
        self.smtp_server = 'smtp.163.com'
        self.imap_server = 'imap.163.com'
        self.email = 'imeixi@163.com'

    def sending_from_file(self, text_file):
        # Open the plain text file whose name is in textfile for reading.
        with open(text_file) as fp:
            # Create a text/plain message
            msg = EmailMessage()
            msg.set_content(fp.read())

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = f'Send message From file'
        msg['From'] = self.email
        msg['To'] = self.email

        s = smtplib.SMTP(self.smtp_server)
        s.login(self.username, self.password)
        s.send_message(msg)
        s.quit()

    def parser_header_from_file(self, text_file):
        # If the e-mail headers are in a file, uncomment these two lines:
        with open(text_file, 'rb') as fp:
            headers = BytesParser(policy=default).parse(fp)
        # Now the header items can be accessed as a dictionary:
        print('To: {}'.format(headers['to']))
        print('From: {}'.format(headers['from']))
        print('Subject: {}'.format(headers['subject']))
        print('Content: \n{}'.format(headers.get_content()))

        # You can also access the parts of the addresses:
        print('Recipient username: {}'.format(headers['to'].addresses[0].username))
        print('Sender name: {}'.format(headers['from'].addresses[0].display_name))

        s = smtplib.SMTP(self.smtp_server)
        s.login(self.username, self.password)
        s.send_message(headers)
        s.quit()

    def parser_header_from_text(self):
        #  Or for parsing headers in a string (this is an uncommon operation), use:
        headers = Parser(policy=default).parsestr(
            'From: IMEIXI <imeixi@163.com>\n'
            'To: <imeixi@163.com>\n'
            'Subject: Test message\n'
            '\n'
            'Body would go here\n')

        #  Now the header items can be accessed as a dictionary:
        print('To: {}'.format(headers['to']))
        print('From: {}'.format(headers['from']))
        print('Subject: {}'.format(headers['subject']))
        print('Content: \n{}'.format(headers.get_content()))

        # You can also access the parts of the addresses:
        print('Recipient username: {}'.format(headers['to'].addresses[0].username))
        print('Sender name: {}'.format(headers['from'].addresses[0].display_name))

        s = smtplib.SMTP(self.smtp_server)
        s.login(self.username, self.password)
        s.send_message(headers)
        s.quit()


if __name__ == '__main__':
    # 命令行输入三个参数，第1个参数 sys.argv[0] 是脚本名称，第2个是邮箱用户名，第3个是邮箱密码
    if len(sys.argv) < 2:
        user = input('please input email username: ')
        pw = input('please input email password: ')
    elif len(sys.argv) < 3:
        user = sys.argv[1]
        pw = input('please input email password: ')
    else:
        user = sys.argv[1]
        pw = sys.argv[2]

    email = EmailHandler(user, pw)
    # email.sending_from_file('testfile')
    email.parser_header_from_file('header')


