#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


urp_index_url = "http://newjw.cduestc.cn"
urp_login_url = "http://newjw.cduestc.cn/loginAction.do"
urp_main_url = "http://newjw.cduestc.cn/menu/s_main.jsp"
urp_jxpg_list_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=listWj"
urp_jxpg_url = "http://newjw.cduestc.cn/jxpgXsAction.do"
urp_jxpg_page_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=wjpg"


class Student(object):
    def __init__(self, account, password):
        self.requests = requests
        # 创建Requests session
        self.sess = requests.Session()
        self.account = account
        self.password = password

    def login(self):
        print("登录中，请稍等……\r")
        # 构造form表单内容
        data = {
            "zjh": self.account,
            "mm": self.password
        }
        # 构造headers，模拟浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Host": "newjw.cduestc.cn",
            "Origin": "http://newjw.cduestc.cn",
            "Referer": "http://newjw.cduestc.cn/",
            "DNT": "1"
        }
        try:
            # 首先发送post请求登录urp系统
            response = self.sess.post(urp_login_url, data=data, headers=headers, timeout=10)
            if "您的密码不正确，请您重新输入！" in response.text or "你输入的证件号不存在，请您重新输入！" in response.text:
                print("账号或密码有误，请重试！")
                return False
            return True
        except:
            print("遇到了点小问题，请重试！")