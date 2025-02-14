"""
@file Create_SWFPImage.py
@brief SWFPプロダクトからデータを抽出、格子データを作成し、描画処理するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")


##@brief SWFPプロダクトからデータを抽出、格子データを作成し、描画処理する
##@param [in] sysin  制御データクラス
##@param [in] co2_sysin CO2用制御データセットクラス
##@param [in] ch4_sysin CH4用制御データセットクラス
##@param [in] co_sysin CO用制御データセットクラス
##@return ERR = 0：正常, 1~12：取得できなかった月
def Create_SWFPImage(sysin, co2_sysin, ch4_sysin, co_sysin):
    
    import numpy as np
    import sys
    
    import Create_GridData
    
    #SWFPプロダクトファイルデータを取得
    import Input_SWFPData as FP_DAT
    import Version_c as Ver
    import XYZQ_c
    import Draw_Map as DM
    import Get_Reexe_Num as Re_Num

    #各気体データ取得クラスコンストラクタ
    FP_CO2 = XYZQ_c.XYZQ()
    FP_CH4 = XYZQ_c.XYZQ()
    FP_CO  = XYZQ_c.XYZQ()
    #エラーフラグ0
    ERR = 0

    #再処理の実施有無による設定
    if sysin.REEXEFLG == 1:
        begin_fp, end_fp = sysin.GetPeriod('SWFP')
        num = Re_Num.Get_Reexe_Num(sysin, begin_fp, end_fp)
    else:
        num = 1

    #バージョン設定
    FP_Ver = Ver.Version()
    FP_Ver.Set_Version(sysin.PRODFILEPATH_SWFP, FP_CO, 'SWFP')
    ver = FP_Ver.Get_Version()
    if ver == 'none':
        logger.warn('FILE_OPEN_ERROR：読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format('SWFP'))
        print('読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format('SWFP'))
        return ERR

    for i in range(num):
        # プロダクトデータ取得(計算範囲の始点と終点を取得)
        ERR, calcbegin_t, calcend_t = FP_DAT.Input_SWFPData(sysin, FP_CH4, FP_CO, FP_CO2)

        if (ERR > 0) and (ERR < 13):
            return ERR

        #ファイル名の日付設定
        begin = str(calcbegin_t.year) + '{:0>2}'.format(calcbegin_t.month) + '{:0>2}'.format(calcbegin_t.day)
        end   = str(calcend_t.year) + '{:0>2}'.format(calcend_t.month) + '{:0>2}'.format(calcend_t.day)
        date_period = begin + '_' + end + '_tmp.png'

        if FP_CO2.IsGetInfo():   #取得対象か？
            #観測点と観測データ設定
            X_CO2, Y_CO2, Z_CO2, Q_CO2, LF_CO2, myid = FP_CO2.GetData()
            #格子データ作成
            grid_CO2 = Create_GridData.griddata(X_CO2, Y_CO2, Z_CO2, step = sysin.SPACIALSTEP)
        
            #描画処理   
            pltfpco2 = DM.Draw_Map(sysin, co2_sysin, begin, end, grid_CO2, ver, myid)
            if (sysin.BIAS_FLAG):
                pltfpco2.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CO2_' + sysin.CO2_VER + '_' + date_period)
            else:
                pltfpco2.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CO2_' + date_period)
            pltfpco2.close()
        else:
            logger.info('SWFP_CO2データを取得していません。')
        
        if FP_CH4.IsGetInfo():   #取得対象か？
            #観測点と観測データ設定
            X_CH4, Y_CH4, Z_CH4, Q_CH4, LF_CH4 , myid= FP_CH4.GetData()
            #格子データ作成
            grid_CH4 = Create_GridData.griddata(X_CH4, Y_CH4, Z_CH4, step = sysin.SPACIALSTEP)
        
            #描画処理   
            pltfpch4 = DM.Draw_Map(sysin, ch4_sysin, begin, end, grid_CH4, ver, myid)
            if (sysin.BIAS_FLAG):
                pltfpch4.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CH4_' + sysin.CH4_VER + '_' + date_period)
            else:
                pltfpch4.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CH4_' + date_period)
            pltfpch4.close()
        else:
            logger.info('SWFP_CH4データを取得していません。')
        
        if FP_CO.IsGetInfo():   #取得対象か？
            #観測点と観測データ設定
            X_CO, Y_CO, Z_CO, Q_CO, LF_CO , myid= FP_CO.GetData()
            #格子データ作成
            grid_CO = Create_GridData.griddata(X_CO, Y_CO, Z_CO, step = sysin.SPACIALSTEP)
        
            #描画処理
            pltfpco = DM.Draw_Map(sysin, co_sysin, begin, end, grid_CO, ver, myid)
            if (sysin.BIAS_FLAG):
                pltfpco.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CO_' + sysin.CO_VER + '_' + date_period)
            else:
                pltfpco.savefig(sysin.IMGPATH + '\SWFP' + ver + 'CO_' + date_period)
            pltfpco.close()
        else:
            logger.info('SWFP_COデータを取得していません。')

        if ERR != 0:
            break

    
    return ERR