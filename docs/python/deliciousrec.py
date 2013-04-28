# -*- coding: utf-8 -*-
from pydelicious import get_popular, get_userposts, get_urlposts
import time


def initializeUserDict(tag, count=30):  # 引数に tag と count をとる、count の指定がなければ 5
    user_dict = {}
    # popular な投稿を 0 から count 番目まで取得
    for p1 in get_popular(tag=tag)[0:count]:
        # このリンクを投稿したすべてのユーザを取得
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict


def fillItems(user_dict):
    all_items = {}

    # すべてのユーザによって投稿されたリンクを取得
    for user in user_dict:
        for i in range(3):  # 3回試行する
            try:
                posts = get_userposts(user)
                break  # 取得できたらループから脱出
            except:
                print "Failed user "+user+", retrying"
                time.sleep(4)  # 4秒待って再試行
        for post in posts:
            url = post['href']
            user_dict[user][url] = 1.0
            all_items[url] = 1

    # 空のアイテムを 0 で埋める
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0
