#!/usr/bin/python3

# 試験用データクリエーター
#
# Author: Zhao
#
# Waterfall -v1.0 (2018-03-07T15:00:58+09)
#
# Copyright 2018 Fujitsu General Limited
# ==========================================
""" 室内機情報 """


class R02(object):
    """ 室内機運転情報

    運転状態（必要な部分だけ）埋め込む

    Attributes:
        rcg_id: RCGID
        __mode: 運転モード (9)
        __limited: 室内機温度上下限設定有無(55)
    """

    def __init__(self, mode, limited, rcg_id):
        self.__mode = mode
        self.__limited = limited
        self.__rcg_id = rcg_id

    def get_parameter(self, idx):
        """ 運転情報を取得

        指定したインデクスに従って必要な情報をゲットする

        Args:
            idx: インデクス 9: 運転モード、55：室内機温度上下限設定有無

        Returns: 運転状態の場合：
                 0:冷房 1:除湿 2:暖房 3:自動 4:送風 5:混在
                 6:機能無し 7:冷暖房別自動
                 室内機温度上下限設定有無の場合
                 0:無し 1:有り 2:混在 3:機能無し
        """
        if idx == 9:
            return self.__mode
        if idx == 55:
            return self.__limited
        if idx == 1:
            return self.__rcg_id
        return None


class R03(object):
    """ 室内機静的情報

    静的情報（機能情報）を埋め込む

    Attributes:
        __has_auto: 自動モード有無(18)
        __has_heat: 暖房モード有無(19)
        __has_cool: 冷房モード有無(20)
        __has_custom: 新自動モード有無(81)
        __lower_auto: 自動下限値(0~63.5)(37)
        __upper_auto: 自動上限値(0~63.5)(38)
        __lower_heat: 暖房下限値(0~63.5)(39)
        __upper_heat: 暖房上限値(0~63.5)(40)
        __lower_cool: 冷房下限値(0~63.5)(41)
        __upper_cool: 冷房上限値(0~63.5)(42)
        __dead_band: デッドバンド(0~7.0)(82)
        __rcg_id: RCGID
    """

    def __init__(self, has_auto, has_heat, has_cool, has_custom,
                 lower_auto, upper_auto, lower_heat, upper_heat,
                 lower_cool, upper_cool, dead_band, rcg_id):
        self.__has_auto = has_auto
        self.__has_heat = has_heat
        self.__has_cool = has_cool
        self.__has_custom = has_custom
        self.__lower_auto = lower_auto
        self.__upper_auto = upper_auto
        self.__lower_heat = lower_heat
        self.__upper_heat = upper_heat
        self.__lower_cool = lower_cool
        self.__upper_cool = upper_cool
        self.__dead_band = dead_band
        self.__rcg_id = rcg_id

    def get_parameter(self, idx):
        """ 静的情報を取得

        指定したインデクスに従って必要な情報をゲットする

        Args:
            idx: インデクス 18: 自動モード有無 19：暖房モード有無
                          20: 冷房モード有無 81: 新自動モード有無
                          37: 自動下限値 38: 自動上限値
                          39: 暖房下限値 40: 暖房上限値
                          41: 冷房下限値 42: 冷房上限値
                          82: デッドバンド

        Returns: 機能有無の場合：1: 機能あり 0: 機能無し
                 温度の場合： 0~63.5
                 デッドバンドの場合： 0~7
        """
        if idx == 18:
            return self.__has_auto
        if idx == 19:
            return self.__has_heat
        if idx == 20:
            return self.__has_cool
        if idx == 81:
            return self.__has_custom
        if idx == 37:
            return self.__lower_auto
        if idx == 38:
            return self.__upper_auto
        if idx == 39:
            return self.__lower_heat
        if idx == 40:
            return self.__upper_heat
        if idx == 41:
            return self.__lower_cool
        if idx == 42:
            return self.__upper_cool
        if idx == 82:
            return self.__dead_band
        if idx == 0:
            return self.__rcg_id
        return None


class R15(object):
    """ 動的温度情報

    動的温度（必要な部分だけ）を埋め込む

    Attributes:
        __status: 設定状態
        __lower_auto: 自動下限値(0~127)(3)
        __upper_auto: 自動上限値(0~127)(4)
        __lower_heat: 暖房下限値(0~127)(5)
        __upper_heat: 暖房上限値(0~127)(6)
        __lower_cool: 冷房下限値(0~127)(7)
        __upper_cool: 冷房上限値(0~127)(8)
        __rcg_id: RCGID
    """

    def __init__(self, status, lower_auto, upper_auto, lower_heat,
                 upper_heat, lower_cool, upper_cool, rcg_id):
        self.__status = status
        self.__lower_auto = lower_auto
        self.__upper_auto = upper_auto
        self.__lower_heat = lower_heat
        self.__upper_heat = upper_heat
        self.__lower_cool = lower_cool
        self.__upper_cool = upper_cool
        self.__rcg_id = rcg_id

    def get_parameter(self, idx):
        """ 動的温度情報を取得

        指定したインデクスに従って必要な情報をゲットする

        Args:
            idx: インデクス

        Returns:
            設定状態
            要求温度
        """
        if idx == 1:
            return self.__status
        if idx == 3:
            return self.__lower_auto
        if idx == 4:
            return self.__upper_auto
        if idx == 5:
            return self.__lower_heat
        if idx == 6:
            return self.__upper_heat
        if idx == 7:
            return self.__lower_cool
        if idx == 8:
            return self.__upper_cool
        if idx == 0:
            return self.__rcg_id
        return None


class Error(Exception):
    """ Base class for exceptions in this module.

    """
    pass


class ReversalError(Error):
    """ 逆転エラー

    下限値と上限値は逆転の場合エラーとして挙げる

    Attributes:
         lower: 下限値
         upper: 上限値
         message: エラーメッセージ
    """

    def __init__(self, lower, upper, message):
        self.lower = lower
        self.upper = upper
        self.message = message


class LogicError(Error):
    """ 矛盾エラー

    機能はない機能で運転する場合エラーとして挙げる

    Attributes:
        function_name: 機能なしの機能名
        message: エラーメッセージ

    """

    def __init__(self, function_name, message):
        self.function_name = function_name
        self.message = message
