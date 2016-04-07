#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  test_detect_region
# @author   dectincchen@sohu-inc.com
# @date     2016-03-28 01:01

import subprocess
import unittest

from core.util import LoggerUtil
from core.util import config

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


class TestDetectRegion(unittest.TestCase):
    def test_detect_region(self):
        __affine__, __thres__ = config.HESSIAN_AFFINE
        _from = config.pjoin(config.DATA_TEST, 'ppm')
        _to = config.pjoin(config.DATA_TEST)

        subprocess.call([config.AFFINE_DETECTOR,
                               '-{}'.format(__affine__),
                               '-i', _from,
                               '-o', _to,
                               '-thres', __thres__])


if __name__ == '__main__':
    unittest.main()
