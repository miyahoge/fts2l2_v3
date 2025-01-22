"""
@file main.py
@brief L2マップツールメインモジュール
"""


##@brief L2マップ作成ツールメインモジュール
def main():
    
    import sys
    args = sys.argv

    if len(args) < 3:
        print("引数が不足しています")
        print("第1引数：制御データファイル")
        print("第2引数：実行リストファイル")
        sys.exit(1)

    print('********処理開始********')

    sysin_file = args[1]
    log_file   = args[2]
    # ------------ 出力ログ設定
    import logging
    format="%(asctime)s func:%(funcName)s [line:%(lineno)4d] %(levelname)-8s：%(message)s"
    logging.basicConfig(filename = log_file, level = logging.INFO,
                        format = format.format(), filemode = 'w')
    from logging import getLogger
    logger = getLogger('Log')
    # -------------

    #=========================
    #初期設定                =
    #=========================

    #制御データの入力
    import Input_Sysin
    import Settings_For_Map_c as SetMap
    sysin = Input_Sysin.configInit(sysin_file)
    sysin.Input_Sysin(sysin_file)
    #制御データ入力値チェック
    if False == sysin.Check_sysin() :
        logger.error('制御データREAD　ERROR')
        print('[main] 制御データREAD　ERROR')
        sys.exit(1)
        
    #=========================
    #SWFPプロダクト処理      =
    #=========================
    FP_result = 0
    #気体ごとにコンストラクタコール
    fpco2f_sysin = SetMap.SetSysin_For_Map()
    fpch4_sysin  = SetMap.SetSysin_For_Map()
    fpco_sysin   = SetMap.SetSysin_For_Map()
    #SWFPの制御データ設定
    fpco2f_sysin.Set_sysin(sysin.TITLEFP_CO2, sysin.COLORID_FPCO2, sysin.COLORBAR_TITLE_FPCO2, 
                           sysin.COLORSCALEMAX_FPCO2, sysin.COLORSCALEMIN_FPCO2, sysin.SCALESTEP_FPCO2, \
                           sysin.BEGINDATE_FP, sysin.ENDDATE_FP)
    fpch4_sysin.Set_sysin(sysin.TITLEFP_CH4, sysin.COLORID_FPCH4, sysin.COLORBAR_TITLE_FPCH4, 
                          sysin.COLORSCALEMAX_FPCH4, sysin.COLORSCALEMIN_FPCH4, sysin.SCALESTEP_FPCH4, \
                          sysin.BEGINDATE_FP, sysin.ENDDATE_FP)
    fpco_sysin.Set_sysin(sysin.TITLEFP_CO, sysin.COLORID_FPCO, sysin.COLORBAR_TITLE_FPCO, 
                         sysin.COLORSCALEMAX_FPCO, sysin.COLORSCALEMIN_FPCO, sysin.SCALESTEP_FPCO, \
                         sysin.BEGINDATE_FP, sysin.ENDDATE_FP)

    import Create_SWFPImage as SWFP

    if sysin.SWFP_CO2 + sysin.SWFP_CH4 + sysin.SWFP_CO == 0:
        print('SWFPは出力対象外')
    else:
        #SWFPマップ作成
        FP_result = SWFP.Create_SWFPImage(sysin, fpco2f_sysin, fpch4_sysin, fpco_sysin)

 
    #=========================
    #SWPRプロダクト処理      =
    #=========================
    PR_result = 0
    #気体ごとにコンストラクタコール
    prch4_sysin = SetMap.SetSysin_For_Map()
    prco_sysin  = SetMap.SetSysin_For_Map()
    prsif_sysin = SetMap.SetSysin_For_Map()

    #SWPRの制御データ設定
    prch4_sysin.Set_sysin(sysin.TITLEPR_CH4, sysin.COLORID_PRCH4, sysin.COLORBAR_TITLE_PRCH4, \
                          sysin.COLORSCALEMAX_PRCH4, sysin.COLORSCALEMIN_PRCH4, sysin.SCALESTEP_PRCH4, \
                          sysin.BEGINDATE_PR, sysin.ENDDATE_PR)
    prco_sysin.Set_sysin(sysin.TITLEPR_CO, sysin.COLORID_PRCO, sysin.COLORBAR_TITLE_PRCO, \
                         sysin.COLORSCALEMAX_PRCO, sysin.COLORSCALEMIN_PRCO, sysin.SCALESTEP_PRCO, \
                          sysin.BEGINDATE_PR, sysin.ENDDATE_PR)
    prsif_sysin.Set_sysin(sysin.TITLEPR_SIF, sysin.COLORID_PRSIF, sysin.COLORBAR_TITLE_PRSIF, \
                          sysin.COLORSCALEMAX_PRSIF, sysin.COLORSCALEMIN_PRSIF, sysin.SCALESTEP_PRSIF, \
                          sysin.BEGINDATE_PR, sysin.ENDDATE_PR)

    import Create_SWPRImage as SWPR

    if sysin.SWPR_CH4 + sysin.SWPR_CO + sysin.SWPR_SIF == 0:
        swpr_flg = 0;
        print('SWPRは出力対象外')
    else:
       #SWPRマップ作成
       PR_result = SWPR.Create_SWPRImage(sysin, prch4_sysin, prco_sysin, prsif_sysin)

        
    #画像データ圧縮＆サムネイル画像作成
    import Create_Thumbnail as Thumb
    Thumb.CreateThumbnail(sysin)
    logger.info('サムネイル画像作成終了')

    #データの月の連続性がなかった場合
    if FP_result != 0:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('SWFPの、指定期間内%d月のプロダクトファイルが指定フォルダに存在しませんでした。' %FP_result)
        print('必要に応じてプロダクトファイル格納フォルダを確認してください。')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    
    if PR_result != 0:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('SWPRの、指定期間内%d月のプロダクトファイルが指定フォルダに存在しませんでした。' %PR_result)
        print('必要に応じてプロダクトファイル格納フォルダを確認してください。')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    print('********処理完了********')
    logger.info('********処理正常終了********')


if __name__ == '__main__':
    main()
