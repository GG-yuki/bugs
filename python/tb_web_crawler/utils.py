import re

with open("test.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        print(re.findall(r'https://www.google.com/search\?q=(.*)', line)[0])
        # a = r''
