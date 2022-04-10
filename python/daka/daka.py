from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.implicitly_wait(100)
driver.get("https://ehall.jlu.edu.cn/taskcenter/workflow/appall")
driver.find_element_by_id("username").send_keys("XXXXXX")#账号
driver.find_element_by_id("password").send_keys("XXXXXX")#密码
driver.find_element_by_id("login-submit").send_keys(Keys.ENTER)#登录
driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/div/ul[1]/li[2]/div[2]/p[1]/a").send_keys(Keys.ENTER)#点每日打卡
driver.find_element_by_xpath("//*[@id='V1_CTRL6']/option[2]").click()#中心校区
driver.find_element_by_xpath("//*[@id='V1_CTRL7']/option[5]").click()#南二
driver.find_element_by_xpath("//*[@id='V1_CTRL8']").send_keys("XXX")#房间号
driver.find_element_by_xpath("//*[@id='V1_CTRL28']").click()#正常体温
js = "document.getElementsByClassName('command_button_content')[0].click()"
driver.execute_script(js)#点提交
driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/button[1]").click()#点好
driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/button").click()#点关闭