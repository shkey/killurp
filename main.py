#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import prettytable
import login
import judge
import score
import cet

def main():
    student = login.Student()
    student.login()
    pt = prettytable.PrettyTable(["操作类型"])
    # 设置prettytable靠左对齐
    pt.align = "l"
    pt.add_row(["1、成绩查询"])
    pt.add_row(["2、一键评教"])
    pt.add_row(["3、四六级查询"])
    print(pt)
    choice = int(input("请输入你要进行的操作类型：")) - 1
    if choice == 0:
        score.main(student)
    elif choice == 1:
        judge.judge_all(student)
    elif choice == 2:
        cet.main()
    else:
        print("你的输入有误，请重新运行本程序再次进行输入！")
        return 0

if __name__ == "__main__":
    main()