#!/usr/bin/python3

# 試験用データクリエーター
#
# Author: Zhao
#
# Waterfall -v1.0 (2018-03-07T15:00:58+09)
#
# Copyright 2018 Fujitsu General Limited
# ==========================================
""" 本アプリ """

import sys

from optparse import OptionParser

from control import create_sample_file


def main():
    usage = 'usage: %prog [options] < path_of_input'
    parser = OptionParser(usage=usage)

    parser.add_option('-c',
                      '--check',
                      action='store_true',
                      dest='check',
                      default=False,
                      help='CSVファイルを作成する前にデータの検証を行う。')

    (options, args) = parser.parse_args()
    file = sys.stdin.readlines()

    create_sample_file(file, check=options.check)


if __name__ == '__main__':
    main()
