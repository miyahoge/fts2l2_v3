"""
@file Input_SWPRData.py
@brief SWPRプロダクトデータを入力するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")


##@brief SWPRプロダクトからデータを取得し、有効データのみを抽出
##@param [in] sysin  制御データクラス
##@param [in, out] PR_CH4 CH4用データセットクラス
##@param [in, out] PR_CO CO用データセットクラス
##@param [in, out] PR_SIF SIF用データセットクラス
##@return ERR 0：正常, 1～12：ファイルが無かった月
##@return calcbegin_t 計算開始日付
##@return calcend_t 計算終了日付
def Input_SWPRData(sysin, PR_CH4, PR_CO, PR_SIF):
    import numpy as np
    from datetime import datetime
    
    prfile_id = 'SWPR'
    file_folder = sysin.PRODFILEPATH_SWPR
    threshold = 10.0  #陸域判定閾値

    begin = sysin.BEGINDATE_PR
    end   = sysin.ENDDATE_PR
    #制御データの始点と終点を取得
    begin_t = datetime.strptime(begin, '%Y%m%d')
    end_t   = datetime.strptime(end, '%Y%m%d')
    #計算始点と終点用datetimeを初期化
    string_date = '2000/01/01'
    # string to datetime
    calcbegin_t = datetime.strptime(string_date, '%Y/%m/%d')
    calcend_t   = datetime.strptime(string_date, '%Y/%m/%d')
    
    PR = [1, 1, 1]    #エラーフラグ（初期値=ERROR）
    ERR = 0
    if sysin.SWPR_CH4 == 1:
        file_ch4idx = 0
        print('--------SWPR_CH4取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        PR[0], file_ch4idx, calcbegin_t, calcend_t = PR_CH4.Input_common(sysin, prfile_id, file_folder, begin_t, end_t)
        ERR =  PR[0]
        if PR[0] == 0:
            print('--------SWPR_CH4取得完了--------')
            logger.info('SWPR_CH4取得完了')
            # 品質、濃度からデータを設定
            PR_CH4.Set_ProdData(prfile_id, file_ch4idx, 0)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_PRCH4 == 2:
                PR_CH4.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_PRCH4 == 3:
                PR_CH4.Set_byLandFraction_Sea(threshold)
        
    if sysin.SWPR_CO == 1:
        file_coidx = 0
        print('--------SWPR_CO取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        PR[1], file_coidx, calcbegin_t, calcend_t = PR_CO.Input_common(sysin, prfile_id, file_folder, begin_t, end_t)
        ERR =  PR[1]
        if PR[1] == 0:
            print('--------SWPR_CO取得完了--------')
            logger.info('SWPR_CO取得完了')
            # 品質、濃度からデータを設定
            PR_CO.Set_ProdData(prfile_id, file_coidx, 1)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_PRCO == 2:
                PR_CO.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_PRCO == 3:
                PR_CO.Set_byLandFraction_Sea(threshold)

    if sysin.SWPR_SIF == 1:
        file_sifidx = 0
        print('--------SWPR_SIF取得開始--------')
        # 撮像中心点緯度経度、観測点数等を取得
        PR[2], file_sifidx, calcbegin_t, calcend_t = PR_SIF.Input_common(sysin, prfile_id, file_folder, begin_t, end_t)
        ERR =  PR[2] 
        if PR[2] == 0:
            print('--------SWPR_SIF取得完了--------')
            logger.info('SWPR_SIF取得完了')
            # 品質、濃度からデータを設定
            PR_SIF.Set_ProdData(prfile_id, file_sifidx, 2)
            #陸域のみ指定の場合は海域分のデータを削除
            if sysin.MAPRNG_PRSIF == 2:
                PR_SIF.Set_byLandFraction_Land(threshold)
            #海域のみ指定の場合は陸域分のデータを削除
            elif sysin.MAPRNG_PRSIF == 3:
                PR_SIF.Set_byLandFraction_Sea(threshold)

    return ERR, calcbegin_t, calcend_t