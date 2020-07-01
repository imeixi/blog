---
title: Python写网络爬虫（笔记）
author: imeixi
top: true
cover: true
toc: false
mathjax: false
categories: Markdown
tags:
  - Typora
  - Markdown
comments: false
date: 2020-07-01 20:03:50
img:
coverImg:
password:
summary:
type:
---

#### 第1章  网络爬虫简介

1.3.1  检查robots.txt 文件

​	确定哪些是可以抓取的内容

​	eg：https://www.taobao.com/robots.txt



1.3.3  估算网站大小

http://www.google.com/advanced_search

Google 搜索

 "site:example.webscraping.com"

 "site:www.imeixi.cn"

根据搜索结果，估算共有多少个网页



1.3.4 识别网站所用技术

```python
pip install buildwith

import builtwith
builtwith.parse('http://www.imeixi.cn')
```



1.3.5  寻找网站作者

```python
pip install python-whois

import whois
print(whois.whois('imeixi.cn'))
```



#### 第2章 数据抓取

2.2 三种网页抓取方法

2.2.1 正则表达式

https://docs.python.org/zh-cn/3/howto/regex.html

2.2.2 Beautiful Soup

2.2.3 Lxml



#### 第7章 验证码处理

7.1.1  加载验证码图像

 Pillow 处理图像包  Image类

https://pillow.readthedocs.io/en/stable/



7.2 光学字符识别  OCR

pip install pytesseract



7.3.2  9kw 入门

Https://www.9kw.eu

Https://www.9kw.eu/api.html





