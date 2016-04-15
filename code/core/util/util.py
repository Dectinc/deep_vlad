# -*- coding: utf-8 -*-
# @filename util
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-03-27 22:17 PM

import os
from core.util import LoggerUtil
from core.util import config
from core.util.config import pjoin
from fast_rcnn.config import cfg
from os.path import exists, isdir

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])


def walk(func):
    """
    Walk recursively through a path and handler each file with func
    :param func: file operation function
    :return: wrapped function
    """

    def walk_wrapper(path_from, path_to, _ext=None):
        path_from = os.path.abspath(path_from)
        path_to = os.path.abspath(path_to)
        if path_from[-1] != os.sep:
            path_from += os.sep
        logger.info('Walk in {}'.format(path_from))
        logger.info('Results to {}'.format(path_to))
        _prefix = os.path.commonprefix([os.path.split(path_from),
                                        os.path.split(path_to)])
        len_prefix = len(os.path.sep.join(_prefix))
        logger.info('Common prefix: {}'.format(_prefix))
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
                try:
                    func(_from_file, _to_file)
                    logger.info('[{}] from {} to {}'.format(
                        func.func_name,
                        '${{FROM}}{}'.format(_from_file[len_prefix:]),
                        '${{TO}}{}'.format(_to_file[len_prefix:])
                    ))
                except Exception, e:
                    logger.info('Failed [{}] {}, error msg: {}'.format(
                        func.func_name, _from_file, str(e)
                    ))

    return walk_wrapper


def check_directory(_directory):
    """
    Check whether a directory exists, creating it if not
    :param _directory: directory path
    """
    if not exists(_directory) or not isdir(_directory):
        logger.info('Directory not exists, create it: {}'.format(_directory))
        os.makedirs(_directory)


def ensure_directory(*outer_args):
    """
    Decorator for ensuring directory exists
    :param outer_args: directory name
    :return: function wrapper
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


def get_model_path(model_set, model_name):
    """
    Get model path by model set and model name
    :param model_set: model collections under ${FASTER_RCNN_ROOT}/data
    :param model_name: model name without any suffix, i.e. vgg
    :return: model path and corresponding proto file path
    """
    model_root = pjoin(config.FASTER_RCNN_DIR, 'data')
    if model_set in ('fast', 'faster'):
        model_set += '_rcnn'
    model_set_dir = pjoin(model_root, '{}_models'.format(model_set))
    models = os.listdir(model_set_dir)
    for model in models:
        if model.lower().startswith(model_name.lower()):
            model_path = pjoin(model_set_dir, model)
            proto_path = pjoin(cfg.MODELS_DIR, model_name.upper(),
                               'faster_rcnn_alt_opt',
                               'faster_rcnn_test.pt')
            return model_path, proto_path
    return None, None
