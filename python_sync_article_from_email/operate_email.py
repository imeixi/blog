#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import poplib
import smtplib
import email.utils
from email.message import Message
from email.parser import Parser
from email.header import decode_header
from email.header import Header
from email.utils import parseaddr


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

    def send_mail_by_message(self):
        m = Message()
        m['from'] = self.email
        m['to'] = self.email
        m['subject'] = 'form email.message import Message'
        m.set_payload('This email is send by python script with email.message Message')

        s = str(m)
        print(s)
        print('\n' + '-' * 80)

        x = Parser().parsestr(s)
        print(x)
        print('\n' + '-' * 80)

        print(x['From'])
        print(x.get_payload())
        print(x.items())

    @staticmethod
    def decode_str(s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    @staticmethod
    def guess_charset(msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    @staticmethod
    def get_email_headers(msg):
        # 邮件的From, To, Subject存在于根对象上:
        headers = {}
        for header in ['From', 'To', 'Subject', 'Date']:
            value = msg.get(header, '')
            if value:
                if header == 'Date':
                    headers['date'] = value
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    subject = OperateEmail.decode_str(value)
                    headers['subject'] = subject
                else:
                    # 需要解码Email地址:
                    hdr, address = parseaddr(value)
                    print(hdr)
                    print(address)
                    name = OperateEmail.decode_str(hdr)
                    value = u'%s <%s>' % (name, address)
                    if header == 'From':
                        from_address = value
                        headers['from'] = from_address
                    else:
                        to_address = value
                        headers['to'] = to_address
        content_type = msg.get_content_type()
        print('head content_type: ', content_type)
        return headers

    @staticmethod
    def get_email_content(message, base_save_path):
        j = 0
        content = ''
        attachment_files = []
        for part in message.walk():
            j = j + 1
            file_name = part.get_filename()
            content_type = part.get_content_type()
            # 保存附件
            if file_name:  # Attachment
                # Decode filename
                h = Header(file_name)
                dh = decode_header(h)
                print(dh)
                filename = dh[0][0]
                if dh[0][1]:  # 如果包含编码的格式，则按照该格式解码
                    # filename = filename.decode(dh[0][1])
                    filename = OperateEmail.decode_str(str(filename, dh[0][1])) #将附件名称可读化
                    print(filename)
                    print('_'*80)
                    # filename = filename.encode("utf-8")
                data = part.get_payload(decode=True)
                att_file = open(str(base_save_path) + str(filename), 'wb')
                attachment_files.append(filename)
                att_file.write(data)
                att_file.close()
            elif content_type == 'text/plain' or content_type == 'text/html':
                # 保存正文
                data = part.get_payload(decode=True)
                charset = OperateEmail.guess_charset(part)
                if charset:
                    charset = charset.strip().split(';')[0]
                    print('charset:', charset)
                    data = data.decode(charset)
                content = data
        return content, attachment_files

    def rec_email_by_pop3(self):
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

            resp, mails, octets = server.list()
            print('------ resp ------')
            print(resp)  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
            print('------ mails ------')
            print(mails)  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
            print('------ octets ------')
            print(octets)

            # 获取最新一封邮件, 注意索引号从1开始:
            msg_count = len(mails)
            for i in range(msg_count):
                resp, lines, octets = server.retr(i + 1)  # octets 是字节数
                # lines存储了邮件的原始文本的每一行,
                # 可以获得整个邮件的原始文本:
                msg_content = b'\r\n'.join(lines).decode('utf-8')

                # 把邮件内容解析为Message对象：
                msg = Parser().parsestr(msg_content)

                print(msg.get('From'))
                print(msg.get('To'))
                print(msg.get('Subject'))

                # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
                # 嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
                print('---------- 解析之后 ----------')
                msg_headers = OperateEmail.get_email_headers(msg)
                if msg_headers['subject'].__contains__('日记'):
                    base_save_path = './time_diary/'
                    content, attachment_files = OperateEmail.get_email_content(msg, base_save_path)
                elif msg_headers['subject'].__contains__('imeixi'):
                    base_save_path = './imeixi/'
                    content, attachment_files = OperateEmail.get_email_content(msg, base_save_path)
                else:
                    pass

                print('subject:', msg_headers['subject'])
                print('from_address:', msg_headers['from'])
                print('to_address:', msg_headers['to'])
                print('date:', msg_headers['date'])
                # print('content:', content)
                print('attachment_files: ', attachment_files)

            # 可以根据邮件索引号直接从服务器删除邮件:
            # server.dele(msg_count)

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
    # operate_email.send_mail_by_smtp()
    operate_email.rec_email_by_pop3()
    # operate_email.send_mail_by_message()
