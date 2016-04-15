#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  extract_feature
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-04-11 17:27#! /usr/bin/env python
import os
import sys

from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list

execfile('_init_paths.py')

import argparse

from core.util import LoggerUtil
from core.util import util
import caffe
import numpy as np

logger = LoggerUtil.get_logger(__file__.split('/')[-1][:-3])

MODEL_SETS = {
    'fast_rcnn': 'fast_rcnn_models',
    'faster_rcnn': 'faster_rcnn_models',
    'fast': 'fast_rcnn_models',
    'faster': 'faster_rcnn_models',
    'imagenet': 'imagenet_models'
}
NET_NAMES = ['vgg16', 'zf', 'vgg_cnn_m_1024', 'caffenet']


def parse_args():
    parser = argparse.ArgumentParser(description='Feature Extraction with '
                                                 'Faster RCNN')
    parser.add_argument('--gpu', dest='gpu_id', default=0, type=int,
                        help='GPU device id to use [0]')
    parser.add_argument('--cpu', dest='cpu_mode', action='store_true',
                        help='Use CPU mode (overrides --gpu)')
    parser.add_argument('--net', dest='net_name',
                        choices=NET_NAMES, default='vgg16',
                        help='Network to use [vgg16]')
    parser.add_argument('--model-sets', dest='model_set',
                        choices=MODEL_SETS.keys(), default='faster_rcnn',
                        help='Model set name')
    parser.add_argument('--set', dest='set_cfgs', default=None,
                        nargs=argparse.REMAINDER, help='set config keys')
    parser.add_argument('--cfg', dest='cfg_file', default=None, type=str,
                        help='optional config file')
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the network',
                        default=None, type=str)
    args = parser.parse_args()
    return args


def extract_feature():
    pass


if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)
    if args.set_cfgs is not None:
        cfg_from_list(args.set_cfgs)

    model_path, proto_path = util.get_model_path(args.model_set,
                                                 args.net_name)
    if not model_path:
        logger.error('cannot locate model by set/name: {}/{}'.format(
            args.model_set, args.net_name
        ))
        sys.exit(-1)
    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(proto_path, model_path, caffe.Test)
    net.name = os.path.splitext(os.path.basename(model_path))[0]
    logger.info('Loaded network from: {}'.format(model_path))

    # warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)

    pass
