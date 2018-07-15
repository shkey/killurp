#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import prettytable
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def main():
    zkzh = input("请输入15位笔试或口试准考证号：").strip()
    xm = input("请输入你的姓名：").strip()
    sess = requests.Session()
    main_url = sess.get("https://www.chsi.com.cn/cet/")
    img = sess.get("https://www.chsi.com.cn/cet/ValidatorIMG.JPG")
    im = Image.open(BytesIO(img.content))
    im.show()
    yzm = input("请输入验证码：").strip()
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
    except:
        print("sorry，出了点小问题，请重试！")

if __name__ == "__main__":
    main()