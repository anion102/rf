#!/usr/bin/env python
# coding=utf-8
# python version:2.7.10
# system:windows xp
import os,sys

def relpath_to_abspath(path):
    '''
    将相对路径转换成绝对路径
    return 绝对路径
    '''
    abspath = os.path.abspath(path)
    return abspath


#test
