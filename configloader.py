#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import os


def init_user(account, password):
    config = configparser.ConfigParser()
    config.add_section("user")
    config.set("user", "account", account)
    config.set("user", "password", password)
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def load_user():
    config = configparser.ConfigParser()
    user = {}
    config.read("config.ini")
    user["account"] = config.get("user", "account")
    user["password"] = config.get("user", "password")
    return user

def set_urp_status(code):
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "status" not in config:
        config.add_section("status")
    config.set("status", "code", code)
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def get_urp_status():
    config = configparser.ConfigParser()
    config.read("config.ini")
    code = config.get("status", "code")
    return code

def main():
    test = int(input("请输入测试项：1为初始化，2为读取").strip())
    if test == 1:
        init_user("123","test")
    elif test == 2:
        load_user()

if __name__ == "__main__":
    main()
