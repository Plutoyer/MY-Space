# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 20:30:20 2018

@author: peter
"""

import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect(r"qdaily.db")
url_id = conn.execute("select id from qdaily order by id;").fetchall()
sharenum = conn.execute("select sharenum from qdaily order by id;").fetchall()
plt.title("文章id与分享数关系图", fontproperties='SimHei', fontsize=25)
plt.xlabel("文章id", fontproperties='SimHei', fontsize=15)
plt.ylabel("分享数", fontproperties='SimHei', fontsize=15)
plt.plot(url_id, sharenum, '-r')
conn.close()
