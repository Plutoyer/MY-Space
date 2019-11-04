# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 20:18:46 2018

@author: peter
"""
import sqlite3
import requests
import time
import json
from bs4 import BeautifulSoup
    

url = "http://www.qdaily.com/articles/"
now_id = 1
end_id = 64016


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
        head = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'Host': 'www.qdaily.com',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Cookie': ('_qdaily4_web_session=all0TnRSaDhKSC9Md3JSOTl'
                       'ncFRXRmVQcjU3Q09JSDJ3RGxPRXVRS2FYeEI2T3R0SXVNMVBNZEt5WUh3bjV5bVRkRVg2RFZJT'
                       'TRwSW9ORkRVN3IvSWl3eGQxV09vSnBuREtrMFVDM0JnSWwva3o2b05tRnhZOEs4NWhlNVVFUGNrcV'
                       'NsVjdqOTdFMHBwcnNPVlpvREJ3PT0tLTBWRXl6QVpMdzFpRkVjcGdaZzhGckE9PQ%3D%3D--5f402d'
                       'd1706b6bd67a09d46bc84ccda438f16fcc'),
            'Referer': real_url,
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe'
                           'bKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'),
            'X-CSRF-Token': ('WnHSYPZiO6ICtOIYHx1J8UFVFvWBLcFp08RK5ouMqQdEHBw46PTLBJPdEtup0'
                             'alfS4tRTdS9fWSyfULZ8HOb6w=='),
            'X-Requested-With': 'XMLHttpRequest'
        }
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
        pass


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


if __name__ == '__main__':
    create()
    time0 = time.time()
    while now_id <= end_id:
        func(now_id)
        now_id += 1
        time1 = time.time()
        print("\r已爬取{0}个网页 ，总花费时间:{1:.2f}s".format(
            now_id-1, time1-time0), end="")
    conn.close()
