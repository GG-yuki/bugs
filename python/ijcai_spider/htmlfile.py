import time
from selenium import webdriver
import re

class GoogleScholarCommon():

    # 这里url是要搜索的关键词
    def __init__(self, wait_time=120, url="https://www.google.com/search?q="):
        self.gs_url = url
        self.driver = webdriver.Chrome() # 需要chromedriver
        self.wait_time = wait_time
        self.source = self.driver.page_source

    def search_cite(self):
        """搜索website并返回
        """
        self.driver.implicitly_wait(self.wait_time) # 等待时间，为避免被机器人抓，不知道到底需不要等啊，我暂且是这么写的
        self.driver.get(self.gs_url)
        source = self.driver.page_source # 扒取网页源码
        print(source)
        print(re.findall(r'https://translate.google.com/translate\?hl=zh-TW&amp;sl=en&amp;u=(.*?)\&amp', source)) # 模式匹配得到搜索结果
        # time.sleep(3) # 避免机器人，原理同上
        # # 这里在做模拟点击下一页，注意，这里下一页，需要特地设置。模拟点击后操作和之前一样
        # self.driver.find_element_by_partial_link_text("下一頁").click() # 设置下一页内容，我的是台湾定位，所以是繁体字，也可以是数字，但是容易点到别的地方去
        # source = self.driver.page_source
        # print(re.findall(r'https://webcache.googleusercontent.com/search\?q=.*?https://(.*?)\+\&amp', source))


if __name__ == "__main__":
    # with open("test.txt", "r") as f: # 打开文件读取信息
    #     for line in f.readlines():
    #         line = line.strip('\n')  # 去掉列表中每一个元素的换行符
    #         print(re.findall(r'https://www.google.com/search\?q=(.*)', line)[0]) # 这里txt文件中给的数据，和要搜查的网址是不匹配的，每个地址多出来个https://www.google.com/search
    #         gs = GoogleScholarCommon(url=re.findall(r'https://www.google.com/search\?q=(.*)', line)[0]) # 这里我是一行行读取的，写代码比较匆忙，后期调整吧
    #         # gs = GoogleScholarCommon()
    #         gs.search_cite()
    gs = GoogleScholarCommon(url=r'https://www.google.com/search?q=Wisconsin+is+on+pace+to+double+the+number+of+layoffs+this+year.&sxsrf=AOaemvLT_7dfRtUVxt_m_hATILb8M76pHg%3A1639539392626&source=hp&ei=wGK5Ydb6I_Gk2roPiLikwAQ&iflsig=ALs-wAMAAAAAYblw0O3egcERLbVAZh3p7gKt8NX3-B3E&ved=0ahUKEwjW2tyY8OT0AhVxklYBHQgcCUgQ4dUDCAo&uact=5&oq=Wisconsin+is+on+pace+to+double+the+number+of+layoffs+this+year.&gs_lcp=Cgdnd3Mtd2l6EAMyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECdQiwFYiwFg2QJoAXAAeACAAQCIAQCSAQCYAQCgAQKgAQGwAQo&sclient=gws-wiz')
    gs.search_cite()