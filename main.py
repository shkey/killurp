#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import prettytable

import cet
import judge
import student
import score
import yaml


def init_config():
    config_str = """
---
user: 
  # 学号
  account: ''
  # urp密码
  password: ''
cet: 
  # 准考账号
  zkzh: ''
  # 姓名
  xm: ''
status:
  # 状态码，0为登录失败，1为登录成功，2为登录成功但验证失败
  urp_code: 0
  cet_code: 0
...
"""
    with open("config.yml", "w", encoding= "utf-8") as cfg:
        cfg.write(config_str)

def save_config(cy):
    with open("config.yml", "w", encoding= "utf-8") as cfg:
        yaml.dump(cy, cfg, default_flow_style=False, allow_unicode=True, explicit_start=True, explicit_end=True)

def main():
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as cfg:
            cy = yaml.load(cfg)
            if cy["status"]["urp_code"]:
                account = cy["user"]["account"]
                password = cy["user"]["password"]
            else:
                account = input("请输入你的学号：")
                password = input("请输入你的密码：")
                cy["user"]["account"] = account
                cy["user"]["password"] = password
            stu = student.Student(account, password)
            response_status = stu.login()
            if not response_status:
                cy["status"]["urp_code"] = 0
                return 0
            else:
                print("登录成功！")
                cy["status"]["urp_code"] = 1
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
                            cet.main(cy)
                        else:
                            print("你选择退出程序，好的，再见。")
                            save_config(cy)
                            return 0
                    else:
                        print("你选择退出程序，好的，再见。")
                        save_config(cy)
                        return 0
    else:
        print("配置文件已丢失，正在重新生成···")
        init_config()
        print("配置文件重新生成成功，请重新运行本程序进行登录")


if __name__ == "__main__":
    main()
