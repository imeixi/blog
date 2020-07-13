---
title: Python网络数据采集
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
date: 2020-07-01 21:31:30
img:
coverImg:
password:
summary:
type:
---

### 前言

------

示例源码： https://github.com/REMitchell/python-scraping

案例：http://wefeelfine.org

pyhton基础：《Python 语言及其应用》

​						video ：http://shop.oreilly.com/product/110000448.do



#### 第1章 初见网络爬虫

urllib库：  http://docs.python.org/3/library/urllib.html

```python
from urllib.request input urlopen
html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())
```

#### 第2章 复杂的HTML

BeautifulSoup库：https://beautifulsoup.readthedocs.io/zh_CN/latest/

​								https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

findAll(tag, attributes, recursive, text, limit, keywords)

find(tag, attributes, recursive, text, keywords)



正则表达式：在线测试网站  http://regexpal.com









