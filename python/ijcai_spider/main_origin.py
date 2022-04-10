''' 
crawl reports from google
last modified by zw
'''
import time
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import json
import io
import os
from os.path import join as pjoin

import urllib.parse  # url coding
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import socket
import random
import hashlib

# 将selenium改成不阻塞
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

ROOT_PATH = os.path.dirname('.')
delete_list = ['snopes.com', 'politifact.com', 'factcheck.org', 'checkyourfact.com']


class GoogleScholarCommon():

    # 这里url是要搜索的关键词
    def __init__(self, wait_time=5, url="https://www.google.com/search?q=", ds_name='test'):
        self.dataset_name = ds_name
        self.gs_url = url
        self.driver = webdriver.Chrome("chromedriver.exe")  # 需要chromedriver
        self.wait_time = wait_time
        self.source = self.driver.page_source

    def search_cite(self):
        """搜索website并返回
        """
        claim_reports = dict()
        claim_reports['reports'] = []
        # self.driver.implicitly_wait(self.wait_time) # 等待时间，为避免被机器人抓，不知道到底需不要等啊，我暂且是这么写的
        # 打开google搜索主页url：self.driver.get(self.gs_url) 
        self.driver.get('https://www.google.com/')
        self.driver.implicitly_wait(self.wait_time)
        input_box = self.driver.find_element_by_css_selector("input[name='q']")  # 查找元素
        submit_btn = self.driver.find_element_by_css_selector("input[name='btnK']")
        # 清空已有搜索词 keyword=u'中国'
        input_box.click()
        input_box.clear()

        # 自动填入-搜索词，提交
        claim_reports['claim'] = self.gs_url
        input_box.send_keys(self.gs_url)
        submit_btn.submit()
        self.driver.implicitly_wait(self.wait_time)  # 等待时间
        time.sleep(random.uniform(1.2, 2.1))  # 避免机器人，原理同上

        # 定位超链接, 循环点击爬取
        # link_list = self.driver.find_elements_by_css_selector('div > div > a[href^="/url?q=https://www."]')
        # link_list = self.driver.find_elements_by_css_selector('div.yuRUbf>a')

        # link_list[0].click()
        all_title_links = []
        N_page = 2
        while (N_page):
            source = self.driver.page_source  # 扒取网页源码
            bf = BeautifulSoup(source, "lxml")
            # # filtering delete_list !!!!! #soup.find_all("div", class_="g")
            all_title_links += self.filtering(bf.select('div.yuRUbf>a'), delete_list)
            time.sleep(random.uniform(2, 2.5))  # 避免机器人，原理同上
            # 爬取下一页
            self.driver.find_element_by_id('pnnext').click()  # 设置下一页内容
            N_page = N_page - 1
            time.sleep(random.uniform(1.5, 2))  # 避免机器人，原理同上

        # items = self.driver.find_elements_by_xpath('//*[@class="yuRUbf"]/a')
        counts = len(all_title_links)
        for i in range(counts):
            report = dict()  # 返回的reports
            # # 每次循环，都重新获取元素，防止元素失效或者页面刷新后元素改变了
            # items = self.driver.find_elements_by_xpath('//*[@class="yuRUbf"]/a')

            # 循环点击获取的元素 
            # items[i].click() # 先点击-> link
            # link = self.driver.current_url
            link = all_title_links[i].get('href')  # get_attribute

            report_content, is_report = self.download_the_page(link)
            # 打印每次获取元素，调试用
            print(link)
            # link_id = hashlib.md5(link.encode('utf-8')).hexdigest()

            report['claim'] = self.gs_url
            report['report_link'] = link
            report['report_content'] = report_content
            report['report_is_report'] = is_report

            # 隐式等待，避免页面加载慢获取元素失败导致点击失效
            time.sleep(1)  # 避免机器人，原理同上
            self.driver.back()  # 后退
            time.sleep(random.uniform(1, 2))  # 避免机器人，原理同上
            # source = self.driver.page_source # 扒取网页源码

            # saving
            claim_reports['reports'].append(report)

        self.write2file(pjoin(ROOT_PATH, f'snopes/{self.dataset_name}/{_generate_uid()}.json'), claim_reports)

        # links = re.findall(r'https://webcache.googleusercontent.com/search\?q=.*?https://(.*?)\+\&amp', source)
        # print(re.findall(r'https://webcache.googleusercontent.com/search\?q=.*?https://(.*?)\+\&amp', source)) # 模式匹配得到搜索结果
        # time.sleep(4) # 避免机器人，原理同上
        # # 这里在做模拟点击下一页，注意，这里下一页，需要特地设置。模拟点击后操作和之前一样
        # self.driver.find_element_by_id('pnnext').click() # 设置下一页内容
        # source = self.driver.page_source
        # print(re.findall(r'https://webcache.googleusercontent.com/search\?q=.*?https://(.*?)\+\&amp', source))
        # 关闭
        self.driver.quit()

    def download_the_page(self, url):
        socket.setdefaulttimeout(5)
        # proxies = get_proxies(proxy_pool)
        # print(proxies)
        try:
            print("download the page...")
            html = requests.get(url, timeout=(8, 9)).text
        except requests.exceptions.RequestException as err:
            print(err)
            return None, False
        except socket.timeout as tout:
            print(tout)
            return None, False
        bs = BeautifulSoup(html, 'html.parser')
        p_items = bs.find_all('p')
        text_list = []
        for p_item in p_items:
            p_text = p_item.text.strip()
            if judge_text(p_text):
                text_list.append(p_text)
        is_report = judge_report(text_list)
        report_content = '\n'.join(text_list)
        print(url)
        print(report_content)
        return report_content, is_report

    def filtering(self, all_title_links, delete_list):
        # bf.select('div > div > a[href^="/url?q=https://www."]')[0]['href']
        # link { h3}
        ret_links = []
        for i, link in enumerate(all_title_links):
            # delete links if they are in link['href']
            continue_flag = False
            for ditem in delete_list:
                if ditem in link.get('href'):
                    continue_flag = True
                    break
            if continue_flag: continue
            ret_links.append(link)
        return ret_links

    def write2file(self, out_path, data):
        with io.open(out_path, 'ab+') as data_file:
            data = json.dumps(data, ensure_ascii=False, indent=4)
            data_file.write(data.encode('utf8', 'replace'))
        print(f'##save at {out_path}')


def judge_text(text):
    if text == '':
        return False
    if '\n\n' in text:
        return False
    return True


def judge_report(text_list):
    if len(text_list) < 3:
        return False
    return True


import time


def _generate_uid():
    n = 0
    previous_time = ''
    current_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))[2:]
    if previous_time != current_time:
        n = 0
    n = n + 1
    previous_time = current_time
    # return str(current_time) + '%02d' % n + '%02d' % random.randint(10,99)#'%02d' % n
    return str(current_time) + '%02d' % random.randint(10, 99)


# _generate_code = _generate_code_func()


with open("test_links.txt", "r") as f:  # 打开文件读取信息
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        print(re.findall(r'https://www.google.com/search\?q=(.*)', line)[
                  0])  # 这里txt文件中给的数据，和要搜查的网址是不匹配的，每个地址多出来个https://www.google.com/search
        gs = GoogleScholarCommon(
            url=re.findall(r'https://www.google.com/search\?q=(.*)', line)[0])  # 这里我是一行行读取的，写代码比较匆忙，后期调整吧
        # gs = GoogleScholarCommon()
        gs.search_cite()
