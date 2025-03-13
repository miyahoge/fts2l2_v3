
"""
@file Calc_Correct_Param.py
@brief バイアス補正パラメータを、バイアス補正パラメータデータセットと計算式から計算するモジュール
"""

import math
import re
import sys
import numpy as np
# ログのライブラリ
from logging import getLogger
## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

##@brief 長さ2以上リストならリストを、長さ1なら数値に変換
##@param [in] value 確認対象リスト
##@return var 変換後リストまたは数値
def assign_value(value):
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
##@attention valueには必ず1個の実数値を設定すること
##@return var 変換後数値 [rad]
def deg2rad(value):
    pi = 4.*math.atan(1.)
    dtr = pi / 180.
    if isinstance(value, list):
        logger.error('バイアス補正パラメータの計算で予期せぬエラー: {}'.format("must be real number, not list"))
        sys.exit(1)
    
    return value*dtr
   
##@brief バイアス補正パラメータ計算
##@param [in] X_NUM バイアス補正パラメータ個数
##@param [in] X_CAL バイアス補正パラメータ計算式
##@param [in] dat_set バイアス補正パラメータ計算元データセット
##@return Bias_Param バイアス補正パラメータリスト
def Calc_Correct_Pram(X_NUM, X_CAL, dat_set):
    def ln(x):
        return np.log(x)
    def log10(x):
        return np.log10(x)
    def sin(x):
        return np.sin(x)
    def cos(x):
        return np.cos(x)
    def tan(x):
        return np.tan(x)
    def asin(x):
        return np.asin(x)
    def acos(x):
        return np.acos(x)
    def atan(x):
        return np.atan(x)
    def atan2(x):
        return np.atan2(x)
    def sqrt(x):
        return np.sqrt(x)
   
    Bias_Param = []
    set_limit = 5
    for i in range(X_NUM):
        # 一時変数をここで毎回初期化
        x_tmp =[]
        fst_flg = [1,1,1,1,1]
        # データセットの内容を配列か数値かを確認してデータ設定する
        for j in range(set_limit):
            x_tmp.append(assign_value(dat_set[j+5*i]))
   
        # 文字の置き換え
        expression = X_CAL[i].replace("$","x")

        # sigma を np.sum にして各行の和とする（ただし、指定したパスが２次元配列以上でなければ値をそのまま返す）
        pattern = r"sigma\((x\d+)\)"
        replacement = r"np.sum(\1, axis=1) if \1.ndim > 1 else \1"
        # sigmaを置換する際は文字列の中にif文を設けて、x1などの配列が2次元未満であれば値をそのまま返す
        # 置換を実行
        expression = re.sub(pattern, replacement, expression)
   
        # 三角関数の場合はデータセットの内容をラジアン変換
        # cos 使用 x をすべて抽出
        matches_cos = re.findall(r"cos\((.*?)\)", expression)
        if matches_cos:
            for c in matches_cos:
                idx = int(c[1])
                if fst_flg[idx-1]==1:  # 初回判定　初回だけラジアン変換
                    x_tmp[idx-1] = deg2rad(x_tmp[idx-1])
                    fst_flg[idx-1]=0
   
        # sin 使用 x をすべて抽出
        matches_sin = re.findall(r"sin\((.*?)\)", expression)
        if matches_sin:
            for s in matches_sin:
                idx = int(s[1])
                if fst_flg[idx-1]==1:  # 初回判定　初回だけラジアン変換
                    x_tmp[idx-1] = deg2rad(x_tmp[idx-1])
                    fst_flg[idx-1]=0
   
        # tan 使用 x をすべて抽出
        matches_tan = re.findall(r"tan\((.*?)\)", expression)
        if matches_tan:
            for t in matches_tan:
                idx = int(t[1])
                if fst_flg[idx-1]==1:  # 初回判定　初回だけラジアン変換
                    x_tmp[idx-1] = deg2rad(x_tmp[idx-1])
                    fst_flg[idx-1]=0
        
        # eval関数で使用する変数名x1~x5にtemp変数を代入する。
        x1 = x_tmp[0]
        x2 = x_tmp[1]
        x3 = x_tmp[2]
        x4 = x_tmp[3]
        x5 = x_tmp[4]
        try:
            Bias_Param.append(eval(expression))
        except SyntaxError:
            logger.error('バイアス補正パラメータの計算式構文エラー: {}'.format(expression))
            print("バイアス補正パラメータの計算式構文エラー 計算式を修正してください。{}".format(expression))
            sys.exit(1)
        except NameError:
            logger.error('バイアス補正パラメータの計算式変数エラー: {}'.format(expression))
            print("バイアス補正パラメータの計算式変数エラー 変数名を修正してください。: {}".format(expression))
            sys.exit(1)
        except Exception as e:
            logger.error('バイアス補正パラメータの計算で予期せぬエラー: {}'.format(e))
            print("バイアス補正パラメータの計算で予期せぬエラー 制御データファイルを確認してください。: {}".format(e))
            sys.exit(1)

            
    return Bias_Param

    
