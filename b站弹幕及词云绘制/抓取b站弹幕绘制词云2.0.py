from bs4 import BeautifulSoup
import requests
import re
import csv
# 导入词云制作库wordcloud和中文分词库jieba
import jieba
import wordcloud
# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio

mk = imageio.imread("C:\\Users\金少\Desktop\Chinamap.gif")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

response = requests.get("https://api.bilibili.com/x/v1/dm/list.so?oid=130684654", headers=headers)
# print(response.text)
html_doc = response.content.decode('utf-8')
# soup = BeautifulSoup(html_doc,'lxml')
format = re.compile("<d.*?>(.*?)</d>")
DanMu = format.findall(html_doc)

for i in DanMu:
    with open(r'C:\Users\金少\Desktop\b站弹幕.csv', "a", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        danmu = []
        danmu.append(i)
        writer.writerow(danmu)

# 构建并配置词云对象w，注意要加stopwords集合参数，将不想展示在词云中的词放在stopwords集合里，这里去掉“曹操”和“孔明”两个词
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        scale=15,
                        stopwords={' '},
                        contour_width=5,
                        contour_color='red')

# 对来自外部文件的文本进行中文分词，得到string
f = open(r'C:\Users\金少\Desktop\b站弹幕.csv', encoding='utf-8')
txt = f.read()
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)

# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file(r'C:\Users\金少\Desktop\output2-threekingdoms.png')

