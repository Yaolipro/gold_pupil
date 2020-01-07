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

        pat1 = '<li><p>行情日期：(.+?)</p></li>'
        pat2 = '<li><p>上海金早盘价（元/克）</p><span class="colorRed fs20">(.+?)</span></li>'
        pat3 = '<li><p>上海金午盘价（元/克）</p><span class="colorRed fs20">(.+?)</span></li>'
        pat4 = '<li><p>上海银早盘价（元/千克）</p><span class="colorRed fs20">(.+?)</span></li>'
        pat5 = '<li><p>上海银午盘价（元/千克）</p><span class="colorRed fs20">(.+?)</span></li>'

        statis_time = re.compile(pat1).findall(data)[0]
        gold_1_price = re.compile(pat2).findall(data)[0]
        gold_2_price = re.compile(pat3).findall(data)[0]
        silver_1_price = re.compile(pat4).findall(data)[0]
        silver_2_price = re.compile(pat5).findall(data)[0]

        with open('gold_price.txt', 'a+') as fh:
            content = "日期：" + get_today() + "\t行情日期：" + statis_time + "\n" \
                      + "金早盘价：" + gold_1_price + "\t" + "金午盘价：" + gold_2_price + "\n" \
                      + "银早盘价：" + silver_1_price + "\t" + "银午盘价：" + silver_2_price + "\n"
            fh.write(content)

        return content
    except Exception as e:
        return "not available, %s" % str(e)


if __name__ == "__main__":
    content = get_gold()
    content += '金价下线：275, 上线285'
    e = Email(MAIL_USER, MAIL_PASS, MAIL_HOST)
    e.send(RECEIVERS, "黄金瞳", content)

