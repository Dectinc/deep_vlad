# -*- coding: utf-8 -*-
# @filename oxford_map
# @author   Dectinc
# @date     2015-05-21 14:27 PM

'''
This file is for calculating the map of Oxford retrieval results, reference to evaluate_holiday of INRIA 2008.

Copyright MIG 2015. License: GPL
'''
import sys


def usage():
    print >> sys.stderr, """usage: python oxford_map.py result_file.dat

Where result_file.dat is a textfile. Its format is:

result_file = ( result_line newline )*

# each line is a query image with associated results
result_line = query_image_name query_result*

# a query result is a pair: the result's filename is prefixed with its rank (0 based)
query_result = rank result_image_name

Where:
- all items are separated by whitespaces (space or tab)
- image names are like all_souls_000007 (case sensitive and no suffix)
- the order of queries is not relevant
- if the query image is ranked, it is ignored in the scoring

Copyright MIG 2015. License: GPL
"""
    sys.exit(1)


dataset = 'oxford'
# dataset = 'paris'


def load_image_names():
    print 'using dataset: ', dataset
    image_names = []
    f = open(dataset + '_names.txt', 'r')
    try:
        for line in f:
            image_name = line.strip()
            image_names.append(image_name)
    finally:
        f.close()

    return image_names


def parse_ground_truth():
    gt_pos = {}
    gt_junk = {}
    import os
    import re

    if dataset == 'oxford':
        _gt_dir = 'gt_files_170407'
    elif dataset == 'paris':
        _gt_dir = 'gt_paris'
    else:
        return

    query_files = [f for f in os.listdir(_gt_dir) if re.match(r'[a-z_]+\d+_query.txt', f)]
    query_list_file = open('gt_'+dataset + '_query.txt', 'w')
    for query_file_path in query_files:
        query_id = query_file_path[:-len('query.txt')]

        query_file = open(os.path.join(_gt_dir, query_file_path), 'r')
        try:
            _line = query_file.readline()
            query_name = _line.split()[0]
            if query_name.startswith('oxc1_'):
                query_name = query_name[len('oxc1_'):]
        finally:
            query_file.close()

        query_result_pos = set()
        good_file = open(os.path.join(_gt_dir, query_id + 'good.txt'), 'r')
        try:
            for _line in good_file:
                query_result_pos.add(_line.strip())
        finally:
            good_file.close()
        ok_file = open(os.path.join(_gt_dir, query_id + 'ok.txt'), 'r')
        try:
            for _line in ok_file:
                query_result_pos.add(_line.strip())
        finally:
            good_file.close()

        query_result_junk = set()
        junk_file = open(os.path.join(_gt_dir, query_id + 'junk.txt'), 'r')
        try:
            for _line in junk_file:
                query_result_junk.add(_line.strip())
        finally:
            junk_file.close()

        gt_pos[query_name] = query_result_pos
        gt_junk[query_name] = query_result_junk
        query_list_file.write(query_name + '\n')

    query_list_file.close()
    save_ground_truth(gt_pos, gt_junk)
    return gt_pos, gt_junk


def load_ground_truth():
    _dataset = dataset
    # return parse_ground_truth(_gt_dir)
    import os

    if not os.path.exists('gt_' + _dataset + '_pos.txt') or not os.path.exists(
                            'gt_' + _dataset + '_junk.txt'):
        return parse_ground_truth()

    gt_pos = {}
    gt_junk = {}

    pos_file = open('gt_' + _dataset + '_pos.txt', 'r')
    try:
        for _line in pos_file:
            fields = _line.split()
            gt_pos[fields[0]] = set(fields[2::2])
    finally:
        pos_file.close()

    junk_file = open('gt_' + _dataset + '_junk.txt', 'r')
    try:
        for _line in junk_file:
            fields = _line.split()
            gt_junk[fields[0]] = set(fields[2::2])
    finally:
        junk_file.close()
    return gt_pos, gt_junk


def save_ground_truth(_gt_pos, _gt_junk, _gt_path_prefix='gt_' + dataset + '_'):
    _gt_file_pos = open(_gt_path_prefix + 'pos.txt', 'w')
    try:
        for _query in _gt_pos:
            _gt_file_pos.write(_query)
            _results = _gt_pos[_query]
            index = 0
            for _result in _results:
                _gt_file_pos.write(' ')
                _gt_file_pos.write(str(index))
                _gt_file_pos.write(' ')
                _gt_file_pos.write(_result)
                index += 1
            _gt_file_pos.write('\n')
    finally:
        _gt_file_pos.close()

    _gt_file_junk = open(_gt_path_prefix + 'junk.txt', 'w')
    try:
        for _query in _gt_junk:
            _gt_file_junk.write(_query)
            _results = _gt_junk[_query]
            index = 0
            for _result in _results:
                _gt_file_junk.write(' ')
                _gt_file_junk.write(str(index))
                _gt_file_junk.write(' ')
                _gt_file_junk.write(_result)
                index += 1
            _gt_file_junk.write('\n')
    finally:
        _gt_file_junk.close()


def load_results(_result_filename):
    ''' go through the result file and return in suitable structures
    '''
    result_file = open(_result_filename, 'r')
    try:
        for line in result_file:
            fields = line.split()
            query_name = fields[0]
            ranks = [int(rank) for rank in fields[1::2]]
            yield (query_name, zip(ranks, fields[2::2]))
    finally:
        result_file.close()


def evaluate_single_query(_query_name, _results, _gt_pos, _gt_amb):
    old_precision, old_recall = 1.0, 0.0
    ap = 0.0

    intersect_size = 0
    num_parsed = 0
    num_pos_results = float(len(_gt_pos))

    for i in xrange(len(_results)):
        _cur_name = _results[i][1]
        if _cur_name in _gt_amb:
            continue
        if _cur_name in _gt_pos:
            intersect_size += 1
        recall = intersect_size / num_pos_results
        precision = intersect_size / float(num_parsed + 1.0)

        ap += (recall - old_recall) * ((old_precision + precision) / 2.0)

        old_recall, old_precision = recall, precision
        num_parsed += 1

    return ap


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    if len(sys.argv) == 3:
        dataset = sys.argv[2]

    # image_names = load_image_names()
    # gt_pos, gt_junk = parse_ground_truth()
    gt_pos, gt_junk = load_ground_truth()

    result_file_name = sys.argv[1]
    sum_ap, num_query = 0.0, 0
    for _query_name, _query_results in load_results(result_file_name):
        if _query_name not in gt_pos:
            print 'unknown query ', _query_name
            sys.exit(1)

        _query_results.sort()
        _result_pos = gt_pos.pop(_query_name)
        _result_junk = gt_junk.pop(_query_name)
        _cur_ap = evaluate_single_query(_query_name, _query_results, _result_pos, _result_junk)
        print _query_name, ': ', str(_cur_ap)

        num_query += 1
        sum_ap += _cur_ap

    if gt_pos:
        print 'no results for queries: ', gt_pos.keys()
        sys.exit(1)

    print 'mAP for %s: %.5f' % (result_file_name, sum_ap / float(num_query))


