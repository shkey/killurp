#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import prettytable
import login
from bs4 import BeautifulSoup

def get_qbinfo(choice_html):
    # 将得到的教务系统的源码转换成BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(choice_html.text, "lxml")
    # 通过css选择器选出要用的数据
    score_tables = soup.select("#user > tr > td")
    pt_score = prettytable.PrettyTable(["课程号", "课程名", "学分", "课程属性", "成绩"])
    # 设置prettytable靠左对齐
    pt_score.align = "l"
    for i in range(0, len(score_tables), 7):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        pt_score.add_row([course_id, course_name, course_num, course_type, course_score])
    print(pt_score)

def get_sxinfo(choice_html):
    # 将得到的教务系统的源码转换成BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(choice_html.text, "lxml")
    # 通过css选择器选出要用的数据
    score_tables = soup.select("#user > tr > td")
    pt_score = prettytable.PrettyTable(["课程号", "课程名", "学分", "课程属性", "成绩"])
    # 设置prettytable靠左对齐
    pt_score.align = "l"
    for i in range(0, len(score_tables), 8):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        pt_score.add_row([course_id, course_name, course_num, course_type, course_score])
    print(pt_score)

def get_fainfo(choice_html):
    # 将得到的教务系统的源码转换成BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(choice_html.text, "lxml")
    # 通过css选择器选出要用的数据
    score_tables = soup.select("#user > tr > td")
    pt_score = prettytable.PrettyTable(["课程号", "课程名", "学分", "课程属性", "成绩"])
    # 设置prettytable靠左对齐
    pt_score.align = "l"
    for i in range(0, len(score_tables), 8):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        pt_score.add_row([course_id, course_name, course_num, course_type, course_score])
    print(pt_score)

def get_bjg(choice_html):
    # 将得到的教务系统的源码转换成BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(choice_html.text, "lxml")
    # 通过css选择器选出要用的数据
    score_tables = soup.select("#user > tr > td")
    pt_score = prettytable.PrettyTable(["课程号", "课程名", "学分", "课程属性", "成绩", "考试时间"])
    # 设置prettytable靠左对齐
    pt_score.align = "l"
    for i in range(0, len(score_tables), 9):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        course_time = score_tables[i + 7].get_text().strip()
        pt_score.add_row([course_id, course_name, course_num, course_type, course_score, course_time])
    print(pt_score)

def main(student):
    # 构造一个列表，用来存放查询成绩的类型
    score_urls = [
        "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=qbinfo", "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=sxinfo", "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=fainfo", "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=bjg"
    ]
    pt = prettytable.PrettyTable(["查询类型"])
    # 设置prettytable靠左对齐
    pt.align = "l"
    pt.add_row(["1、全部及格成绩查询"])
    pt.add_row(["2、按课程属性成绩查询"])
    pt.add_row(["3、按方案成绩查询"])
    pt.add_row(["4、不及格成绩查询"])
    print(pt)
    choice = int(input("请输入你要进行的查询类型：")) - 1
    if choice == 0:
        score_html = student.sess.get(score_urls[choice])
        get_qbinfo(score_html)
    elif choice == 1:
        score_html = student.sess.get(score_urls[choice])
        get_sxinfo(score_html)
    elif choice == 2:
        score_html = student.sess.get(score_urls[choice])
        get_fainfo(score_html)
    elif choice == 3:
        score_html = student.sess.get(score_urls[choice])
        get_bjg(score_html)
    else:
        print("你的输入有误，请重新运行本程序再次进行输入！")
        return 0

if __name__ == "__main__":
    student = login.Student()
    student.login()
    main(student)