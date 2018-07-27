#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import prettytable

import cet
import configloader
import judge
import student
import score


def main():
    if os.path.exists("config.ini"):
        if configloader.get_status() == "1":
            user = configloader.load_user()
            account = user["account"]
            password = user["password"]
        else:
            account = input("请输入你的学号：").strip()
            password = input("请输入你的密码：").strip()
            configloader.init_user(account, password)
    else:
        account = input("请输入你的学号：").strip()
        password = input("请输入你的密码：").strip()
        configloader.init_user(account, password)
    stu = student.Student(account, password)
    response_status = stu.login()
    if not response_status:
        configloader.set_status("0")
        print("账号或密码有误，请重试！")
        return 0
    else:
        configloader.set_status("1")
        pt = prettytable.PrettyTable(["操作类型"])
        # 设置prettytable靠左对齐
        pt.align = "l"
        pt.add_row(["1、成绩查询"])
        pt.add_row(["2、一键评教"])
        pt.add_row(["3、四六级查询"])
        print(pt)
        choice = int(input("请输入你要进行的操作类型：").strip())
        if choice == 1:
            score.main(stu)
        elif choice == 2:
            judge.judge_all(stu)
        elif choice == 3:
            cet.main()
        else:
            print("你的输入有误，请重新运行本程序再次进行输入！")
            return 0

if __name__ == "__main__":
    main()
