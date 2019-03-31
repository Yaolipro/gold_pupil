# -*- coding: utf-8 -*-

"""
@created on 2019/3/31
@author Yao Li
@desc 频次爬取http://www.sge.com.cn/(上海黄金交易所)的黄金价格，并自动发送到邮箱
"""

import urllib2
import re
import datetime

from notice import Email
from setting import MAIL_USER, MAIL_PASS, MAIL_HOST, RECEIVERS

URL = "http://www.sge.com.cn/"


def url_open(url):
    try:
        req = urllib2.Request(url)
        req.add_header(
            "user-agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"
        )
        return urllib2.urlopen(req).read()
    except:
        pass


def get_today():
    h = datetime.datetime.now()
    today = h.strftime("%Y-%m-%d")
    return today


def get_gold():
    try:
        data = url_open(URL)

        pat1 = '<span class="fl color999">（截止日期: (.*?)）'
        pat2 = '<span class="colorRed fs24">(.+?)<'

        statis_time = re.compile(pat1).findall(data)[0]
        today_price = re.compile(pat2).findall(data)[0]

        with open('gold_price.txt', 'a+') as fh:
            fh.write("日期：" + get_today() + "\t截止日期" + statis_time + "\t" + "早盘价：" + today_price + "\n")

        return str(today_price)
    except Exception as e:
        return "not available, %s" % str(e)


if __name__ == "__main__":
    value = get_gold()
    content = '日期：%s, 价格：%s' % (get_today(), value)
    content += '\n下线：275, 上线285'
    e = Email(MAIL_USER, MAIL_PASS, MAIL_HOST)
    e.send(RECEIVERS, "黄金瞳", content)

