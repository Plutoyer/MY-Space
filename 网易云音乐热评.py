import requests
import json
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
}


# 获得接口，解析评论接口
def parse_comments_json(comments_list, path):
    for hotComments in comments_list:
        print("==============================================")
        user_icon = hotComments.get('user').get('avatarUrl')
        print("user_icon: ", user_icon)

        userId = hotComments.get('user').get('userId')
        print("userId: ", userId)

        user_nickname = hotComments.get('user').get('nickname')
        print("user_nickname: ", user_nickname)

        comment_time = hotComments.get('time')
        print("comment_time: ", comment_time)
        comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(comment_time) / 1000))
        print(comment_time)

        zan_count = hotComments.get('likedCount')
        print("zan_count: ", zan_count)

        comment_content = hotComments.get('content')
        print("comment_content: ", comment_content)

        try:
            # 读写文件
            with open(path, 'a+', encoding='utf-8') as f:
                f.write(str(userId) + ";" + user_nickname + ";" + comment_content + ";" + str(
                    zan_count) + ";" + user_icon + "; " + comment_time + "\n")
                # f.write(comment_content + "\n")
                # # csv文件
                # with open('comment.csv', 'a+', encoding='gbk') as f:
                #     writer = csv.writer(f)
                #
                #     writer.writerow([userId, user_nickname, comment_content, zan_count, user_icon, comment_time])
        except Exception as e:
            pass
            # with open('load_error.txt', 'a+', encoding='utf-8') as f:
            #     f.write("==============="+str(e)+"\n")
            #     writer = csv.writer(f)
            #     writer.writerow([userId, user_nickname, comment_content, zan_count, user_icon, comment_time])


# 获取精彩评论
def get_wangyiyun_hotcomments(url, path):
    data = {
        "params": "fe0TVdyT+VuJ55uu+LgTsXlea7dROxXPYGv/FVSJMsm6Vh4nDodf59/qk0EnA/ZcFV7ZfzseLNQgnx7P/7Xnmg0mAO5kMVzNIoGwXr4ya8ZtkS0pU2b9/qwzszDgXp5LyJ8BxOJh6ZqcPFl8Vm7pF8ZpwiKlkPbRACtUnZmzdSEIK1vTXK2Lhlm4nDlw2K2tzNvYRiSesRApZZqBYJqBBvEMu4w/2dICbq8C10GkT1EZY4sX9irB/e7gOrzbYcAVm4pGDSuSWTdG+KoAg4+nCV0wAw2u4IBXw1J/c8tRXfsy0UhM/RrT/ABCHWrndb64mR/nsjResiTbTblHR9EwBh6knLSneQR/0PacjB7Zp6tLlbvhLCAENhTgMfmyRuu1qNb0unshrC/su5u48suwyRdwzCCZIQC/D1atjYpyUirEwBkyFqHN0OVeSsWZf5XjeXyIkJcXZUOu+/kGrYWrm6sLSqGqzJXgYeTYvoHaX0w=",
        "encSecKey": "13948d0b5288185467075eb5bbc36b66759c6cc8ee6cb4676016c47fb114d135fb4225c7072fab489e30ba63af1cc8f2852444d8989064958df436c498a18a7a3c43f290a053021ae0d8653b5f3f27dbb8b3a705ddaa7b9060124c86e065a493ceb4595fe5c6ea1e97ea301d4f6f774e5a5051747cda4d84af2180078fe8c8f5",
    }

    # postdata = requests
    resp = requests.post(url, data=data, headers=headers)
    # print(resp.text)
    comments_dict = json.loads(resp.text)
    hotComments_list = comments_dict.get('hotComments')
    print(hotComments_list)

    parse_comments_json(hotComments_list, path)


# 获取全部评论
def get_wangyiyu_comments(url, path):
    header = {
        'Accept': "*/*",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'Host': "music.163.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }

    # get_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_410714325'

    n = 1
    for i in range(0, 125290, 20):
        param = {
            'limit': str(i),
            'offset': str(n * 20 - 1)
        }
        n += 1
        response = requests.post(url, headers=header, params=param)
        # print(response.text)
        comments_dict = json.loads(response.text)
        comments_list = comments_dict.get('comments')
        print(comments_list)
        parse_comments_json(comments_list, path=path)


# 制作评论词云
def draw_wordcloud(path):
    from wordcloud import WordCloud, ImageColorGenerator
    from PIL import Image
    import matplotlib.pyplot as plt
    import numpy as np

    bg_mask = np.array(Image.open('bg1.jpg'))
    text = open(path, encoding='utf-8').read()
    my_wordcloud = WordCloud(background_color='white',  # 设置背景颜色
                             mask=bg_mask,  # 设置背景图片
                             max_words=2000,  # 设置最大显示的字数
                             font_path=r'C:\Windows\Fonts\STZHONGS.TTF',  # 设置中文字体，使的词云可以显示
                             max_font_size=250,  # 设置最大字体大小
                             random_state=30,  # 设置有多少种随机生成状态， 即有多少种配色方案
                             )
    myword = my_wordcloud.generate(text)

    plt.imshow(myword)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # url = "https://music.163.com/#/song?id=410714325"
    url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_410714325?csrf_token="
    # get_wangyiyun_hotcomments(url)

    path = '网易云热评.txt'

    start_time = time.time()
    comments_url = "http://music.163.com/api/v1/resource/comments/R_SO_4_444356086"

    get_wangyiyu_comments(comments_url, path)
    end_time = time.time()
    print("程序耗时%f秒." % (end_time - start_time))

    draw_wordcloud(path)
