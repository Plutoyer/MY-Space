##爬取网络：慕课网（"https://www.imooc.com/"）

from bs4 import BeautifulSoup
import urllib.request
import xlwt
import time

time_star = time.time()
ur = ["mobile", "python", "java", "php"]  ##通过查看网页源代码，手动构造访问链接
url_basic, mingc, lianj, url, hda, x = [], [], [], [], [], 1

for j in range(len(ur)):
    url_basic.append("http://www.imooc.com/course/list?c=" + ur[j] + "&page=")
    for i in range(7):  ##网页个数最多为7
        urll = url_basic[j] + str(i)
        url.append(urll)

heads = {
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
     q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

for key, value in heads.items():
    items = (key, value)
    hda.append(items)

opn = urllib.request.build_opener()
opn.addheaders = hda
urllib.request.install_opener(opn)

for i in url:
    try:  ##当网页不存在时，跳过本次循环，以便程序继续执行
        data = opn.open(i).read()
        soup = BeautifulSoup(data, 'lxml')
        coursenames = soup.find_all('h3', class_="course-card-name")
        links = soup.find_all('a', class_="course-card")
    except:
        continue
    for cour in coursenames:
        coursenames = cour.get_text()
        mingc.append(coursenames)
        x += 1
    for link in links:
        links = 'https://www.imooc.com' + str(link['href'])
        lianj.append(links)

header = ["序号", "课程名称", "课程链接"]
with open(r"C:\\Users\金少\Desktop\test\muke.csv", "w", encoding='utf-8') as file:
    file = xlwt.Workbook(encoding='utf-8')
    sheet = file.add_sheet('hello')
    sheet.write(0, 0, header[0])  ##此处尚需优化：学习用一行代码插入三列的标题（表头）
    sheet.write(0, 1, header[1])
    sheet.write(0, 2, header[2])
    for i in range(x - 1):
        sheet.write(i + 1, 0, i + 1)
        sheet.write(i + 1, 1, mingc[i])
        sheet.write(i + 1, 2, lianj[i])
        file.save(r"C:\\Users\金少\Desktop\test\muke.csv")

time_spend = time.time() - time_star
print(time_spend)  ##运行结果为32秒，代码执行速度太慢，还需要进一步优化

