#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：7/15/2020  1:38 PM 
# 文件名称   ：NedStark.py
import os
import sys
import platform


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)


from core import HouseStark


if __name__ == '__main__':
    HouseStark.ArgvHandle(sys.argv)
