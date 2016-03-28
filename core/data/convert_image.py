# -*- coding: utf-8 -*-
# @filename convert_image
# @author   Dectinc Chen
# @author   chenshijiang.thu@gmail.com
# @date     2016-03-27 22:02 PM


import _init_paths
import subprocess
import sys

from core.util import LoggerUtil
from core.util import util
from core.util.config import pjoin, DATASETS, DATA_ROOT, DATA_PPM_ROOT

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


@util.walk
def convert_image(_from, _to):
    subprocess.check_call(['convert', _from, _to])


def run_default():
    for _dataset in DATASETS:
        _from = pjoin(DATA_ROOT, _dataset)
        _to = pjoin(DATA_PPM_ROOT, _dataset)
        convert_image(_from, _to, 'ppm')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        convert_image(pjoin(DATA_ROOT, 'test'),
                      pjoin(DATA_PPM_ROOT, 'test'),
                      'ppm')
    else:
        run_default()
