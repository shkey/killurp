#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random

import requests
from bs4 import BeautifulSoup

import student


urp_index_url = "http://newjw.cduestc.cn"
urp_login_url = "http://newjw.cduestc.cn/loginAction.do"
urp_main_url = "http://newjw.cduestc.cn/menu/s_main.jsp"
urp_jxpg_list_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=listWj"
urp_jxpg_url = "http://newjw.cduestc.cn/jxpgXsAction.do"
urp_jxpg_page_url = "http://newjw.cduestc.cn/jxpgXsAction.do?oper=wjpg"


def get_random_word():
    # 可以修改下面的列表内容为你想填写的主观评价
    words_list = ["完全ok", "不错", "可以", "很好", "还行"]
    return words_list[random.randint(0, 4)]


def judge_all(stu):
    try:
        print("程序运行中，请稍等……")
        main_jsp = stu.sess.get(urp_main_url, timeout=10)
        jxpg_jsp = stu.sess.get(urp_jxpg_list_url, timeout=10)
        soup = BeautifulSoup(jxpg_jsp.text, 'lxml')
        # 匹配出需要评教的列表
        course_info_list = soup.select('tr.odd > td > img')
        if len(course_info_list) == 0:
            print("未检测到需要评教的科目，是不是学号或者密码输错啦！")
        for c in course_info_list:
            # 通过#@切分字段
            c_info = c['name'].split('#@')
            # 构造请求表单
            querystring = {
                "wjbm":c_info[0],
                "bpr":c_info[1],
                "pgnr":c_info[5],
                "oper":"wjShow",
                "wjmc":c_info[3].encode('gb2312'),
                "bprm":c_info[2].encode('gb2312'),
                "pgnrm":c_info[4].encode('gb2312'),
                "pageSize":"20",
                "page":"1",
                "currentPage":"1",
                "pageNo":""
            }
            # 请求具体科目评教页面，目的是完全模拟浏览器行为
            jxpg_page = stu.sess.post(urp_jxpg_url, data=querystring, timeout=10)
            # 构造评教数据表单
            querystring = {
                "wjbm":c_info[0],
                "bpr":c_info[1],
                "pgnr":c_info[5],
                "0000000054":"5_1",
                "0000000055":"5_1",
                "0000000056":"5_1",
                "0000000057":"6_1",
                "0000000058":"6_1",
                "0000000059":"5_1",
                "0000000060":"4_1",
                "0000000061":"6_1",
                "0000000062":"7_1",
                "0000000063":"5_1",
                "0000000064":"8_1",
                "0000000065":"10_1",
                "0000000066":"8_1",
                "0000000067":"4_1",
                "0000000068":"6_1",
                "0000000069":"5_1",
                "0000000070":"5_1",
                "zgpj":get_random_word().encode('gb2312')
            }
            # 提交评教数据
            jxpg_submit = stu.sess.post(urp_jxpg_page_url, data=querystring, timeout=10)
            # 若科目评教成功则打印成功信息
            if jxpg_submit.status_code == requests.codes.get('ok'):
                print(c_info[4],"评教完成")
        print("程序自动评教完成，请注意自行检查是否真的评教完成～\r\n如果没有完成评教，请检查是否输错学号或密码后重试！")
    except:
        print("遇到了点小问题，请重试")


if __name__ == "__main__":
    stu = student.Student("123", "test")
    stu.login()
    judge_all(stu)
