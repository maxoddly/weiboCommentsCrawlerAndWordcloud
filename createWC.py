# -*- coding: utf-8 -*-
# @Time    : 2019-08-01 16:02
# @Author  : Kazoo310
# @File    : createWC.py

import jieba
import imageio
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd

# 处理文本
text = pd.read_csv('comments.csv')
text_list = text.values.tolist()
stopword = ['xa0','ue627']  # 设置屏蔽词
comment = jieba.cut(str(text_list), cut_all=False)
words = ' '.join(comment)

# 图片
background = imageio.imread("hb.jpg")
wc = WordCloud(background_color='#FFFAF0',  # 背景颜色
               scale=8,
               max_words=1000,  # 最大词数
               mask=background,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=70,  # 显示字体的最大值
               stopwords=stopword,
               font_path='/System/Library/Fonts/Hiragino Sans GB.ttc', #需要添加字体，否则中文是乱码
               random_state=10,  # 为每个词返回一个PIL颜色
               )


wc.generate(words)
image_colors = ImageColorGenerator(background)  # 设置背景图片
plt.imshow(wc)  # 显示图片
plt.axis('off')  # 关闭坐标轴
# 绘制词云
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
# 保存图片
wc.to_file('CLWC.jpg')





