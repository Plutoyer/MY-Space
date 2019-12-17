import requests

'''爬取全部'''
'''创建个函数输入先知的页数'''


def paqu_xianzhi(n):
    for k in range(1, n + 1):
        r = requests.get('https://xz.aliyun.com?page={}'.format(k))
        response = r.text
        # print(response)
        table1 = response.find('<table class="table topic-list">')
        # print(table1)
        table2 = response.find('</table>')
        # print(table2)
        contents = response[table1:table2]
        div = contents.split('<tr><td>')
        print('Page{}'.format(k))
        with open('b.txt', 'a', encoding='UTF-8') as file:
            file.write('Page{}'.format(k) + '\n')
        # print(div[i]) #1-30 30个标题
        for i in range(1, 31):
            # 继续分片 用<a分 分了五片 第0片没用 2：文章标题和连接
            # 3：作者 和连接 4：文章分类和发布时间和评论
            div2 = div[i].split('<a')
            j = 2
            print('-' * 50)
            # print(div2[4])

            # 取标题
            title1 = div2[j].find('">') + 2
            title2 = div2[j].find('</a>')
            title = div2[j][title1:title2].strip()
            print('标题:' + title)

            # 取标题连接
            title_link1 = div2[j].find('href="') + 6
            title_link2 = div2[j].find('">')
            title_link = div2[j][title_link1:title_link2]
            print('标题链接为：https://xz.aliyun.com' + title_link)
            j += 1

            # 作者
            author1 = div2[j].find('">') + 2
            author2 = div2[j].find('</a>')
            author = div2[j][author1:author2]
            print('作者为：' + author)

            # 作者链接
            author_link1 = div2[j].find('href="') + 6
            author_link2 = div2[j].find('">')
            author_link = div2[j][author_link1:author_link2]
            print('作者链接为：https://xz.aliyun.com' + div2[j][author_link1:author_link2])
            j += 1

            # 文章发布时间
            time1 = div2[j].find('/ 2') + 2
            time2 = time1 + 10
            time = div2[j][time1:time2]
            print('发布时间为：' + time)
            # 分类
            article_type1 = div2[j].find('">') + 2
            article_type2 = div2[j].find('</a>')
            article_type = div2[j][article_type1:article_type2]
            print('该文章属于:' + article_type)
            # 评论数量
            comment_number1 = div2[j].find('text-center ">') + 14
            comment_number2 = div2[j].find('</span></span>')
            comment_number = div2[j][comment_number1:comment_number2]
            print('该文章评论数为：' + comment_number)
            # 写入文件
            with open('b.txt', 'a', encoding='utf-8') as file:
                file.write('-' * 50 + '\n')
                file.write('标题:' + title + '\n')
                file.write('标题链接为：https://xz.aliyun.com' + title_link + '\n')
                file.write('作者为：' + author + '\n')
                file.write('作者链接为：https://xz.aliyun.com' + div2[j][author_link1:author_link2] + '\n')
                file.write('发布时间为：' + time + '\n')
                file.write('该文章属于:' + article_type + '\n')
                file.write('该文章评论数为：' + comment_number + '\n')

        print('-' * 50)


n = int(input('请输入要爬取的前几页：\n'))
paqu_xianzhi(n)
