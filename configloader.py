#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import os


class Configloader(object):
    """docstring for Configloader."""
    def __init__(self):
        self.config = configparser.ConfigParser()

    def init_user(self, account, password):
        self.config.clear()
        self.config.add_section("user")
        self.config.set("user", "account", account)
        self.config.set("user", "password", password)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def load_user(self):
        self.config.read("config.ini")
        account = self.config.get("user", "account")
        password = self.config.get("user", "password")
        return account, password

    def set_urp_status(self, code):
        self.config.read("config.ini")
        if "status" not in self.config:
            self.config.add_section("status")
        self.config.set("status", "urp_code", code)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_urp_status(self):
        self.config.read("config.ini")
        code = self.config.get("status", "urp_code")
        return code
    
    def set_cet_status(self, code):
        self.config.read("config.ini")
        if "status" not in self.config:
            self.config.add_section("status")
        self.config.set("status", "cet_code", code)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_cet_status(self):
        self.config.read("config.ini")
        if "cet_code" not in self.config["status"]:
            return "0"
        code = self.config.get("status", "cet_code")
        return code

    def set_cet(self, zkzh, xm):
        self.config.read("config.ini")
        if "cet" not in self.config:
            self.config.add_section("cet")
        self.config.set("cet", "zkzh", zkzh)
        self.config.set("cet", "xm", xm)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_cet(self):
        self.config.read("config.ini")
        zkzh = self.config.get("cet", "zkzh")
        xm = self.config.get("cet", "xm")
        return zkzh, xm


def main():
    cl = Configloader()
    test = int(input("请输入测试项：1为初始化，2为读取").strip())
    if test == 1:
        cl.init_user("123","test")
    elif test == 2:
        print(cl.load_user())


if __name__ == "__main__":
    main()
