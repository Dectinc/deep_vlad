#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  config
# @author   Dectinc Chen[chenshijiang.thu@gmail.com]
# @date     2016-03-04 15:42

import os.path as osp
from os.path import join as pjoin

__TESTING__ = True

ROOT_DIR = pjoin(osp.dirname(__file__), '..', '..')

LOG_DIR = pjoin(ROOT_DIR, 'log')
RESULT_DIR = pjoin(ROOT_DIR, 'result')
DATA_DIR = pjoin(ROOT_DIR, 'data')
CONFIG_DIR = pjoin(ROOT_DIR, 'config')
SOURCE_DIR = pjoin(ROOT_DIR, 'core')
TEST_DIR = pjoin(ROOT_DIR, 'test')

DATA_TEST = pjoin(DATA_DIR, 'test')


def print_path(dir_name):
    print osp.abspath(dir_name)


def get_path(*paths):
    return pjoin(DATA_DIR, *paths)
