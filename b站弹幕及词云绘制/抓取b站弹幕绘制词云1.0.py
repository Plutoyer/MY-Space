from bs4 import BeautifulSoup#负责解析网页源码
import requests#负责爬取网页源码
import re#对解析后的文件进行弹幕匹配
import csv
import wordcloud

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
response = requests.get("https://api.bilibili.com/x/v1/dm/list.so?oid=130684654", headers=headers)
html_doc = response.content.decode('utf-8')
format = re.compile("<d.*?>(.*?)</d>")
DanMu = format.findall(html_doc)
#逐个输出弹幕
for i in DanMu:
  with open(r'C:\Users\金少\Desktop\b站弹幕.csv',"a", newline='',encoding='utf-8-sig') as csvfile:
    writer= csv.writer(csvfile)
    danmu = []
    danmu.append(i)
    writer.writerow(danmu)

# 从外部.txt文件中读取大段文本，存入变量txt中
f = open(r'C:\Users\金少\Desktop\b站弹幕.csv',encoding='utf-8')
txt = f.read()

# 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc')

# 将txt变量传入w的generate()方法，给词云输入文字
w.generate(txt)

# 将词云图片导出到当前文件夹
w.to_file('C:\\Users\金少\Desktop\output3.png')
