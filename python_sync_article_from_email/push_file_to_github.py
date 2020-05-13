#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import base64
import json
import sys
import os
from hashlib import sha1


# 文件base64 加密
def file_base64(filename):
    with open(filename, 'rb') as f:
        fn_b64 = base64.b64encode(f.read()).decode('utf-8')
    return fn_b64


def get_blob_sha(s):
    # s是个字符串，也就是文件里的内容。
    sha1_obj = sha1()
    content = s.encode('ascii')	# 以二进制编码
    content = b'blob %d\0' % len(content) + content
    sha1_obj.update(content)
    return sha1_obj.hexdigest()


def push_file(url, tokens, fn):
    # 准备put的json数据，其中content是经过base64位编码后的 文件字节流
    data = {
        "message": "my commit message",
        "committer": {
            "name": "imeixi",
            "email": "zheng.ah.r@gmail.com"
        },
        "content": file_base64(fn),
        "sha": get_blob_sha(file_base64(fn))
    }
    # token 授权
    headers = {"Authorization": 'token ' + tokens}
    # put方法将文件推送到服务端
    res = requests.put(url, data=json.dumps(data), headers=headers)
    if res.status_code == 201:
        print('success')
    else:
        print('response code: ' + str(res.status_code))
        print('response message: ' + str(res.text))


if __name__ == '__main__':
    # 命令行输入三个参数，第1个参数 sys.argv[0] 是脚本名称，第2个是github token
    if len(sys.argv) == 1:
        token = input('please input github token: ')
    elif len(sys.argv) == 2:
        token = sys.argv[1]

    imeixi_dir = './imeixi'
    for root, dirs, files in os.walk(imeixi_dir, topdown=True):
        for name in files:
            url_imeixi = 'https://api.github.com/repos/imeixi/blog/contents/source/_posts/' + name
            file = os.path.join(root, name)
            print(file)
            push_file(url_imeixi, tokens=token, fn=file)
        for name in dirs:
            print(os.path.join(root, name))

    time_diary_dir = './time_diary'
    for root, dirs, files in os.walk(time_diary_dir, topdown=False):
        for name in files:
            url_time_diary = 'https://api.github.com/repos/imeixi/timediary/contents/source/_posts/' + name
            file = os.path.join(root, name)
            print(file)
            push_file(url_time_diary, tokens=token, fn=file)
        for name in dirs:
            print(os.path.join(root, name))
