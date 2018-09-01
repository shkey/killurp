#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import BytesIO

import prettytable
import requests
import yaml
from bs4 import BeautifulSoup
from PIL import Image


def cet_login(sess, zkzh, xm):
    main_url = sess.get("https://www.chsi.com.cn/cet/")
    img = sess.get("https://www.chsi.com.cn/cet/ValidatorIMG.JPG")
    im = Image.open(BytesIO(img.content))
    im.show()
    yzm = input("请输入验证码：").strip()
    print("查询中，请稍等……\r")
    headers = {
        "Referer": "https://www.chsi.com.cn/cet/", 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    payload = {"zkzh": zkzh, "xm": xm, "yzm": yzm}
    score_html = sess.get("https://www.chsi.com.cn/cet/query", params=payload, headers=headers)
    try:
        soup = BeautifulSoup(score_html.text, 'lxml')
        pt_title = soup.select("#leftH > h2")
        pt_items = soup.select("#leftH > div > table > tr > td")
        pt = prettytable.PrettyTable([pt_title[0].get_text()])
        pt.align = "l"
        pt.add_row(["姓名：{}".format(pt_items[0].get_text().strip())])
        pt.add_row(["学校：{}".format(pt_items[1].get_text().strip())])
        pt.add_row(["考试级别：{}".format(pt_items[2].get_text().strip())])
        pt.add_row(["笔试准考证号：{}".format(pt_items[3].get_text().strip())])
        pt.add_row(["笔试成绩总分：{}".format(pt_items[4].get_text().strip())])
        pt.add_row(["听力：{}".format(pt_items[6].get_text().strip())])
        pt.add_row(["阅读：{}".format(pt_items[8].get_text().strip())])
        pt.add_row(["写作和翻译：{}".format(pt_items[10].get_text().strip())])
        pt.add_row(["口试准考证号：{}".format(pt_items[11].get_text().strip())])
        pt.add_row(["口试等级：{}".format(pt_items[12].get_text().strip())])
        print(pt)
        if "验证码不正确" in score_html.text:
            return False
        return True
    except:
        print("sorry，出了点小问题，请重试！")
        return 0

def main(cy):
    pre_code = cy["status"]["cet_code"]
    if pre_code:
        zkzh = cy["cet"]["zkzh"]
        xm = cy["cet"]["xm"]
    else:
        zkzh = input("请输入你的准考证号：")
        xm = input("请输入你的姓名：")
        cy["cet"]["zkzh"] = zkzh
        cy["cet"]["xm"] = xm
    sess = requests.Session()
    response_status = cet_login(sess, zkzh, xm)
    if not response_status:
        if pre_code:
            cy["status"]["cet_code"] = 2
            print("验证码输入有误，请重试！")
            return 0
        cy["status"]["cet_code"] = 0
        print("账号或密码有误，请重试！")
        return 0
    else:
        print("查询成功！")
        cy["status"]["cet_code"] = 1


if __name__ == "__main__":
    with open("config.yml", "r", encoding="utf-8") as cfg:
        cy = yaml.load(cfg)
        main(cy)
