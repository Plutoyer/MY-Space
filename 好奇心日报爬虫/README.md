# 用Python爬取好奇心日报
## 本项目最后更新于2019-5-24，可能会因为没有更新而失效。如已失效或需要修正，请提issue！
## 在写这个项目时，我还不会Python的协程编程，用协程可提升爬虫速度至少5倍，参考我的文章[线程，协程对比和Python爬虫实战说明](https://github.com/zhang0peter/python-coroutine)
## 声明
* 代码、教程且仅限于学习交流，请勿用于任何商业用途！   


## 前言

因为我是最近才关注好奇心日报的，感觉之前的许多好文章我都没看，所以打算找出这些好文章。  
一般来说一篇好文的分享数或者评论数比较多，所以我只要爬下
好奇心日报的每篇文章的评论数和分享数就行了。

## 准备工作

第一步是发现好奇心日报的文章地址编码是按数字递增的，例如：
http://www.qdaily.com/articles/38425.html  
截止今天，好奇心日报的文章编码已经从1到55613了，共5万篇文章。  
然后我发现文章的标题，分享数和文章发布日期都写死在页面里，但是评论数不在页面中   
为了找到评论数，我使用谷歌浏览器的F12的network功能，发现了评论是通过json数据获得的，地址类似：
http://www.qdaily.com/comments/article/38425/0.json     
看到json的数据自带评论，于是我顺便把评论的内容也爬下来了，顺便做一个评论的词云    

## 爬虫代码编写
先写建数据库的代码   
```python
def create():
     # 创建数据库
    global conn
    conn = sqlite3.connect('qdaily.db')
    conn.execute("""
                create table if not exists qdaily(
                id INTEGER PRIMARY KEY ,
                title varchar DEFAULT NULL,
                sharenum int DEFAULT NULL,
                date DATE DEFAULT NULL,
                comments int DEFAULT NULL)""")
    conn.execute("""
                create table if not exists comments(
                id INTEGER PRIMARY KEY ,
                url_id int DEFAULT NULL,
                comment varchar DEFAULT NULL)""")
```
然后写爬取的核心代码,在这段代码里，我使用了requests库来获取网页。         
```python
def func(id=0):
    if id == 0:
        print("id=0,error!")
        return
    real_url = url+str(id)+".html"
    try:
        r1 = requests.get(real_url, timeout=10)
        r1.encoding = r1.apparent_encoding
        demo = r1.text
        if "页面出错" in demo:
            return
        soup = BeautifulSoup(demo, "html.parser")
        sharenum = int(soup.find('span', 'num').string)
        title = soup.find('h2', 'title').string
        date = soup.find(
            'span', 'date smart-date').attrs['data-origindate'][:-15]
        comment_url = "http://www.qdaily.com/comments/article/" + \
            str(id)+"/0.json"
        r2 = requests.get(comment_url, headers=head, timeout=10).text
        jsDict = json.loads(r2)
        feeds = jsDict['data']['feeds']
        comments = jsDict['data']['total_count']
        tuple1 = (id, title, sharenum, date, comments)
        while jsDict['data']["has_more"]:
            more_comment = jsDict['data']['last_key']
            more_comment_url = "http://www.qdaily.com/comments/article/" + \
                str(id)+"/"+str(int(more_comment))+".json"
            r3 = requests.get(more_comment_url, headers=head, timeout=10).text
            jsDict = json.loads(r3)
            for i in jsDict['data']['feeds']:
                feeds.append(i)
        save(tuple1, feeds)
    except Exception as e:
        print()
        print(str(id)+"error!")
        print(e)
```
接着写一个保存数据到数据库的函数：
```python
def save(tuple1=None, list1=None):
    global conn
    if tuple1 == None:
        return
    command1 = "insert into qdaily \
             (id,title,sharenum,date,comments) values (?,?,?,?,?);"
    command2 = "insert into comments\
             (url_id,comment) values (?,?);"
    conn.execute(command1, tuple1)
    for i in list1:
        temp = (tuple1[0], i['content'])
        conn.execute(command2, temp)
        if i['child_comments'] != []:
            for j in i['child_comments']:
                temp = (tuple1[0], j['content'])
                conn.execute(command2, temp)
    conn.commit()
```
**完整的爬虫代码在 [qdaily-spider](https://github.com/zhang0peter/qdaily-spider/blob/master/qdaily-spider.py)**    

## 爬虫结果展示
我爬完5万篇文章用了快一天，虽然多线程可以加快速度，但我采用单线程减轻好奇心日报服务器的压力。  
先是根据文章分享数排序：     
![share.png](share.png)     

然后是根据文章的评论数排序：  
![comment](comment.png)  

## 好奇心日报文章id与评论数的关系
我感觉好奇心日报用的人越来越多了，那么随着id的增加，文章的平均评论数应该也会增加。  
代码如下：
```python
import matplotlib.pyplot as plt
import sqlite3
conn = sqlite3.connect(r"qdaily.db")
url_id = conn.execute("select id from qdaily order by id;").fetchall()
comment = conn.execute("select comments from qdaily order by id;").fetchall()
plt.title("id与评论数关系图", fontproperties='SimHei', fontsize=25)
plt.xlabel("id", fontproperties='SimHei', fontsize=15)
plt.ylabel("comment", fontproperties='SimHei', fontsize=15)
plt.plot(url_id, comment, '-r')
conn.close()
```
画出的图如下：  
![id-comment.png](id-comment.png)    
可以看出越到后面，平均每篇文章的分享数就越多，反映出好奇心日报的用户数变多  
**生成文章id与评论数关系图的完整代码在 [qdaily-id-comment](https://github.com/zhang0peter/qdaily-spider/blob/master/qdaily-comment.py)**    

## 根据评论生成词云
既然我把评论也爬了下来，那么我就写一个根据评论生成词云的代码  
```python
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
import sqlite3
conn = sqlite3.connect('qdaily.db')
wordlist = []
for i in conn.execute("select comment from comments").fetchall():
    wordlist.append(i[0])
wl_space_split = " ".join(wordlist)
mask_png = imread("mask.jpeg")
my_wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\simhei.ttf",
                         background_color="white",  # 背景颜色
                         max_words=500,  # 词云显示的最大词数
                         max_font_size=100,  # 字体最大值
                         random_state=42,
                         mask=mask_png,
                         width=1000, height=860, margin=2).generate(wl_space_split)
image_colors = ImageColorGenerator(mask_png)
plt.figure()
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.axis("off")
plt.show()
my_wordcloud.to_file("wordcloud.png")
```
生成的词云结果如下：  
![wordcloud.png](wordcloud.png)    
    

**生成词云代码在 [qdaily-comment](https://github.com/zhang0peter/qdaily-spider/blob/master/qdaily-comment.py)**    


