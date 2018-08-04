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
    cl = configloader.Configloader()
    if os.path.exists("config.ini"):
        if cl.get_urp_status() == "1":
            account, password = cl.load_user()
        else:
            account = input("请输入你的学号：").strip()
            password = input("请输入你的密码：").strip()
            cl.init_user(account, password)
    else:
        account = input("请输入你的学号：").strip()
        password = input("请输入你的密码：").strip()
        cl.init_user(account, password)
    stu = student.Student(account, password)
    response_status = stu.login()
    if not response_status:
        cl.set_urp_status("0")
        return 0
    else:
        print("登录成功！")
        cl.set_urp_status("1")
        while(True):
            pt = prettytable.PrettyTable(["操作类型"])
            # 设置prettytable靠左对齐
            pt.align = "l"
            pt.add_row(["1、成绩查询"])
            pt.add_row(["2、一键评教"])
            pt.add_row(["3、四六级查询"])
            print(pt)
            choice = input("请按序号输入你要进行的操作，或者按其他任意键退出程序\r\n# ").strip()
            if choice.isdigit():
                choice = int(choice)
                if choice == 1:
                    score.main(stu)
                elif choice == 2:
                    judge.judge_all(stu)
                elif choice == 3:
                    cet.main(cl)
            else:
                print("你选择退出程序，好的，再见。")
                return 0


if __name__ == "__main__":
    main()
