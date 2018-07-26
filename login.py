#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import requests

import configloader

urp_index_url = "http://newjw.cduestc.cn"
urp_login_url = "http://newjw.cduestc.cn/loginAction.do"
urp_main_url = "http://newjw.cduestc.cn/menu/s_main.jsp"
urp_jxpg_list_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=listWj"
urp_jxpg_url = "http://newjw.cduestc.cn/jxpgXsAction.do"
urp_jxpg_page_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=wjpg"

class Student(object):
    def __init__(self, *args, **kwargs):
        self.requests = requests
        # 创建Requests session
        self.sess = requests.Session()
        if os.path.exists("config.ini"):
            user = configloader.load_user()
            self.account = user["account"]
            self.password = user["password"]
        else:
            self.account = input("请输入你的学号：").strip()
            self.password = input("请输入你的密码：").strip()
            configloader.init_user(self.account, self.password)

    def login(self):
        # 构造form表单内容
        data = {
            'zjh': self.account,
            'mm': self.password
        }
        # 构造headers，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Host': 'newjw.cduestc.cn',
            'Origin': 'http://newjw.cduestc.cn',
            'Referer': 'http://newjw.cduestc.cn/',
            'DNT': '1'
        }
        # 首先发送post请求登录urp系统
        self.sess.post(urp_login_url, data=data, headers=headers)
        return self.sess
