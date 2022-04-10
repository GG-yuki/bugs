import pdfplumber
import pandas as pd

with pdfplumber.open(r'1.pdf') as pdf:
    content = ''
    for i in range(len(pdf.pages)):
        # 读取PDF文档第i+1页
        page = pdf.pages[i]

        # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        page_content = '\n'.join(page.extract_text().split('\n')[:-1])
        content = content + page_content

# 提取以上解析结果中，“地方法规”和“2.其他有关资料”之间的内容
print(content)