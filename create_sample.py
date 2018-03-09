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

__author__ = 'Zhao Zhongwen'
__version__ = '1.0'
__description__ = """
最低限のデータを入力することで、試験用R02、R03、R15のCSVファイルを作成。
"""


import sys

from optparse import OptionParser

from Lib import create_sample_file


def main():
    usage = 'usage: %prog [options] < path_of_input'
    parser = OptionParser(usage=usage,
                          version=__version__,
                          description=__description__)

    parser.add_option('-c',
                      '--check',
                      action='store_true',
                      dest='check',
                      default=False,
                      help='CSVファイルを作成する前にデータの検証を行う。')

    parser.add_option('-r',
                      '--reference',
                      action='store_true',
                      dest='ref',
                      default=False,
                      help='Todo(Zhao): レファレンスを同時に出力。')

    (options, args) = parser.parse_args()
    file = sys.stdin.readlines()

    create_sample_file(file, check=options.check)


if __name__ == '__main__':
    main()
