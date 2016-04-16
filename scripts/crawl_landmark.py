#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  crawl_landmark
# @author   Dectinc(chenshijiang.thu@gmail.com)
# @date     2016-04-15 16:43

import argparse
import logging
import sys
from multiprocessing.pool import Pool, cpu_count

import os
import requests
from os.path import exists, isdir
from progressbar import Counter, Percentage, Bar, Timer, AdaptiveETA, \
    ProgressBar

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def get_landmark_dir(landmark_index):
    return os.path.join(args.data_dir,
                        '{:03d}'.format(landmark_index))


class Landmark():
    __LANDMARK_MAP = {}
    __alias_id_map = {}
    __count = 0

    def __init__(self, index, landmark_id, landmark_name):
        self.index = index
        self.alias = landmark_id
        self.landmark_name = landmark_name

    @classmethod
    def get_landmark_id(cls, landmark_id, landmark_name):
        if landmark_id not in cls.__alias_id_map:
            _landmark = Landmark(cls.__count, landmark_id, landmark_name)
            cls.__LANDMARK_MAP[cls.__count] = _landmark
            cls.__alias_id_map[landmark_id] = _landmark.__count
            check_directory(get_landmark_dir(_landmark.index))
            cls.__count += 1
        return cls.get_landmark_by_alias(landmark_id).index

    def __str__(self):
        return '{:03d}\t{}\t{}'.format(self.index, self.alias,
                                       self.landmark_name)

    @classmethod
    def save_all(cls, _file):
        if not _file:
            logging.error('No file specified')
            sys.exit(-1)
        landmarks = sorted(cls.__LANDMARK_MAP.values(), key=lambda x: x.index)
        with open(_file, 'wb') as f:
            for landmark in landmarks:
                f.write(str(landmark))
                f.write(os.linesep)
        logging.info('Landmarks saved to: {}'.format(_file))

    @classmethod
    def get_landmark(cls, landmark_index):
        return cls.__LANDMARK_MAP.get(landmark_index)

    @classmethod
    def get_landmark_by_alias(cls, landmark_alias):
        return cls.get_landmark(cls.__alias_id_map.get(landmark_alias))

    @classmethod
    def load_landmarks(cls, _file):
        with open(_file, 'rb') as f:
            lines = [_.strip() for _ in f.readlines()]
            for line in lines:
                _parts = line.split()
                landmark = Landmark(int(_parts[0]), _parts[1],
                                    ' '.join(_parts[2:]))
                cls.__LANDMARK_MAP[landmark.index] = landmark
                cls.__alias_id_map[landmark.alias] = landmark.index
        logging.info('Loaded {} landmarks from {}'.format(
            len(cls.__LANDMARK_MAP), _file))


class Image():
    def __init__(self, index_, url, landmark_id=None, landmark_name=None):
        self.index = index_
        self.url = url
        if not landmark_id and not landmark_name:
            self.landmark_id = None
            self.file = None
        else:
            self.landmark_id = Landmark.get_landmark_id(landmark_id,
                                                        landmark_name)
            self.file = self.get_image_path()

    @classmethod
    def parse_line(cls, _line):
        assert isinstance(_line, str)
        _parts = _line.split()  # index, landmark_id, url, file
        image = Image(int(_parts[0]), _parts[2])
        image.landmark_id = _parts[1]
        image.file = _parts[3] if len(_parts) > 3 else None
        return image

    @classmethod
    def set_root_dir(cls, data_dir):
        cls.DATA_ROOT = data_dir

    def get_image_path(self):
        if len(self.url) < 4:
            _suffix = '.jpg'
        else:
            _suffix = self.url[-4:]
            if _suffix not in ['.jpg', '.png']:
                _suffix = '.jpg'
        return os.path.join(self.DATA_ROOT,
                            '{:03d}'.format(self.landmark_id),
                            '{:06d}{}'.format(self.index, _suffix))

    def __str__(self):
        return 'index:{:06d}\nlandmark:{}\nurl:{}\nfile:{}'.format(
            self.index,
            Landmark.get_landmark(self.landmark_id),
            self.url,
            self.file
        )

    @staticmethod
    def save_image_list(image_list, _file):
        if not _file:
            logging.error('No file specified')
            sys.exit(-1)
        with open(_file, 'wb') as f:
            for image in image_list:
                f.write('{:06d}\t{:03d}\t{}\t{}'.format(image.index,
                                                        image.landmark_id,
                                                        image.url,
                                                        image.file))
                f.write(os.linesep)
        logging.info('Image info saved to {}'.format(_file))

    @staticmethod
    def load_image_list(_file):
        image_list = []
        with open(_file, 'rb') as f:
            for line in [_.strip() for _ in f.readlines()]:
                image_list.append(Image.parse_line(line))
        logging.info('Loaded {} images from {}'.format(len(image_list), _file))
        return image_list


def parse_args():
    parser = argparse.ArgumentParser(description='Crawl Landmark')
    parser.add_argument('-s', '--save-to', type=str,
                        dest='data_dir', default=None,
                        help='data dir to store images')
    parser.add_argument('-l', '--image-list', type=str,
                        dest='list_file', default=None,
                        help='image list file path')
    args = parser.parse_args()
    return args


def check_directory(_directory):
    """Check whether directory exists
    if not, create it
    :param _directory: path of directory to be checked
    """
    _directory = os.path.abspath(_directory)
    logging.info('Checking {}'.format(_directory))
    if not exists(_directory) or not isdir(_directory):
        os.makedirs(_directory)


def get_progress_bar(max_value):
    widgets = ['Processed: ', Counter(), '/{} ['.format(max_value),
               Percentage(), '] ', Bar(), ' ', Timer(), ' ', AdaptiveETA()]
    pbar = ProgressBar(widgets=widgets, maxval=max_value)
    pbar.start()
    return pbar


def load_image_list(_file):
    with open(_file, 'rb') as f:
        lines = [_.strip() for _ in f.readlines()]
        lines = [_ for _ in lines if _]
        num_images = len(lines)
        images = [None] * num_images
        logging.info('loading {} image infos'.format(num_images))
        pbar = get_progress_bar(num_images)
        count = 0
        for line in lines:
            _parts = line.strip().split()
            _parts = _parts[:2] + [' '.join(_parts[2:])]
            images[count] = Image(count, *_parts)
            count += 1
            pbar.update(count)
        pbar.finish()
        return images, num_images


def crawl_job(image):
    url, path = image.url, image.file
    check_directory(os.path.dirname(path))
    # NOTE the stream=True parameter
    try:
        r = requests.get(url, stream=True, timeout=10)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush() commented by recommendation from J.F.Sebastian
    except Exception, e:
        logging.warn('Failed downloading {}: {}'.format(url, e))
        image.file = None
    return image


def clean_image_list(image_list):
    to_handle = []
    for i, image in enumerate(image_list):
        if image.file is not None and not os.path.exists(image.file):
            to_handle.append(i)
    return [image_list[_] for _ in to_handle], len(to_handle)


def crawl():
    pool = Pool(cpu_count() - 2)
    image_list, num_images = load_image_list(args.list_file)
    print 'Loaded {} images'.format(num_images)
    cleaned_image_list, cleaned_num_images = clean_image_list(image_list)
    print '{} images to crawl'.format(cleaned_num_images)
    pbar = get_progress_bar(cleaned_num_images)

    for i, _ in enumerate(pool.imap(crawl_job, cleaned_image_list), 1):
        pbar.update(i)
    pbar.finish()
    Image.save_image_list(image_list, args.image_cache)
    Landmark.save_all(args.landmark_cache)
    logging.info('All done')


if __name__ == '__main__':
    args = parse_args()
    logging.info(args)
    if not args.list_file or not args.data_dir:
        print 'image-list and data-dir should be specified'
        sys.exit(-1)
    args.data_dir = os.path.abspath(args.data_dir)

    check_directory(args.data_dir)
    Image.set_root_dir(args.data_dir)

    args.image_cache = os.path.join(args.data_dir, '..', 'image.list')
    args.landmark_cache = os.path.join(args.data_dir, '..', 'landmark.list')

    crawl()
