"""
@file Bias_Correct.py
@brief 補正係数とバイアス補正パラメータからバイアス補正計算を実施し、気体濃度のバイアス補正計算結果を出力するモジュール
"""
import numpy as np


##@brief 補正係数とバイアス補正パラメータからバイアス補正計算を実施
##@param [in] Z バイアス補正前気体濃度
##@param [in] A 補正係数30個
##@param [in] X 最大29個のバイアス補正パラメータ配列
##@return バイアス補正後気体濃度
def Bias_Correct(Z, A, X):

    Z_AddA0 = Z + A[0] # 気体濃度＋補正係数[0]
    SigmaAX = np.zeros(len(Z)) # 0で初期化(気体濃度と同じサイズ)
    for ii in range(len(X)): # 補正係数×補正パラメータ
        SigmaAX += A[ii+1] * X[ii]

    Z_BiasCorrected = Z_AddA0 + SigmaAX # 補正計算結果

    return Z_BiasCorrected
