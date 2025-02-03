
"""
@file Calc_Correct_Param.py
@brief バイアス補正パラメータを、バイアス補正パラメータデータセットと計算式から計算するモジュール
"""

import math
import re

##@class Calc_Correct
##@brief バイアス補正パラメータ計算クラス
class Calc_Correct:

    ##@brief クラスの初期化メソッド（コンストラクタ）
    def __init__(self):
        self.pi = 4.*math.atan(1.)
        self.set_limit = 5

    ##@brief 長さ2以上リストならリストを、長さ1なら数値に変換
    ##@param [in] value 確認対象リスト
    ##@return var 変換後リストまたは数値
    def assign_value(self, value):
        if isinstance(value, list):
            if len(value) == 1:
                var = value[0]
            else:
                var = value
        else:
            var = value
        return var
    
    ##@brief degreeからradianに変換
    ##@param [in] value 変換対象数値[deg]
    ##@return var 変換後数値 [rad]
    def deg2rad(self, value):
        dtr = self.pi / 180.
        return value*dtr
    
    ##@brief バイアス補正パラメータ計算
    ##@param [in] X_NUM バイアス補正パラメータ個数
    ##@param [in] X_CAL バイアス補正パラメータ計算式
    ##@param [in] dat_set バイアス補正パラメータ計算元データセット
    ##@return Bias_Param バイアス補正パラメータリスト
    def Calc_Correct_Pram(self, X_NUM, X_CAL, dat_set):
        def ln(x):
            return math.log(x)
        def log10(value):
            return math.log10(value)
        def sin(x):
            return math.sin(x)
        def cos(x):
            return math.cos(x)
        def tan(x):
            return math.tan(x)
        def asin(x):
            return math.asin(x)
        def acos(x):
            return math.acos(x)
        def atan(x):
            return math.atan(x)
        def atan2(x):
            return math.atan2(x)
        def sqrt(x):
            return math.sqrt(x)
    
        Bias_Param = []
        for i in range(X_NUM):
            # 一時変数をここで毎回初期化
            x_tmp =[]
            # データセットの内容を配列か数値かを確認してデータ設定する
            for j in range(self.set_limit):
                x_tmp.append(self.assign_value(dat_set[j+5*i]))
    
            # 文字の置き換え
            expression = X_CAL[i].replace("$","x")
            expression = expression.replace("sigma", "sum")
    
            # 三角関数の場合はデータセットの内容をラジアン変換
            # cos 使用 x をすべて抽出
            matches_cos = re.findall(r"cos\((.*?)\)", expression)
            variables = {}
            if matches_cos:
                for c in matches_cos:
                    idx = int(c[1])
                    x_tmp[idx-1] = self.deg2rad(x_tmp[idx-1])
    
            # sin 使用 x をすべて抽出
            matches_sin = re.findall(r"sin\((.*?)\)", expression)
            variables = {}
            if matches_sin:
                for s in matches_sin:
                    idx = int(s[1])
                    x_tmp[idx-1] = self.deg2rad(x_tmp[idx-1])
    
            # tan 使用 x をすべて抽出
            matches_tan = re.findall(r"tan\((.*?)\)", expression)
            variables = {}
            if matches_tan:
                for t in matches_tan:
                    idx = int(t[1])
                    x_tmp[idx-1] = self.deg2rad(x_tmp[idx-1])
            
            # eval関数で使用する変数名x1~x5にtemp変数を代入する。
            x1 = x_tmp[0]
            x2 = x_tmp[1]
            x3 = x_tmp[2]
            x4 = x_tmp[3]
            x5 = x_tmp[4]
            Bias_Param.append(eval(expression))
        
        return Bias_Param

    
