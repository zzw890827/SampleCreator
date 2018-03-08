#!/usr/bin/python3

# 試験用データクリエーター
#
# Author: Zhao
#
# Waterfall -v1.0 (2018-03-07T15:00:58+09)
#
# Copyright 2018 Fujitsu General Limited
# ==========================================
""" データ作成用モジュール """

import os
import csv

from model import R02, R03, R15
from model import ReversalError, LogicError


def write_csv_file(array, file_path):
    """ CSVファイルを書き出し

    Args:
        array: 出力しようとする配列
        file_path: 出力場所

    Returns:
        CSVファイル

    Raises:
        データは存在しない場合、ValueErrorをあげる

    """
    with open(file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',')
        if array:
            for row in array:
                writer.writerow(row)
        else:
            raise ValueError
    output_file.close()


def check_data(monitor, static):
    """ パラメータ検証

       入力データを検証：
       １．静的範囲逆転判定
       ２．静的情報と動的情報に矛盾

    Args:
        monitor: R02のインスタンス
        static: R03のインスタンス

    Returns:
        True: データが正しい

    Raises:
         ReversalError: 静的上下限逆転
         LogicError: 運転状態矛盾
    """
    # 矛盾チェック
    if not static.get_parameter(18) and monitor.get_parameter(9) == 3:
        raise LogicError('自動',
                         '自動機能はないが、自動で運転している！')

    if not static.get_parameter(81) and monitor.get_parameter(9) == 7:
        raise LogicError('新自動',
                         '新自動機能はないが、新自動で運転している！')

    if not static.get_parameter(19) and monitor.get_parameter(9) == 2:
        raise LogicError('暖房',
                         '暖房機能はないが、暖房で運転している！')

    if not static.get_parameter(20) and monitor.get_parameter(9) == 0:
        raise LogicError('冷房',
                         '冷房機能はないが、冷房で運転している！')

    if not static.get_parameter(81) and static.get_parameter(82) != -1:
        raise LogicError('新自動',
                         '新自動機能はないが、デッドバンドは存在！')

    if static.get_parameter(81) and static.get_parameter(82) == -1:
        raise LogicError('新自動',
                         '新自動機能はあるが、デッドバンドは存在しない！')

    # 逆転チェック
    if static.get_parameter(37) > static.get_parameter(38):
        raise ReversalError(static.get_parameter(37),
                            static.get_parameter(38),
                            '自動は逆転している！')

    if static.get_parameter(39) > static.get_parameter(40):
        raise ReversalError(static.get_parameter(39),
                            static.get_parameter(40),
                            '暖房は逆転している！')

    if static.get_parameter(41) > static.get_parameter(42):
        raise ReversalError(static.get_parameter(41),
                            static.get_parameter(42),
                            '冷房は逆転している！')
    return True


def create_input_array(monitor, static, dynamic):
    """ 試験用インプット配列作成

    Args:
        monitor: R02情報
        static: R03情報
        dynamic: R15情報

    Returns:
        [R02, R03, R15]
    """
    # R02配列作成
    # 初期化
    sel_r02 = []
    for i in range(64):
        sel_r02.append(0)
    # データを埋め込む
    index_table = [1, 9, 55]
    for i in index_table:
        sel_r02[i] = monitor.get_parameter(i)

    # R03配列作成
    # 初期化
    sel_r03 = []
    for i in range(83):
        sel_r03.append(0)
    # データを埋め込む
    index_table = [0, 18, 19, 20, 38, 39, 40, 41, 42, 81, 82]
    for i in index_table:
        sel_r03[i] = static.get_parameter(i)

    # R15配列作成
    # 初期化
    sel_r15 = []
    for i in range(9):
        sel_r15.append(0)
    # データを埋め込む
    index_table = [0, 1, 3, 4, 5, 6, 7, 8]
    for i in index_table:
        sel_r15[i] = dynamic.get_parameter(i)

    sel_rcg_info = [[], [], []]
    sel_rcg_info[0] = sel_r02
    sel_rcg_info[1] = sel_r03
    sel_rcg_info[2] = sel_r15

    return sel_rcg_info


def create_sample_file(input_file, check=False):
    """ 試験用ファイルを作成

    Args:
        input_file: 入力データ
        check: 検証モード（デフォルトOFF）

    Returns:
       R02monUnit.csv
       R03infUnit.csv
       R15tempSet.csv
    """
    input_info = []
    for line in input_file:
        input_info.append(line.replace('\n', '').split(' '))

    total_case = int(input_info[0][0])  # caseの総数
    row_pos = 1
    for case_count in range(total_case):  # case分ループ
        sel_r02 = []
        sel_r03 = []
        sel_r15 = []
        rcg_id = 256
        n = int(input_info[row_pos][0])  # 台数
        for j in range(n):  # 台数ループ分
            # R02
            pos = row_pos + 1 + j * 3
            mode = int(input_info[pos][0])
            is_limited = int(input_info[pos][1])
            r02 = R02(mode, is_limited, rcg_id)  # R02インスタンス

            # R03
            pos = row_pos + 2 + j * 3
            has_auto = int(input_info[pos][0])  # 自動機能情報
            has_heat = int(input_info[pos][1])  # 暖房機能情報
            has_cool = int(input_info[pos][2])  # 冷房機能情報
            has_custom = int(input_info[pos][3])  # 新自動機能情報
            lower_auto = int(input_info[pos][4])  # 自動下限値
            upper_auto = int(input_info[pos][5])  # 自動上限値
            lower_heat = int(input_info[pos][6])  # 暖房下限値
            upper_heat = int(input_info[pos][7])  # 暖房上限値
            lower_cool = int(input_info[pos][8])  # 冷房下限値
            upper_cool = int(input_info[pos][9])  # 冷房上限値
            dead_band = int(input_info[pos][10])  # デッドバンド

            r03 = R03(has_auto, has_heat, has_cool, has_custom,
                      lower_auto, upper_auto, lower_heat, upper_heat,
                      lower_cool, upper_cool, dead_band, rcg_id)

            # R15
            pos = row_pos + 3 + j * 3
            status = int(input_info[pos][0])  # 制限状態
            lower_auto = int(input_info[pos][1])  # 自動下限値
            upper_auto = int(input_info[pos][2])  # 自動上限値
            lower_heat = int(input_info[pos][3])  # 暖房下限値
            upper_heat = int(input_info[pos][4])  # 暖房上限値
            lower_cool = int(input_info[pos][5])  # 冷房下限値
            upper_cool = int(input_info[pos][6])  # 冷房上限値

            r15 = R15(status, lower_auto, upper_auto, lower_heat,
                      upper_heat, lower_cool, upper_cool, rcg_id)
            # 検証
            if check:
                check_data(r02, r03)
            # 配列化
            sel_rcg_info = create_input_array(r02, r03, r15)
            sel_r02.append(sel_rcg_info[0])
            sel_r03.append(sel_rcg_info[1])
            sel_r15.append(sel_rcg_info[2])
            rcg_id = rcg_id + 1
        # ファイルを書き出し
        fold_name = 'case' + ('00' + str(case_count + 1))[-2:] + '/'
        os.mkdir(fold_name)
        path_r02 = fold_name + 'R02monUnit.csv'
        path_r03 = fold_name + 'R03infUnit.csv'
        path_r15 = fold_name + 'R15tempSet.csv'
        write_csv_file(sel_r02, path_r02)  # R02monUnit.csv
        write_csv_file(sel_r03, path_r03)  # R03infUnit.csv
        write_csv_file(sel_r15, path_r15)  # R15tempSet.csv
        row_pos = row_pos + 1 + n * 3
