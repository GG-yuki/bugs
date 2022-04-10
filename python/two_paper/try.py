import urllib.request
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
url = r'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7259704/pdf'
file_name = url.split('/')[-1]
print(file_name)
req = urllib.request.Request(url=url, headers=headers)
u = urllib.request.urlopen(url)
f = open(file_name, 'wb')
print(u)

block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    f.write(buffer)
f.close()
print("Sucessful to download" + " " + file_name)

# import requests
#
# url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7259704/pdf/pone.0233491.pdf'#创建需要爬取网页的地址
# #创建头部信息
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
# response = requests.get(url, headers=headers)#发送网络请求
# print(response.status_code)#打印响应状态码 如果等于200说明请求成功

# import urllib.request
# def get_page_source(url):
#     headers = {'Accept': '*/*',
#                'Accept-Language': 'en-US,en;q=0.8',
#                'Cache-Control': 'max-age=0',
#                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
#                'Connection': 'keep-alive',
#                'Referer': r'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7259704/pdf/pone.0233491.pdf'
#                }
#     req = urllib.request.Request(url, None, headers)
#     response = urllib.request.urlopen(req)
#     page_source = response.read()
#     return page_source
# get_page_source(r'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7259704/pdf/pone.0233491.pdf')
# print(get_page_source())