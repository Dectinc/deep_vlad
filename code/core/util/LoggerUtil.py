#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  Logger
# @author   Dectinc Chen[chenshijiang.thu@gmail.com]
# @date     2016-03-04 17:41

import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

from config import pjoin, LOG_DIR, __TESTING__

__date_formatter = '%Y-%m-%d %H:%M:%S'
__log_formatter = '[%(asctime)s](%(levelname)7s) %(filename)s[%(lineno)d] - %(funcName)s : %(message)s'
__simple_formatter = '%(asctime)s - %(filename)s[%(lineno)3d] - %(levelname)s - %(message)s'

if __TESTING__:
    __all_log_file = pjoin(LOG_DIR, 'test_all.log')
    __error_log_file = pjoin(LOG_DIR, 'test_error.log')
else:
    __all_log_file = pjoin(LOG_DIR, 'all.log')
    __error_log_file = pjoin(LOG_DIR, 'error.log')


def get_logger(logger_name='General'):
    if logger_name not in Logger.manager.loggerDict:
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(logging.DEBUG)
        # handler all
        all_handler = TimedRotatingFileHandler(__all_log_file,
                                           when='midnight',
                                           backupCount=7)
        all_formatter = logging.Formatter(__log_formatter, __date_formatter)
        all_handler.setFormatter(all_formatter)
        all_handler.setLevel(logging.INFO)
        _logger.addHandler(all_handler)
        # handler error
        error_handler = TimedRotatingFileHandler(__error_log_file,
                                           when='midnight',
                                           backupCount=7)
        error_formatter = logging.Formatter(__log_formatter, __date_formatter)
        error_handler.setFormatter(error_formatter)
        error_handler.setLevel(logging.ERROR)
        _logger.addHandler(error_handler)

        if __TESTING__:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(__simple_formatter)
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.DEBUG)
            _logger.addHandler(console_handler)

    _logger = logging.getLogger(logger_name)
    return _logger


if __name__ == '__main__':
    logger = get_logger('data_service')
    logger.error('test - error')
    logger.info('test - info')
    logger.warn('test - warn')
