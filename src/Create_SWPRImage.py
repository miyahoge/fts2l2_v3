"""
@file Create_SWPRImage.py
@brief SWPRプロダクトからデータを抽出、格子データを作成し、描画処理するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")


##@brief SWPRプロダクトからデータを抽出、格子データを作成し、描画処理する
##@param [in] sysin  制御データクラス
##@param [in] ch4_sysin CH4用制御データセットクラス
##@param [in] co_sysin CO用制御データセットクラス
##@param [in] sif_sysin SIF用制御データセットクラス
##@return ERR 0：正常, 1～12：ファイルが無かった月
def Create_SWPRImage(sysin, ch4_sysin, co_sysin, sif_sysin):
    import numpy as np
    import sys
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator 

    import Create_GridData
    import Input_SWPRData as PR_DAT
    import Version_c as Ver
    import XYZQ_c
    import Draw_Map as DM
    import Get_Reexe_Num as Re_Num

    #各気体データ取得クラスコンストラクタ
    PR_CH4 = XYZQ_c.XYZQ()
    PR_CO  = XYZQ_c.XYZQ()
    PR_SIF = XYZQ_c.XYZQ()
    #エラーフラグ0
    ERR = 0
    #再処理の実施有無による設定
    if sysin.REEXEFLG == 1:
        #制御データの始点と終点を取得
        begin_pr, end_pr = sysin.GetPeriod('SWPR')
        num = Re_Num.Get_Reexe_Num(sysin, begin_pr, end_pr)
    else:
        num = 1
    #バージョン設定
    PR_Ver = Ver.Version()
    PR_Ver.Set_Version(sysin.PRODFILEPATH_SWPR, PR_CH4, 'SWPR')
    ver = PR_Ver.Get_Version()
    if ver == 'none':
        logger.warn('FILE_OPEN_ERROR：読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format('SWPR'))
        print('読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format('SWPR'))
        return ERR

    for i in range(num):
        # プロダクトデータ取得
        ERR, calcbegin_t, calcend_t = PR_DAT.Input_SWPRData(sysin, PR_CH4, PR_CO, PR_SIF)

        if (ERR > 0) and (ERR < 13):
            return ERR

        #ファイル名の日付設定
        begin = str(calcbegin_t.year) + '{:0>2}'.format(calcbegin_t.month) + '{:0>2}'.format(calcbegin_t.day)
        end   = str(calcend_t.year) + '{:0>2}'.format(calcend_t.month) + '{:0>2}'.format(calcend_t.day)
        date_period = begin + '_' + end + '_tmp.png'

        binsize = 0.01
        myid    = ''
        step    = sysin.SPACIALSTEP
        if PR_CH4.IsGetInfo():
            #観測点と観測データ設定
            X_CH4, Y_CH4, Z_CH4, Q_CH4, LF_CH4, myid = PR_CH4.GetData()
            #格子データ作成
            grid_CH4 = Create_GridData.griddata(X_CH4, Y_CH4, Z_CH4, step = sysin.SPACIALSTEP)

            #描画処理
            pltprch4 = DM.Draw_Map(sysin, ch4_sysin, begin, end, grid_CH4, ver, myid)
            pltprch4.savefig(sysin.IMGPATH + '\SWPR' + ver + 'CH4_' + date_period)
            pltprch4.close()
        else:
            logger.info('SWPR_CH4データを取得していません。')
        
        if PR_CO.IsGetInfo():
            #観測点と観測データ設定
            X_CO, Y_CO, Z_CO, Q_CO, LF_CO , myid = PR_CO.GetData()
            #格子データ作成
            grid_CO = Create_GridData.griddata(X_CO, Y_CO, Z_CO, step = sysin.SPACIALSTEP)
        
            #描画処理   
            pltprco = DM.Draw_Map(sysin, co_sysin, begin, end, grid_CO, ver, myid)
            pltprco.savefig(sysin.IMGPATH + '\SWPR' + ver + 'CO_' + date_period)
            pltprco.close()
        else:
            logger.info('SWPR_COデータを取得していません。')
        
        if PR_SIF.IsGetInfo():
            #観測点と観測データ設定
            X_SIF, Y_SIF, Z_SIF, Q_SIF, LF_SIF, myid = PR_SIF.GetData()
            #格子データ作成
            grid_SIF = Create_GridData.griddata(X_SIF, Y_SIF, Z_SIF, step = sysin.SPACIALSTEP)
        
            #描画処理
            pltprsif = DM.Draw_Map(sysin, sif_sysin, begin, end, grid_SIF, ver, myid)
            pltprsif.savefig(sysin.IMGPATH + '\SWPR' + ver + 'SIF_' + date_period)
            pltprsif.close()
        else:
            logger.info('SWPR_SIFデータを取得していません。')

        if ERR != 0:
            break;

    return ERR