# -*- coding: utf-8 -*-
# @filename test_util
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-03-27 22:35 PM

import shutil
import unittest

from core.util import LoggerUtil
from core.util import config
from core.util import util

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


class TestUtil(unittest.TestCase):
    def test_walk_wrapper(self):
        @util.walk
        def print_filename(_from, _to):
            shutil.copy(_from, _to)
            logger.info('Copy from {} to {}'.format(_from, _to))

        _from = config.get_path('test', 'core')
        _to = config.get_path('test', 'test')

        print_filename(_from, _to, 'txt')


if __name__ == '__main__':
    unittest.main()
