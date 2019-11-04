# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 20:24:05 2018

@author: peter
"""

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