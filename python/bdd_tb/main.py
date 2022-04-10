from selenium import webdriver
import time
import datetime
# 打开Chrome浏览器
browser = webdriver.Chrome()

def login():
    # 打开淘宝首页，通过扫码登录
    browser.get("https://www.taobao.com")
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
        print(f"请尽快扫码登录")
        time.sleep(30)

def picking(method):
    # 打开购物车列表页面
    browser.get("https://cart.taobao.com/cart.htm")
    time.sleep(1)
    # 是否全选购物车
    if method == 0:
        while True:
            try:
                if browser.find_element_by_id("J_SelectAll1"):
                    browser.find_element_by_id("J_SelectAll1").click()
                    break
            except:
                print(f"找不到购买按钮")
    else:
        print(f"请手动勾选需要购买的商品")
        time.sleep(5)
    print('start')

def buy(times):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # print(now)
        # 对比时间，时间到的话就点击结算
        if now > times:
            # 点击结算按钮
            while True:
                try:
                    if browser.find_element_by_xpath('//*[@id="J_Go"]'):
                        time.sleep(0.1)
                        break
                except:
                    pass
            # 点击提交订单按钮//*[@id="submitOrderPC_1"]/div[1]/a[2]
            browser.find_element_by_xpath('//*[@id="J_Go"]').click()
            while True:
                try:
                    if browser.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div[1]/a[2]'):
                        # print('1')
                        browser.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div[1]/a[2]').click()
                        # print('2')
                        js = 'document.getElementByXpath("//*[@id="submitOrderPC_1"]/div[1]/a[2]").click();'
                        # print('3')
                        driver.execute_script(js)
                        # print('4')
                except:
                    print(f"再次尝试提交订单")
            time.sleep(0.01)

if __name__ == '__main__':
    login();
    picking(0);
    buy("2022-02-12 16:59:58.600000"); #修改为自己所需要的时间，注意时间格式一定要对
