# -*-coding:utf-8-*-
'''
Created on 2017年3月17日
@author: lavi
'''
import requests
from bs4 import BeautifulSoup
import bs4
import re


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parserPage(goodsList, html):
    tlt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
    plt = re.findall(r'\"raw_title\"\:\".*?\"', html)  # 添加问号使用最小匹配的
    for i in range(len(tlt)):
        title = eval(tlt[i].split(':')[1])  # eval()函数十分强大，可以将将字符串str当成有效的表达式来求值并返回计算结果
        price = eval(plt[i].split(':')[1])
        goodsList.append([title, price])


def printPage(goodsList):
    tplt = "{:6}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    for i in range(len(goodsList)):
        goods = goodsList[i]
        print(tplt.format(i + 1, goods[0], goods[1]))


def main():
    goods = "书包"
    depth = 2;
    url = "https://s.taobao.com/search?q="
    goodsList = []
    for i in range(depth):
        html = getHTMLText(url + goods + "&s=" + str(i * 44))
        parserPage(goodsList, html)
    printPage(goodsList)


main()