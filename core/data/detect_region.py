#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  detect_hessian_region
# @author   dectincchen@sohu-inc.com
# @date     2016-03-28 00:41


import subprocess
import sys


from core.util import LoggerUtil
from core.util import util
from core.util import config
from core.util.config import AFFINE_DETECTOR, pjoin

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


@util.walk
def detect_region(_from, _to):
    """
    >> ./h_affine.ln -haraff -i img1.ppm -o img1.haraff -thres 1000
    >> ./h_affine.ln -hesaff -i img1.ppm -o img1.hesaff -thres 500
    """
    subprocess.check_call([AFFINE_DETECTOR, '-{}'.format(__affine__),
                           '-i', _from,
                           '-o', _to,
                           '-thres', __thres__])
    logger.info('Detect region {} to {}'.format(_from, _to))


def run_default():
    for _dataset in config.DATASETS:
        _from = pjoin(config.DATA_PPM_ROOT, _dataset)
        _to = pjoin(config.DATA_REGION_ROOT, _dataset)
        detect_region(_from, _to, __suffix__)


if __name__ == '__main__':
    __affine__, __thres__ = config.HESSIAN_AFFINE
    __suffix__  = __affine__
    if len(sys.argv) > 1:
        detect_region(pjoin(config.DATA_PPM_ROOT, 'test'),
                      pjoin(config.DATA_REGION_ROOT, 'test'),
                      __suffix__)
    else:
        run_default()
