# -*- coding: utf-8 -*-
# @Time    : 2019-08-01 16:01
# @Author  : Kazoo310
# @File    : getHotComments.py

import json
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 配置
cookie = "Ugrow-G0=140ad66ad7317901fc818d7fd7743564; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; _s_tentry=-; Apache=1642712607695.0916.1563941099293; SINAGLOBAL=1642712607695.0916.1563941099293; ULV=1563941099331:1:1:1:1642712607695.0916.1563941099293:; WBtopGlobal_register_version=307744aa77dd5677; un=734554586@qq.com; login_sid_t=cae74c590895af093295e892849fd752; cross_origin_proto=SSL; SSOLoginState=1564497727; wvr=6; wb_timefeed_2100889127=1; UOR=,,login.sina.com.cn; wb_view_log_2100889127=1680*10502.200000047683716; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhML_DyE_Trmyd_744b2IU45JpX5KMhUgL.Fozpeh5R1h.peoM2dJLoIp-LxKnL1KzL1-qLxKnL1KzLB.z0eK5t; ALF=1596266158; SCF=AkywCLnpUe53ruyQ_VXCehN7XsV747GbrWDOw5thnK4ry5scdn7ZMu_8BI-6wIAQ17RVooazBtS8ZzSocf1dSgk.; SUB=_2A25wR5NiDeRhGeRP61IZ-CfNyTuIHXVTNIOqrDV8PUNbmtANLVXkkW9NUFrlkUV8XIVDnD4HWspEQdRMKHYPyh9x; SUHB=0JvRcMw0Yaw4QJ; webim_unReadCount=%7B%22time%22%3A1564730182339%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; YF-Page-G0=bd9e74eeae022c6566619f45b931d426|1564730187|1564730157"

Headers = {"Cookie": cookie}
rawUrl = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4348090448295557&filter=hot&from=singleWeiBo"  # 无page参数的url

# 开始获取评论
page = 100  # 设置需要爬取的页数
start = time.time()
list = []

for i in range(page):
    print("当前page:", i + 1, "/", page)
    rawComments = []  # 用来存放一级评论

    # 开始获取评论
    url = rawUrl + "&page="+str(int(i+1)) # 翻页
    req = requests.get(url,headers=Headers).text 
    html = json.loads(req)['data']['html']
    content = BeautifulSoup(html, "html.parser")
    list_con_list = content.find_all('div', attrs={'class': 'list_con'})  # list_con
    for index, list_con in enumerate(list_con_list):
        WB_text = list_con.find('div', attrs={'class': 'WB_text'})  # WB_text
        if index == 0:
            list.append(WB_text)
        if len(list) == 1:
            pass
        else:
            if list[0] == list[1]:
                print("页面元素重复，停止爬虫")
                exit()
            else:
                list.remove(list[0])
        comment_text = WB_text.text.split("：")[1]  # 去除冒号
        comment_text = comment_text.split("¡")[0]  # 去除图片
        str(comment_text).replace("", " ")  # 去除超话
        comment_text = comment_text.strip()
        if len(comment_text) == 0:  # 去掉空字符串
            pass
        else:
            rawComments.append(comment_text)
    comment_pd = pd.DataFrame(rawComments,columns=['comments'])
    comment_pd.to_csv('comments.csv', mode='a', encoding='utf-8', index=False, header=0) # 追加进csv

    time.sleep(4)
    end = time.time()

    print("运行时间：", str(round(end-start, 2)), "s")


