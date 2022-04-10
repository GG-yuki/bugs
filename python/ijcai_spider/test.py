import re
with open("test_links.txt", "r") as f:  # 打开文件读取信息
    for line in f.readlines():
        # line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        print(re.findall(r'https://www.google.com/search\?q=(.*)', line)[0])