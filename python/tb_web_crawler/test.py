#!/usr/bin/python
import re

with open("source.txt", "r",encoding='gbk',errors='ignore' ) as f:  # 打开文件
    data = f.read()  # 读取文件
    # print(data)
    # print(re.findall(
        # r'https://webcache.googleusercontent.com/search\?q=.*https://(.*?)\+\&amp', data))
lines = r'https://translate.google.com/translate?hl=zh-TW&amp;sl=en&amp;u=https://www.npr.org/2021/10/05/1043458068/biden-promised-to-halt-building-trumps-border-wall-but-new-construction-has-begu&amp;p'
# lines = r'https://webcache.googleusercontent.com/search?q=cache:Uq19Qw90IagJ:https://www.udemy.com/course/python-learn/+&amp;href=https://webcache.googleusercontent.com/search?q=cache:LdqRjL_2LJ0J:https://kopu.chat/2017/01/18/%25E4%25B8%2580%25E5%25B0%258F%25E6%2599%2582python%25E5%2585%25A5%25E9%2596%2580-part-1/+&amp;cd=11&amp;'
# print(re.findall(r'https://webcache.googleusercontent.com/search\?q=cache:.*?https://(.*?)\+\&amp', lines))
print(re.findall(r'https://translate.google.com/translate\?hl=zh-TW&amp;sl=en&amp;u=(.*?)\&amp',lines))
# lines = r'https://www.google.com/search?q=https://www.google.com/search?q=Building a wall on the U.S.-Mexico border will take literally years. '
# print(re.findall(r'https://www.google.com/search\?q=https://www.google.com/search\?q=(.*)', lines))

# ['djangogirlstaipei.herokuapp.com/tutorials/python/', 'www.inside.com.tw/article/23933-can-python-be-used-ten-more-years', 'www.coursera.org/learn/pbc1']
