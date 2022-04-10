import time
from selenium import webdriver


class GoogleScholarCommon:

    # 这里url是你要搜索的关键词，我这里关键词是deep cluster
    def __init__(self, wait_time=120, url="https://www.ncbi.nlm.nih.gov/pmc/?term=deep"):
        self.gs_url = url
        self.driver = webdriver.Chrome()
        self.wait_time = wait_time
        self.source = self.driver.page_source

    def iselementexist(self):
        flag = True
        browser = self.driver
        self.driver.implicitly_wait(3)

        # 这里这个PDF-4.2M是在搜索界面上pdf的下载链接
        browser.find_element_by_partial_link_text("Next >")
        return flag

    def search_cite(self):
        """搜索论文名，返回所有引用的论文名
        """

        self.driver.implicitly_wait(self.wait_time)
        self.driver.get(self.gs_url)
        source = self.driver.page_source
        print(source)
        time.sleep(3)
        # 这里在做模拟点击下载
        self.driver.find_element_by_partial_link_text("Next >").click()
        source = self.driver.page_source
        print(source)


if __name__ == "__main__":
    gs = GoogleScholarCommon()
    gs.search_cite()
