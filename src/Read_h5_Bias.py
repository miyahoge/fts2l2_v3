"""
@file Read_h5_Bias.py
@brief HDF5形式のプロダクトデータファイルから、バイアス補正パラメータを読み込むモジュール
"""
import h5py
import numpy as np

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

##@brief SWFPプロダクトのHDF5形式ファイルを読み込み、補正パラメータを取得
##@param [in]  X データセットパス
##@param [in]  Num バイアス補正パラメータ個数
##@param [in]  h5path h5ファイルパス
##@return バイアス補正パラメータデータセット
def Read_Bias_Param(X, Num, h5path):

    with h5py.File(h5path,'r') as f:

        Bias_Param_Dataset = []
        for ii in range(Num):
            X_str = X[ii] # データセットのパス NUM の個数だけ（上限29）ある
            X_str_list = X_str.split(',') # データセットのカンマ区切りをリストに分割
            for data_path in list(X_str_list):
                if data_path == "none":
                    Bias_Param_Dataset.append([""])
                else :
                    try:
                        Bias_Param_Dataset.append(f[data_path][()])
                    except KeyError:
                        logger.error('バイアス補正パラメータのデータセットパスに誤りがあります。{}'.format(data_path))
                        return id
        return Bias_Param_Dataset

