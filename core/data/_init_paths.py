# -*- coding: utf-8 -*-
# @filename _init_paths
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-03-28 13:15 PM

"""Set up paths for DeepVLAD data tools"""

import os.path as osp
import sys


def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


this_dir = osp.dirname(__file__)

root_dir = osp.abspath(osp.join(this_dir, '..', '..'))
add_path(root_dir)
