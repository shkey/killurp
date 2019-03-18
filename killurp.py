#!/usr/bin/env python3

import argparse
import random
import sys
from io import BytesIO

import prettytable
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from PIL import Image

__VERSION__ = '0.1.0'

PORT = '80'
PROTOCOL = 'http://'
URP_INDEX = 'newjw.cduestc.cn'
URP_LOGIN = '/loginAction.do'
URP_MAIN = '/menu/s_main.jsp'
URP_GRADE_QB = '/gradeLnAllAction.do?type=ln&oper=qbinfo'
URP_GRADE_SX = '/gradeLnAllAction.do?type=ln&oper=sxinfo'
URP_GRADE_FA = '/gradeLnAllAction.do?type=ln&oper=fainfo'
URP_GRADE_BJG = '/gradeLnAllAction.do?type=ln&oper=bjg'
URP_JXPG_LIST = '/jxpgXsAction.do?oper=listWj'
URP_JXPG = '/jxpgXsAction.do'
URP_JXPG_PAGE = '/jxpgXsAction.do?oper=wjpg'
WORDS = ['完全 ok', '不错', '可以', '很好', '还行']

PROTOCOL_WITH_SSL = 'https://'
CET_INDEX = 'www.chsi.com.cn/cet/'
VAL_IMG = 'ValidatorIMG.JPG'
CET_SCORE = 'query'


def get_parser():
    parser = argparse.ArgumentParser(
        description='一个小工具集，将会不断更新各项功能，目的是干掉难用落后反人类的科成 urp',
        epilog='有问题或者更好的建议？欢迎来 Github[https://github.com/shkey/killurp] 提 issue 和 PR'
    )
    parser.add_argument(
        'choice', type=str,
        help='''选择你要使用的功能项 ->
                grade：成绩导出，
                judge：一键评教，
                cet：四六级查询''',
        choices=['grade', 'judge', 'cet'])
    urp_group = parser.add_argument_group(title='URP options')
    cet_group = parser.add_argument_group(title='CET options')
    urp_group.add_argument(
        '-a', '--account', type=str,
        help='你的 URP 账号（也就是学号）'
    )
    urp_group.add_argument(
        '-p', '--password', type=str,
        help='你的 URP 账号的密码'
    )
    urp_group.add_argument(
        '-P', '--port', type=str,
        help='URP 教务系统开放端口（默认为 80 端口）'
    )
    cet_group.add_argument(
        '-z', '--zkzh', type=str,
        help='你的 CET 准考证号'
    )
    cet_group.add_argument(
        '-n', '--name', type=str,
        help='你的姓名'
    )
    parser.add_argument('-v', '--version',
                        action='version', version=__VERSION__)
    return parser


def fake_urp_sess(account, password, port=PORT):
    index_url = PROTOCOL + URP_INDEX
    if port:
        index_url = PROTOCOL + URP_INDEX + ':' + port
    login_url = index_url + URP_LOGIN
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Referer': index_url
    }
    data = {
        'zjh': account,
        'mm': password
    }
    sess = requests.Session()
    try:
        status = False
        response = sess.post(login_url, data=data, headers=headers)
        if '学分制综合教务' in response.text:
            status = True
        else:
            print('账号或密码有误，或者加上端口号再试试？')
    except Exception as e:
        print('Exception:', e)
        print('遇到了点小问题，请重试！')
    return sess, status


def get_qbinfo(score_html):
    soup = BeautifulSoup(score_html.text, 'lxml')
    score_tables = soup.select('#user > tr > td')
    score_list = []
    score_list.append(['课程号', '课程名', '学分', '课程属性', '成绩'])
    for i in range(0, len(score_tables), 7):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        score_list.append(
            [course_id, course_name, course_num, course_type, course_score])
    return score_list


def get_sxinfo(score_html):
    soup = BeautifulSoup(score_html.text, 'lxml')
    score_tables = soup.select('#user > tr > td')
    score_list = []
    score_list.append(['课程号', '课程名', '学分', '课程属性', '成绩'])
    for i in range(0, len(score_tables), 8):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        score_list.append(
            [course_id, course_name, course_num, course_type, course_score])
    return score_list


def get_fainfo(score_html):
    soup = BeautifulSoup(score_html.text, 'lxml')
    score_tables = soup.select('#user > tr > td')
    score_list = []
    score_list.append(['课程号', '课程名', '学分', '课程属性', '成绩'])
    for i in range(0, len(score_tables), 8):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        score_list.append(
            [course_id, course_name, course_num, course_type, course_score])
    return score_list


def get_bjg(score_html):
    soup = BeautifulSoup(score_html.text, 'lxml')
    score_tables = soup.select('#user > tr > td')
    score_list = []
    score_list.append(['课程号', '课程名', '学分', '课程属性', '成绩', '考试时间'])
    for i in range(0, len(score_tables), 9):
        course_id = score_tables[i].get_text().strip()
        course_name = score_tables[i + 2].get_text().strip()
        course_num = score_tables[i + 4].get_text().strip()
        course_type = score_tables[i + 5].get_text().strip()
        course_score = score_tables[i + 6].get_text().strip()
        course_time = score_tables[i + 7].get_text().strip()
        score_list.append([course_id, course_name, course_num,
                           course_type, course_score, course_time])
    return score_list


def save_to_xlsx(qb_score, sx_score, fa_score, bjg_score):
    try:
        wb = Workbook()
        ws1 = wb.active
        ws1.title = '全部成绩'
        ws2 = wb.create_sheet('课程属性成绩')
        ws3 = wb.create_sheet('方案成绩')
        ws4 = wb.create_sheet('不及格成绩')
        for row in qb_score:
            ws1.append(row)
        for row in sx_score:
            ws2.append(row)
        for row in fa_score:
            ws3.append(row)
        for row in bjg_score:
            ws4.append(row)
        wb.save('scores.xlsx')
        print('成绩报表导出完成，请注意查看')
    except Exception as e:
        print('Exception:', e)
        print('对不起，好像出了点小问题，要不再试一次？')


def export_grade(account, password, port=PORT):
    index_url = PROTOCOL + URP_INDEX
    if port:
        index_url = PROTOCOL + URP_INDEX + ':' + port
    sess, status = fake_urp_sess(account, password, port)
    if status:
        print('登录成功')
        try:
            print('成绩报表导出中...')
            qb_score_html = sess.get(index_url + URP_GRADE_QB)
            qb_score = get_qbinfo(qb_score_html)
            sx_score_html = sess.get(index_url + URP_GRADE_SX)
            sx_score = get_sxinfo(sx_score_html)
            fa_score_html = sess.get(index_url + URP_GRADE_FA)
            fa_score = get_fainfo(fa_score_html)
            bjg_score_html = sess.get(index_url + URP_GRADE_BJG)
            bjg_score = get_bjg(bjg_score_html)
            save_to_xlsx(qb_score, sx_score, fa_score, bjg_score)
        except Exception as e:
            print('Exception:', e)
            print('遇到了点小问题，请重试！')


def judge_all(account, password, port=PORT):
    index_url = PROTOCOL + URP_INDEX
    if port:
        index_url = PROTOCOL + URP_INDEX + ':' + port
    sess, status = fake_urp_sess(account, password, port)
    if status:
        print('登录成功')
        try:
            print('评教中，请稍等...')
            jxpg_jsp = sess.get(index_url + URP_JXPG_LIST)
            soup = BeautifulSoup(jxpg_jsp.text, 'lxml')
            course_info_list = soup.select('tr.odd > td > img')
            if len(course_info_list) == 0:
                print('未检测到需要评教的科目，是不是学号或者密码输错啦！')
            for c in course_info_list:
                c_info = c['name'].split('#@')
                querystring = {
                    'wjbm': c_info[0],
                    'bpr': c_info[1],
                    'pgnr': c_info[5],
                    'oper': 'wjShow',
                    'wjmc': c_info[3].encode('gb2312'),
                    'bprm': c_info[2].encode('gb2312'),
                    'pgnrm': c_info[4].encode('gb2312'),
                    'pageSize': '20',
                    'page': '1',
                    'currentPage': '1',
                    'pageNo': ''
                }
                jxpg_page = sess.post(
                    index_url + URP_JXPG_PAGE, data=querystring)
                querystring = {
                    'wjbm': c_info[0],
                    'bpr': c_info[1],
                    'pgnr': c_info[5],
                    '0000000054': '10_1',
                    '0000000055': '10_1',
                    '0000000056': '5_1',
                    '0000000057': '5_1',
                    '0000000058': '5_1',
                    '0000000059': '5_1',
                    '0000000060': '5_1',
                    '0000000061': '5_1',
                    '0000000062': '5_1',
                    '0000000063': '5_1',
                    '0000000064': '6_1',
                    '0000000065': '7_1',
                    '0000000066': '6_1',
                    '0000000067': '6_1',
                    '0000000068': '5_1',
                    '0000000069': '5_1',
                    '0000000070': '5_1',
                    'zgpj': WORDS[random.randint(0, len(WORDS) - 1)].encode('gb2312')
                }
                jxpg_submit = sess.post(
                    index_url + URP_JXPG, data=querystring)
                if jxpg_submit.status_code == requests.codes.get('ok'):
                    print(c_info[4], '评教完成')
            print('程序自动评教完成，请注意自行检查是否真的评教完成～')
        except Exception as e:
            print('Exception:', e)
            print('遇到了点小问题，请重试！')


def get_cet_score(zkzh, xm):
    cet_index_url = PROTOCOL_WITH_SSL + CET_INDEX
    try:
        sess = requests.Session()
        main_url = sess.get(cet_index_url)
        img = sess.get(cet_index_url + VAL_IMG)
        im = Image.open(BytesIO(img.content))
        im.show()
        yzm = input('请输入验证码：').strip()
        print('查询中，请稍等...')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Referer': cet_index_url
        }
        payload = {'zkzh': zkzh, 'xm': xm, 'yzm': yzm}
        score_html = sess.get(cet_index_url + CET_SCORE,
                              params=payload, headers=headers)
        soup = BeautifulSoup(score_html.text, 'lxml')
        pt_title = soup.select('#leftH > h2')
        pt_items = soup.select('#leftH > div > table > tr > td')
        pt = prettytable.PrettyTable([pt_title[0].get_text()])
        pt.align = 'l'
        pt.add_row(['姓名：{}'.format(pt_items[0].get_text().strip())])
        pt.add_row(['学校：{}'.format(pt_items[1].get_text().strip())])
        pt.add_row(['考试级别：{}'.format(pt_items[2].get_text().strip())])
        pt.add_row(['笔试准考证号：{}'.format(pt_items[3].get_text().strip())])
        pt.add_row(['笔试成绩总分：{}'.format(pt_items[4].get_text().strip())])
        pt.add_row(['听力：{}'.format(pt_items[6].get_text().strip())])
        pt.add_row(['阅读：{}'.format(pt_items[8].get_text().strip())])
        pt.add_row(['写作和翻译：{}'.format(pt_items[10].get_text().strip())])
        pt.add_row(['口试准考证号：{}'.format(pt_items[11].get_text().strip())])
        pt.add_row(['口试等级：{}'.format(pt_items[12].get_text().strip())])
        print(pt)
        if '请输入验证码' in score_html.text:
            print('请输入验证码！')
        if '验证码不正确' in score_html.text:
            print('验证码不正确，请重试！')
    except Exception as e:
        print('Exception:', e)
        print('sorry，出了点小问题，请重试！')


def cli():
    parser = get_parser()
    args = vars(parser.parse_args())
    choice = args.get('choice')
    account = args.get('account', None)
    password = args.get('password', None)
    port = args.get('port', PORT)
    zkzh = args.get('zkzh', None)
    name = args.get('name', None)
    if choice == 'grade':
        if not account:
            account = input('请输入你的账号：').strip()
        if not password:
            password = input('请输入你的密码：').strip()
        if account and password:
            export_grade(account, password, port)
        else:
            parser.print_help()
            print('ERROR：使用 URP 教务系统功能请同时输入账号及密码！')
            sys.exit()
    elif choice == 'judge':
        if not account:
            account = input('请输入你的账号：').strip()
        if not password:
            password = input('请输入你的密码：').strip()
        if account and password:
            judge_all(account, password, port)
        else:
            parser.print_help()
            print('ERROR：使用 URP 教务系统功能请同时输入账号及密码！')
            sys.exit()
    elif choice == 'cet':
        if not zkzh:
            zkzh = input('请输入 15 位笔试或口试准考证号：').strip()
        if not name:
            name = input('请输入你的姓名（姓名超过 3 个字，可只输入前 3 个）：').strip()
        if zkzh and name:
            get_cet_score(zkzh, name)
        else:
            parser.print_help()
            print('ERROR：使用 CET 功能请同时输入你的准考证号及姓名！')
            sys.exit()


if __name__ == '__main__':
    cli()
