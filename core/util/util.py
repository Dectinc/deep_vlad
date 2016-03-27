# -*- coding: utf-8 -*-
# @filename util
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-03-27 22:17 PM

import os
from os.path import exists, isdir

from core.util import LoggerUtil
from core.util.config import pjoin

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


def walk(func):
    def walk_wrapper(path_from, path_to, _ext=None):
        path_from = os.path.abspath(path_from)
        path_to = os.path.abspath(path_to)
        if path_from[-1] != os.sep:
            path_from += os.sep
        logger.info('Walk in {}'.format(path_from))
        logger.info('Results to {}'.format(path_to))
        for cur_dir, dir_list, file_list in os.walk(path_from):
            dir_name = cur_dir[len(path_from):]
            to_dir = pjoin(path_to, dir_name)
            check_directory(to_dir)
            logger.info('Found directory: {}'.format(cur_dir))
            for _file in file_list:
                _from_file = pjoin(cur_dir, _file)
                if not _ext:
                    _to_file = pjoin(to_dir, _file)
                else:
                    _filename, _origin_ext = os.path.splitext(_file)
                    _to_file = pjoin(to_dir, '{}.{}'.format(_filename, _ext))
                if os.path.exists(_to_file):
                    logger.info('skip for exists: {}'.format(_to_file))
                    continue
                func(_from_file, _to_file)

    return walk_wrapper


def check_directory(_directory):
    if not exists(_directory) or not isdir(_directory):
        logger.info('Directory not exists, create it: {}'.format(_directory))
        os.makedirs(_directory)


def ensure_directory(*outer_args):
    """
    decorator for ensure directory exist
    """

    def _ensure_directory(func):
        def do_func(*inner_args, **kwargs):
            _directory = outer_args[0] if outer_args else inner_args[1] if \
                inner_args[1:] else kwargs[0]
            check_directory(_directory)
            result = func(*inner_args, **kwargs)
            return result

        return do_func

    return _ensure_directory
