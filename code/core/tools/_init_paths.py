#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  _init_paths
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-04-11 17:10

# reset default encoding
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sys.dont_write_bytecode = True
except:
    pass

# add code directory to PYTHON_PATH
from os import path as osp

def add_path(_path):
    if _path not in sys.path:
        sys.path.insert(0, _path)
        print 'insert path:', _path

this_dir = osp.dirname(__file__)
try:
    path_root = osp.abspath(osp.join(this_dir, '..', '..', '..'))
    add_path(path_root)
except:
    sys.stderr('Failed setting path, will exit')
    sys.exit(-1)

# add faster-rcnn directory to PYTHON_PATH
# Add caffe to PYTHONPATH

faster_rcnn_root = osp.join(path_root, '..', 'py-faster-rcnn')
faster_rcnn_root = osp.abspath(faster_rcnn_root)
caffe_path = osp.join(faster_rcnn_root, 'caffe-fast-rcnn', 'python')
add_path(caffe_path)

# Add lib to PYTHONPATH
lib_path = osp.join(faster_rcnn_root, 'lib')
add_path(lib_path)