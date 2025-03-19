"""
@file Input_SWFPData.py
@brief SWFPプロダクトデータを入力するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")


##@brief SWFPプロダクトからデータを取得し、有効データのみを抽出
##@brief バイアス補正フラグONの場合はバイアス補正用制御データを設定し、気体濃度のバイアス補正計算実施
##@param [in] sysin  制御データクラス
##@param [in, out] FP_CH4　CH4用データセットクラス
##@param [in, out] FP_CO　CO用データセットクラス
##@param [in, out] FP_CO2　CO2用データセットクラス
##@return ERR 0：正常, 1～12：ファイルが無かった月
##@return calcbegin_t 計算開始日付
##@return calcend_t 計算終了日付
def Input_SWFPData(sysin, FP_CH4, FP_CO, FP_CO2):

    import numpy as np
    from datetime import datetime

    #SWFPプロダクトの共通項を入力

    fpfile_id = 'SWFP'
    file_folder = sysin.PRODFILEPATH_SWFP
    threshold = 10.0  #陸域判定閾値

    begin = sysin.BEGINDATE_FP
    end   = sysin.ENDDATE_FP
    #制御データの始点と終点を取得
    begin_t = datetime.strptime(begin, '%Y%m%d')
    end_t   = datetime.strptime(end, '%Y%m%d')
    #計算始点と終点用datetimeを初期化
    string_date = '2000/01/01'
    # string to datetime
    calcbegin_t = datetime.strptime(string_date, '%Y/%m/%d')
    calcend_t   = datetime.strptime(string_date, '%Y/%m/%d')

    FP = [1, 1, 1]    #エラーフラグ（初期値=ERROR）
    ERR = 0
    if sysin.SWFP_CO2 == 1:
        file_co2idx = 0
        print('--------SWFP_CO2取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        FP[0], file_co2idx, calcbegin_t, calcend_t = FP_CO2.Input_common(sysin, fpfile_id, file_folder, begin_t, end_t)
        ERR =  FP[0]
        if FP[0] == 0:
            print('--------SWFP_CO2取得完了--------')
            logger.info('SWFP_CO2取得完了')
        
            # 品質、濃度からデータを設定
            # バイアス補正フラグONの場合、バイアス補正用制御データを設定し、気体濃度のバイアス補正計算実施
            if sysin.BIAS_FLAG:
                FP_CO2.SetBiasSysin(sysin.CO2_X, sysin.CO2_X_NUM, sysin.CO2_X_CAL, sysin.CO2_A, sysin.CO2_A2)
                FP_CO2.Set_ProdData_Bias(file_co2idx, 0, sysin.CHANGE_COEF_FLAG, sysin.CHANGE_COEF_DATE)
            else: # バイアス補正フラグOFFの場合
                FP_CO2.Set_ProdData(fpfile_id, file_co2idx, 0)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_FPCO2 == 2:
                FP_CO2.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_FPCO2 == 3:
                FP_CO2.Set_byLandFraction_Sea(threshold)

    if sysin.SWFP_CH4 == 1:
        file_ch4idx = 0
        print('--------SWFP_CH4取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        FP[1], file_ch4idx, calcbegin_t, calcend_t = FP_CH4.Input_common(sysin, fpfile_id, file_folder, begin_t, end_t)
        ERR =  FP[1]
        if FP[1] == 0:
            print('--------SWFP_CH4取得完了--------')
            logger.info('SWFP_CH4取得完了')
        
            # 品質、濃度からデータを設定
            # バイアス補正フラグONの場合、バイアス補正用制御データを設定し、気体濃度のバイアス補正計算実施
            if sysin.BIAS_FLAG:
                FP_CH4.SetBiasSysin(sysin.CH4_X, sysin.CH4_X_NUM, sysin.CH4_X_CAL, sysin.CH4_A, sysin.CH4_A2)
                FP_CH4.Set_ProdData_Bias(file_ch4idx, 1, sysin.CHANGE_COEF_FLAG, sysin.CHANGE_COEF_DATE)
            else: # バイアス補正フラグOFFの場合
                FP_CH4.Set_ProdData(fpfile_id, file_ch4idx, 1)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_FPCH4 == 2:
                FP_CH4.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_FPCH4 == 3:
                FP_CH4.Set_byLandFraction_Sea(threshold)
    
    if sysin.SWFP_CO == 1:
        file_coidx = 0
        print('--------SWFP_CO取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        FP[2], file_coidx, calcbegin_t, calcend_t = FP_CO.Input_common(sysin, fpfile_id, file_folder, begin_t, end_t)
        ERR =  FP[2]
        if FP[2] == 0:
            print('--------SWFP_CO取得完了--------')
            logger.info('SWFP_CO取得完了')
        
            # 品質、濃度からデータを設定
            # バイアス補正フラグONの場合、バイアス補正用制御データを設定し、気体濃度のバイアス補正計算実施
            if sysin.BIAS_FLAG:
                FP_CO.SetBiasSysin(sysin.CO_X, sysin.CO_X_NUM, sysin.CO_X_CAL, sysin.CO_A, sysin.CO_A2)
                FP_CO.Set_ProdData_Bias(file_coidx, 2, sysin.CHANGE_COEF_FLAG, sysin.CHANGE_COEF_DATE)
            else: # バイアス補正フラグOFFの場合
                FP_CO.Set_ProdData(fpfile_id, file_coidx, 2)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_FPCO == 2:
                FP_CO.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_FPCO == 3:
                FP_CO.Set_byLandFraction_Sea(threshold)
    
    return ERR, calcbegin_t, calcend_t
