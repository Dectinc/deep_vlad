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

DATA_ROOT = '/home/shijiang/data/datasets/'
DATA_PPM_ROOT = pjoin(DATA_ROOT, 'all_ppm')
DATA_HESSIAN_ROOT = pjoin(DATA_ROOT, 'all_heaff')
DATASET_HOLIDAY = 'holidays'
DATASET_OXFORD = 'oxford'
DATASET_UKB = 'ukb'
DATASET_PARIS = 'paris'
DATASETS = [DATASET_HOLIDAY, DATASET_OXFORD, DATASET_UKB, DATASET_PARIS]




def print_path(dir_name):
    print osp.abspath(dir_name)


def get_path(*paths):
    return pjoin(DATA_DIR, *paths)
