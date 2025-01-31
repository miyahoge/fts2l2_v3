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
##@param [in]  id 気体識別　id=CO2,CH4,CO
##@param [in]  Bias_Num バイアス補正パラメータ個数
##@return バイアス補正パラメータデータセット
def Read_Bias_Param(id, sysin):

    h5path = sysin.PRODFILEPATH_SWFP

    with h5py.File(h5path,'r') as f:
        if id == 'CO2': #CO2データ入力
            X = sysin.CO2_X         # 補正パラメータのデータセットパスを取得
            Num = sysin.CO2_X_NUM   # 補正パラメータのデータセットパスの数
        elif id == 'CH4':
            X = sysin.CH4_X
            Num = sysin.CH4_X_NUM
        elif id == 'CO':
            X = sysin.CO_X
            Num = sysin.CO_X_NUM

        for ii in range(Num):
            X_str = X[ii] # データセットのパス NUM の個数だけ（上限29）ある
            X_str_list = X_str.split(',') # データセットのカンマ区切りをリストに分割
            Bias_Param_Dataset = []
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

