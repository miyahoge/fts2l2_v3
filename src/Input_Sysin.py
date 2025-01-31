"""
@file Input_Sysin.py
@brief 制御データファイルからパラメータを入力し、データ範囲チェックをするモジュール
"""

 # -*- coding: UTF-8 -*-

# ログのライブラリ
from logging import getLogger

# main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

import os
import sys
import configparser
import numpy as np
import re
##@brief 制御データファイル入力クラス
class configInit:

    ##@brief コンストラクタ
    def __init__(self, sysin_path):
        if not os.path.exists(sysin_path):
            logger.error('制御データファイルが存在しません')
            print('制御データファイルが存在しません')
            sys.exit(1)
            
        #初期値設定
        ##SWFPプロダクトXCO2の出力有無フラグ
        self.SWFP_CO2             = 0
        ##SWFPプロダクトXCO2のマップタイトル
        self.TITLEFP_CO2          = ''
        ##SWFPプロダクトXCH4の出力有無フラグ
        self.SWFP_CH4             = 0
        ##SWFPプロダクトXCH4のマップタイトル
        self.TITLEFP_CH4          = ''
        ##SWFPプロダクトXCOの出力有無フラグ
        self.SWFP_CO              = 0
        ##SWFPプロダクトXCOのマップタイトル
        self.TITLEFP_CO           = ''
        ##SWFPプロダクトのマップ作成期間（始点）
        self.BEGINDATE_FP         = ''
        ##SWFPプロダクトのマップ作成期間（終点）
        self.ENDDATE_FP           = ''
        ##HDF5形式のSWFPプロダクトファイルのフォルダパス
        self.PRODFILEPATH_SWFP    = ''
        ##SWFPプロダクトXCO2のカラー識別
        self.COLORID_FPCO2        = 1
        ##SWFPプロダクトXCO2のマップ領域
        self.MAPRNG_FPCO2         = 1
        ##SWFPプロダクトXCO2のカラーバーラベル名
        self.COLORBAR_TITLE_FPCO2 = ''
        ##SWFPプロダクトXCO2のカラーバースケール最大値
        self.COLORSCALEMAX_FPCO2  = 430.0
        ##SWFPプロダクトXCO2のカラーバースケール最小値
        self.COLORSCALEMIN_FPCO2  = 370.0
        ##SWFPプロダクトXCO2のカラーバーの刻み幅
        self.SCALESTEP_FPCO2      = 5.0
        ##SWFPプロダクトXCH4のカラー識別
        self.COLORID_FPCH4        = 1
        ##SWFPプロダクトXCH4のマップ領域
        self.MAPRNG_FPCH4         = 1
        ##SWFPプロダクトXCH4のカラーバーラベル名
        self.COLORBAR_TITLE_FPCH4 = ''
        ##SWFPプロダクトXCH4のカラーバースケール最大値
        self.COLORSCALEMAX_FPCH4  = 2.0
        ##SWFPプロダクトXCH4のカラーバースケール最小値
        self.COLORSCALEMIN_FPCH4  = 1.6
        ##SWFPプロダクトXCH4のカラーバーの刻み幅
        self.SCALESTEP_FPCH4      = 0.05
        ##SWFPプロダクトXCOのカラー識別
        self.COLORID_FPCO         = 1
        ##SWFPプロダクトXCOのマップ領域
        self.MAPRNG_FPCO          = 1
        ##SWFPプロダクトXCOのカラーバーラベル名
        self.COLORBAR_TITLE_FPCO  = ''
        ##SWFPプロダクトXCOのカラーバースケール最大値
        self.COLORSCALEMAX_FPCO   = 0.18
        ##SWFPプロダクトXCOのカラーバースケール最小値
        self.COLORSCALEMIN_FPCO   = 0.0
        ##SWFPプロダクトXCOのカラーバーの刻み幅
        self.SCALESTEP_FPCO       = 0.02

        ##SWPRプロダクトXCH4の出力有無フラグ
        self.SWPR_CH4             = 0
        ##SWPRプロダクトXCH4のマップタイトル
        self.TITLEPR_CH4          = ''
        ##SWPRプロダクトXCOの出力有無フラグ
        self.SWPR_CO              = 0
        ##SWPRプロダクトXCOのマップタイトル
        self.TITLEPR_CO           = ''
        ##SWPRプロダクトSIFの出力有無フラグ
        self.SWPR_SIF             = 0
        ##SWPRプロダクトSIFのマップタイトル
        self.TITLEPR_SIF          = ''
        ##SWPRプロダクトのマップ作成期間（始点）
        self.BEGINDATE_PR         = ''
        ##SWPRプロダクトのマップ作成期間（終点）
        self.ENDDATE_PR           = ''
        ##HDF5形式のSWPRプロダクトファイルのフォルダパス
        self.PRODFILEPATH_SWPR    = ''
        ##SWPRプロダクトXCH4のカラー識別
        self.COLORID_PRCH4        = 1
        ##SWPRプロダクトXCH4のマップ領域
        self.MAPRNG_PRCH4         = 1
        ##SWPRプロダクトXCH4のカラーバーラベル名
        self.COLORBAR_TITLE_PRCH4 = ''
        ##SWPRプロダクトXCH4のカラーバースケール最大値
        self.COLORSCALEMAX_PRCH4  = 2.0
        ##SWPRプロダクトXCH4のカラーバースケール最小値
        self.COLORSCALEMIN_PRCH4  = 1.6
        ##SWPRプロダクトXCH4のカラーバーの刻み幅
        self.SCALESTEP_PRCH4      = 0.05
        ##SWPRプロダクトXCOのカラー識別
        self.COLORID_PRCO         = 1
        ##SWPRプロダクトXCOのマップ領域
        self.MAPRNG_PRCO          = 1
        ##SWPRプロダクトXCOのカラーバーラベル名
        self.COLORBAR_TITLE_PRCO  = ''
        ##SWPRプロダクトXCOのカラーバースケール最大値
        self.COLORSCALEMAX_PRCO   = 0.18
        ##SWPRプロダクトXCOのカラーバースケール最小値
        self.COLORSCALEMIN_PRCO   = 0.0
        ##SWPRプロダクトXCOのカラーバーの刻み幅
        self.SCALESTEP_PRCO       = 0.02
        ##SWPRプロダクトSIFのカラー識別
        self.COLORID_PRSIF        = 1
        ##SWPRプロダクトSIFのマップ領域
        self.MAPRNG_PRSIF         = 2
        ##SWPRプロダクトSIFのカラーバーラベル名
        self.COLORBAR_TITLE_PRSIF = ''
        ##SWPRプロダクトSIFのカラーバースケール最大値
        self.COLORSCALEMAX_PRSIF  = 1.4
        ##SWPRプロダクトSIFのカラーバースケール最小値
        self.COLORSCALEMIN_PRSIF  = 0.0
        ##SWPRプロダクトSIFのカラーバーの刻み幅
        self.SCALESTEP_PRSIF      = 0.2
                
        ##再処理実行フラグ
        self.REEXEFLG             = 0
        ##時間平均区間
        self.TIMEAVEID            = 1
        ##空間平均範囲
        self.SPACIALSTEP          = 2.5
        
        ##画像の出力先フォルダパス
        self.IMGPATH              = ''
        #self.CMAPFILE             = 'color_scale_rgb.txt'
        ##X軸（経度）のラベル名
        self.XLABEL               = ''
        ##Y軸（緯度）のラベル名
        self.YLABEL               = ''

        ##バイアス計算用
        # 係数の数
        self.BIAS_COEF_NUM        = 30
        self.BIAS_FLAG = 0
        self.CO2_VER = ''
        self.CH4_VER = ''
        self.CO_VER  = ''
        self.CO2_A = []
        self.CH4_A = []
        self.CO_A  = []
        self.CO2_X_NUM = 3
        self.CH4_X_NUM = 3
        self.CO_X_NUM  = 3
        self.CO2_X = []
        self.CH4_X = []
        self.CO_X  = []
        self.CO2_X_CAL = []
        self.CH4_X_CAL = []
        self.CO_X_CAL  = []
        self.CHANGE_COEF_DATE = ''
        self.CO2_A2 = []
        self.CH4_A2 = []
        self.CO_A2  = []
    
    ##@brief 制御データ入力
    ##@param [in] sysin_path 制御データファイルパス
    def Input_Sysin(self, sysin_path):
        
        config_ini = configparser.ConfigParser()
        config_ini.read(sysin_path, encoding='shiftjis')
        logger.info('----[設定開始]----')
        try:
            logger.info('**SWFP用データを読み込み**')
            self.SWFP_CO2             = int(config_ini['SWFP']['SWFP_CO2'])
            logger.info('SWFP_CO2             = {0}'.format(self.SWFP_CO2))
            self.TITLEFP_CO2          = config_ini['SWFP']['TITLEFP_CO2']
            logger.info('TITLEFP_CO2          = {0}'.format(self.TITLEFP_CO2))
            self.SWFP_CH4             = int(config_ini['SWFP']['SWFP_CH4'])
            logger.info('SWFP_CH4             = {0}'.format(self.SWFP_CH4))
            self.TITLEFP_CH4          =  config_ini['SWFP']['TITLEFP_CH4']
            logger.info('TITLEFP_CH4          = {0}'.format(self.TITLEFP_CH4))
            self.SWFP_CO              = int(config_ini['SWFP']['SWFP_CO'])
            logger.info('SWFP_CO              = {0}'.format(self.SWFP_CO))
            self.TITLEFP_CO           = config_ini['SWFP']['TITLEFP_CO']
            logger.info('TITLEFP_CO           = {0}'.format(self.TITLEFP_CO))
            self.BEGINDATE_FP         = config_ini['SWFP']['BEGINDATE_FP']
            logger.info('BEGINDATE_FP         = {0}'.format(self.BEGINDATE_FP))
            self.ENDDATE_FP           = config_ini['SWFP']['ENDDATE_FP']
            logger.info('ENDDATE_FP           = {0}'.format(self.ENDDATE_FP))
            self.PRODFILEPATH_SWFP    = config_ini['SWFP']['PRODFILEPATH_SWFP']
            logger.info('PRODFILEPATH_SWFP    = {0}'.format(self.PRODFILEPATH_SWFP))
            self.COLORID_FPCO2        = int(config_ini['SWFP']['COLORID_FPCO2'])
            logger.info('COLORID_FPCO2        = {0}'.format(self.COLORID_FPCO2))
            self.MAPRNG_FPCO2        = int(config_ini['SWFP']['MAPRNG_FPCO2'])
            logger.info('MAPRNG_FPCO2         = {0}'.format(self.MAPRNG_FPCO2))
            self.COLORBAR_TITLE_FPCO2 =  config_ini['SWFP']['COLORBAR_TITLE_FPCO2']
            logger.info('COLORBAR_TITLE_FPCO2 = {0}'.format(self.COLORBAR_TITLE_FPCO2))
            self.COLORSCALEMAX_FPCO2  = float(config_ini['SWFP']['COLORSCALEMAX_FPCO2'])
            logger.info('COLORSCALEMAX_FPCO2  = {0}'.format(self.COLORSCALEMAX_FPCO2))
            self.COLORSCALEMIN_FPCO2  = float(config_ini['SWFP']['COLORSCALEMIN_FPCO2'])
            logger.info('COLORSCALEMIN_FPCO2  = {0}'.format(self.COLORSCALEMIN_FPCO2))
            self.SCALESTEP_FPCO2      = float(config_ini['SWFP']['SCALESTEP_FPCO2'])
            logger.info('SCALESTEP_FPCO2      = {0}'.format(self.SCALESTEP_FPCO2))
            self.COLORID_FPCH4        = int(config_ini['SWFP']['COLORID_FPCH4'])
            logger.info('COLORID_FPCH4        = {0}'.format(self.COLORID_FPCH4))
            self.MAPRNG_FPCH4         = int(config_ini['SWFP']['MAPRNG_FPCH4'])
            logger.info('MAPRNG_FPCH4         = {0}'.format(self.MAPRNG_FPCH4))
            self.COLORBAR_TITLE_FPCH4 = config_ini['SWFP']['COLORBAR_TITLE_FPCH4']
            logger.info('COLORBAR_TITLE_FPCH4 = {0}'.format(self.COLORBAR_TITLE_FPCH4))
            self.COLORSCALEMAX_FPCH4  = float(config_ini['SWFP']['COLORSCALEMAX_FPCH4'])
            logger.info('COLORSCALEMAX_FPCH4  = {0}'.format(self.COLORSCALEMAX_FPCH4))
            self.COLORSCALEMIN_FPCH4  = float(config_ini['SWFP']['COLORSCALEMIN_FPCH4'])
            logger.info('COLORSCALEMIN_FPCH4  = {0}'.format(self.COLORSCALEMIN_FPCH4))
            self.SCALESTEP_FPCH4      = float(config_ini['SWFP']['SCALESTEP_FPCH4'])
            logger.info('SCALESTEP_FPCH4      = {0}'.format(self.SCALESTEP_FPCH4))
            self.COLORID_FPCO         = int(config_ini['SWFP']['COLORID_FPCO'])
            logger.info('COLORID_FPCO         = {0}'.format(self.COLORID_FPCO))
            self.MAPRNG_FPCO          = int(config_ini['SWFP']['MAPRNG_FPCO'])
            logger.info('MAPRNG_FPCO          = {0}'.format(self.MAPRNG_FPCO))
            self.COLORBAR_TITLE_FPCO  = config_ini['SWFP']['COLORBAR_TITLE_FPCO']
            logger.info('COLORBAR_TITLE_FPCO  = {0}'.format(self.COLORBAR_TITLE_FPCO))
            self.COLORSCALEMAX_FPCO   = float(config_ini['SWFP']['COLORSCALEMAX_FPCO'])
            logger.info('COLORSCALEMAX_FPCO   = {0}'.format(self.COLORSCALEMAX_FPCO))
            self.COLORSCALEMIN_FPCO   = float(config_ini['SWFP']['COLORSCALEMIN_FPCO'])
            logger.info('COLORSCALEMIN_FPCO   = {0}'.format(self.COLORSCALEMIN_FPCO))
            
            logger.info('**SWPR用データを読み込み**')
            self.SWPR_CH4             = int(config_ini['SWPR']['SWPR_CH4'])
            logger.info('SWPR_CH4             = {0}'.format(self.SWPR_CH4))
            self.TITLEPR_CH4          = config_ini['SWPR']['TITLEPR_CH4']
            logger.info('TITLEPR_CH4          = {0}'.format(self.TITLEPR_CH4))
            self.SWPR_CO              = int(config_ini['SWPR']['SWPR_CO'])
            logger.info('SWPR_CO              = {0}'.format(self.SWPR_CO))
            self.TITLEPR_CO           = config_ini['SWPR']['TITLEPR_CO']
            logger.info('TITLEPR_CO           = {0}'.format(self.TITLEPR_CO))
            self.SWPR_SIF             = int(config_ini['SWPR']['SWPR_SIF'])
            logger.info('SWPR_SIF             = {0}'.format(self.SWPR_SIF))
            self.TITLEPR_SIF          = config_ini['SWPR']['TITLEPR_SIF']
            logger.info('TITLEPR_SIF          = {0}'.format(self.TITLEPR_SIF))
            self.BEGINDATE_PR         = config_ini['SWPR']['BEGINDATE_PR']
            logger.info('BEGINDATE_PR         = {0}'.format(self.BEGINDATE_PR))
            self.ENDDATE_PR           = config_ini['SWPR']['ENDDATE_PR']
            logger.info('ENDDATE_PR           = {0}'.format(self.ENDDATE_PR))
            self.PRODFILEPATH_SWPR    = config_ini['SWPR']['PRODFILEPATH_SWPR']
            logger.info('PRODFILEPATH_SWPR    = {0}'.format(self.PRODFILEPATH_SWPR))
            self.COLORID_PRCH4        = int(config_ini['SWPR']['COLORID_PRCH4'])
            logger.info('COLORID_PRCH4        = {0}'.format(self.COLORID_PRCH4))
            self.MAPRNG_PRCH4         = int(config_ini['SWPR']['MAPRNG_PRCH4'])
            logger.info('MAPRNG_PRCH4         = {0}'.format(self.MAPRNG_PRCH4))
            self.COLORBAR_TITLE_PRCH4 = config_ini['SWPR']['COLORBAR_TITLE_PRCH4']
            logger.info('COLORBAR_TITLE_PRCH4 = {0}'.format(self.COLORBAR_TITLE_PRCH4))
            self.COLORSCALEMAX_PRCH4  = float(config_ini['SWPR']['COLORSCALEMAX_PRCH4'])
            logger.info('COLORSCALEMAX_PRCH4  = {0}'.format(self.COLORSCALEMAX_PRCH4))
            self.COLORSCALEMIN_PRCH4  = float(config_ini['SWPR']['COLORSCALEMIN_PRCH4'])
            logger.info('COLORSCALEMIN_PRCH4  = {0}'.format(self.COLORSCALEMIN_PRCH4))
            self.SCALESTEP_PRCH4      = float(config_ini['SWPR']['SCALESTEP_PRCH4'])
            logger.info('SCALESTEP_PRCH4      = {0}'.format(self.SCALESTEP_PRCH4))
            self.COLORID_PRCO         = int(config_ini['SWPR']['COLORID_PRCO'])
            logger.info('COLORID_PRCO         = {0}'.format(self.COLORID_PRCO))
            self.MAPRNG_PRCO          = int(config_ini['SWPR']['MAPRNG_PRCO'])
            logger.info('MAPRNG_PRCO          = {0}'.format(self.MAPRNG_PRCO))
            self.COLORBAR_TITLE_PRCO  = config_ini['SWPR']['COLORBAR_TITLE_PRCO']
            logger.info('COLORBAR_TITLE_PRCO  = {0}'.format(self.COLORBAR_TITLE_PRCO))
            self.COLORSCALEMAX_PRCO   = float(config_ini['SWPR']['COLORSCALEMAX_PRCO'])
            logger.info('COLORSCALEMAX_PRCO   = {0}'.format(self.COLORSCALEMAX_PRCO))
            self.COLORSCALEMIN_PRCO   = float(config_ini['SWPR']['COLORSCALEMIN_PRCO'])
            logger.info('COLORSCALEMIN_PRCO   = {0}'.format(self.COLORSCALEMIN_PRCO))
            self.SCALESTEP_PRCO       = float(config_ini['SWPR']['SCALESTEP_PRCO'])
            logger.info('SCALESTEP_PRCO       = {0}'.format(self.SCALESTEP_PRCO))
            self.COLORID_PRSIF        = int(config_ini['SWPR']['COLORID_PRSIF'])
            logger.info('COLORID_PRSIF        = {0}'.format(self.COLORID_PRSIF))
            self.MAPRNG_PRSIF         = int(config_ini['SWPR']['MAPRNG_PRSIF'])
            logger.info('MAPRNG_PRSIF         = {0}'.format(self.MAPRNG_PRSIF))
            self.COLORBAR_TITLE_PRSIF = config_ini['SWPR']['COLORBAR_TITLE_PRSIF']
            logger.info('COLORBAR_TITLE_PRSIF = {0}'.format(self.COLORBAR_TITLE_PRSIF))
            self.COLORSCALEMAX_PRSIF  = float(config_ini['SWPR']['COLORSCALEMAX_PRSIF'])
            logger.info('COLORSCALEMAX_PRSIF  = {0}'.format(self.COLORSCALEMAX_PRSIF))
            self.COLORSCALEMIN_PRSIF  = float(config_ini['SWPR']['COLORSCALEMIN_PRSIF'])
            logger.info('COLORSCALEMIN_PRSIF  = {0}'.format(self.COLORSCALEMIN_PRSIF))
            self.SCALESTEP_PRSIF      = float(config_ini['SWPR']['SCALESTEP_PRSIF'])
            logger.info('SCALESTEP_PRSIF      = {0}'.format(self.SCALESTEP_PRSIF))
                       
            logger.info('**計算パラメータを読み込み**')
            self.REEXEFLG    = int(config_ini['CALCPARAM']['REEXEFLG'])
            logger.info('REEXEFLG             = {0}'.format(self.REEXEFLG))
            self.TIMEAVEID   = int(config_ini['CALCPARAM']['TIMEAVEID'])
            logger.info('TIMEAVEID            = {0}'.format(self.TIMEAVEID))
            self.SPACIALSTEP = float(config_ini['CALCPARAM']['SPACIALSTEP'])
            logger.info('SPACIALSTEP          = {0}'.format(self.SPACIALSTEP))
            
            logger.info('**マップ設定データを読み込み**')
            self.IMGPATH   = config_ini['MAP']['IMGPATH']
            logger.info('IMGPATH              = {0}'.format(self.IMGPATH))
            #self.CMAPFILE  = config_ini['MAP']['CMAPFILE']
            #logger.info('CMAPFILE             = {0}'.format(self.CMAPFILE))
            #self.TITLEPOS  = int(config_ini['MAP']['TITLEPOS'])
            self.XLABEL    = config_ini['MAP']['XLABEL']
            logger.info('XLABEL               = {0}'.format(self.XLABEL))
            self.YLABEL    = config_ini['MAP']['YLABEL']
            logger.info('YLABEL               = {0}'.format(self.YLABEL))

            # 以下から2024年度改修（バイアス計算機能追加）で追加
            logger.info('**BIAS用データを読み込み**')
            self.BIAS_FLAG = int(config_ini['BIAS']['BIAS_FLAG'])
            logger.info('BIAS_FLAG = {0}'.format(self.BIAS_FLAG))
            if(self.BIAS_FLAG):
                logger.info('**BIAS補正あり**')
                # 補正係数
                CO2_A_str = config_ini['BIAS']['CO2_A']
                self.CO2_A = [float(num) for num in CO2_A_str.split(",")]
                logger.info('CO2_A  = {0}'.format(self.CO2_A))
                CH4_A_str = config_ini['BIAS']['CH4_A']
                self.CH4_A = [float(num) for num in CH4_A_str.split(",")]
                logger.info('CH4_A  = {0}'.format(self.CH4_A))
                CO_A_str  = config_ini['BIAS']['CO_A']
                self.CO_A  = [float(num) for num in CO_A_str.split(",")]
                logger.info('CO_A  = {0}'.format(self.CO_A))
                # バイアス補正のバージョン
                self.CO2_VER = config_ini['BIAS']['CO2_VER']
                logger.info('CO2_VER              = {0}'.format(self.CO2_VER))
                self.CH4_VER = config_ini['BIAS']['CH4_VER']
                logger.info('CH4_VER              = {0}'.format(self.CH4_VER))
                self.CO_VER = config_ini['BIAS']['CO_VER']
                logger.info('CO_VER               = {0}'.format(self.CO_VER))
                # バイアス補正パラメータ個数
                self.CO2_X_NUM   = int(config_ini['BIAS']['CO2_X_NUM'])
                logger.info('CO2_X_NUM            = {0}'.format(self.CO2_X_NUM))
                self.CH4_X_NUM   = int(config_ini['BIAS']['CH4_X_NUM'])
                logger.info('CH4_X_NUM            = {0}'.format(self.CH4_X_NUM))
                self.CO_X_NUM   = int(config_ini['BIAS']['CO_X_NUM'])
                logger.info('CO_X_NUM             = {0}'.format(self.CO_X_NUM))
                # バイアス補正パラメータのデータセットパス
                CO2_X_str = config_ini['BIAS']['CO2_X']
                # 正規表現でダブルクォーテーションで囲まれた部分を抽出
                self.CO2_X = re.findall(r'"([^"]*)"', CO2_X_str)
                logger.info('CO2_X                = {0}'.format(self.CO2_X))
                CH4_X_str = config_ini['BIAS']['CH4_X']
                self.CH4_X = re.findall(r'"([^"]*)"', CH4_X_str)
                logger.info('CH4_X                = {0}'.format(self.CH4_X))
                CO_X_str  = config_ini['BIAS']['CO_X']
                self.CO_X  = re.findall(r'"([^"]*)"', CO_X_str)
                logger.info('CO_X                 = {0}'.format(self.CO_X))
                # バイアス補正パラメータ算出式
                CO2_X_CAL_str = config_ini['BIAS']['CO2_X_CAL']
                self.CO2_X_CAL = [xcal for xcal in CO2_X_CAL_str.split(",")]
                logger.info('CO2_X_CAL  = {0}'.format(CO2_X_CAL_str))
                CH4_X_CAL_str = config_ini['BIAS']['CH4_X_CAL']
                self.CH4_X_CAL = [xcal for xcal in CH4_X_CAL_str.split(",")]
                logger.info('CH4_X_CAL  = {0}'.format(CH4_X_CAL_str))
                CO_X_CAL_str  = config_ini['BIAS']['CO_X_CAL']
                self.CO_X_CAL  = [xcal for xcal in CO_X_CAL_str.split(",")]
                logger.info('CO_X_CAL  = {0}'.format(CO_X_CAL_str))

                # 補正係数の変更日付
                self.CHANGE_COEF_DATE = config_ini['BIAS']['CHANGE_COEF_DATE']
                logger.info('CHANGE_COEF_DATE = {0}'.format(self.CHANGE_COEF_DATE))
                # 変更後補正係数
                CO2_A2_str = config_ini['BIAS']['CO2_A2']
                self.CO2_A2 = [float(num) for num in CO2_A2_str.split(",")]
                logger.info('CO2_A2  = {0}'.format(self.CO2_A2))
                CH4_A2_str = config_ini['BIAS']['CH4_A2']
                self.CH4_A2 = [float(num) for num in CH4_A2_str.split(",")]
                logger.info('CH4_A2  = {0}'.format(self.CH4_A2))
                CO_A2_str  = config_ini['BIAS']['CO_A2']
                self.CO_A2  = [float(num) for num in CO_A2_str.split(",")]
                logger.info('CO_A2  = {0}'.format(self.CO_A2))


            else:
                logger.info('**BIAS補正なし**')

            logger.info('----[全制御データ読み込み完了]----')
            
            logger.info('==========================================================')
            if self.REEXEFLG == 1:
                logger.info('<複数処理パターン>')

            if self.SWFP_CO2 + self.SWFP_CH4 + self.SWFP_CO > 0:
                logger.info(' - SWFP期間：%s ~ %s' %(self.BEGINDATE_FP, self.ENDDATE_FP))
                
            if self.SWPR_CH4 + self.SWPR_CO + self.SWPR_SIF > 0:
                logger.info(' - SWPR期間：%s ~ %s' %(self.BEGINDATE_PR, self.ENDDATE_PR))
            
            logger.info(' - 期間内のプロダクトファイルを %d 月刻みでマップ化' %self.TIMEAVEID)
            logger.info('==========================================================')
    
        except KeyError as e:
            print('制御データ読み込みキーエラー')
            print(e)
            logger.error('制御データ読み込みキーエラー: 制御データファイルの[]内文字を確認してください')
            sys.exit(1)

    ##@brief ファイル存在確認
    ##@param [in] checkfile_or_dir 確認ファイルもしくはディレクトリ名
    ##@return True：存在する  False：存在しない
    def Check_File_Exist(self, checkfile_or_dir):
        import os
        return os.path.exists(checkfile_or_dir)
    
    
    ##@brief 入力パラメータの範囲チェック
    ##@return True：異常なし  False：異常あり
    def Check_sysin(self):
        ret = True
        if self.SWFP_CH4 < 0 or self.SWFP_CH4 > 1:
            logger.error('**制御データ範囲エラー** [SWFP_CH4:{}]'.format(self.SWFP_CH4))
            ret = False

        if self.SWFP_CO < 0 or self.SWFP_CO > 1:
            logger.error('**制御データ範囲エラー** [SWFP_CO:{}]'.format(self.SWFP_CO))
            ret = False

        if self.SWFP_CO2 < 0 or self.SWFP_CO2 > 1:
            logger.error('**制御データ範囲エラー** [SWFP_CO2:{}]'.format(self.SWFP_CO2))
            ret = False

        if len(self.BEGINDATE_FP) != 8:
            logger.error('**制御データ文字数エラー** [BEGINDATE_FP:{}]'.format(self.BEGINDATE_FP))
            ret = False

        if len(self.ENDDATE_FP) != 8:
            logger.error('**制御データ文字数エラー** [ENDDATE_FP:{}]'.format(self.ENDDATE_FP))
            ret = False

        if self.COLORID_FPCH4 < 0 or self.COLORID_FPCH4 > 10:
            logger.error('**制御データ範囲エラー** [COLORID_FPCH4:{}]'.format(self.COLORID_FPCH4))
            ret = False

        if self.MAPRNG_FPCH4 < 1 or self.MAPRNG_FPCH4 > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_FPCH4:{}]'.format(self.MAPRNG_FPCH4))
            ret = False

        if self.COLORID_FPCO < 0 or self.COLORID_FPCO > 10:
            logger.error('**制御データ範囲エラー** [COLORID_FPCO:{}]'.format(self.COLORID_FPCO))
            ret = False

        if self.MAPRNG_FPCO < 1 or self.MAPRNG_FPCO > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_FPCO:{}]'.format(self.MAPRNG_FPCO))
            ret = False

        if self.COLORID_FPCO2 < 0 or self.COLORID_FPCO2 > 10:
            logger.error('**制御データ範囲エラー** [COLORID_FPCO2:{}]'.format(self.COLORID_FPCO2))
            ret = False

        if self.MAPRNG_FPCO2 < 1 or self.MAPRNG_FPCO2 > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_FPCO2:{}]'.format(self.MAPRNG_FPCO2))
            ret = False
            
        if self.TIMEAVEID < 1 or self.TIMEAVEID > 3:
            logger.error('**制御データ範囲エラー** [TIMEAVEID:{}]'.format(self.TIMEAVEID))
            ret = False

        if 360.0 % self.SPACIALSTEP != 0.0:
            logger.error('**空間平均ステップ値エラー** [SPACIALSTEP:{}] 180.0を割り切れる値を設定し直してください。'.format(self.SPACIALSTEP))
            ret = False
        
        
        if self.SWFP_CH4 + self.SWFP_CO2 + self.SWFP_CO != 0:
            if self.Check_File_Exist(self.PRODFILEPATH_SWFP) == False:
                logger.error('**SWFP出力指定にもかかわらず、{}のパスが存在しません** [PRODFILEPATH_SWFP]'.format(self.PRODFILEPATH_SWFP))
                ret = False
        
        if self.SWPR_CH4 + self.SWPR_CO + self.SWPR_SIF != 0:
            if self.Check_File_Exist(self.PRODFILEPATH_SWPR) == False:
                logger.error('**SWPR出力指定にもかかわらず、{}のパスが存在しません** [PRODFILEPATH_SWPR]'.format(self.PRODFILEPATH_SWPR))
                ret = False
            
        if self.Check_File_Exist(self.IMGPATH) == False:
            logger.error('**{}のパスが存在しません** [IMGPATH]'.format(self.IMGPATH))
            ret = False

        if self.SWPR_CH4 < 0 or self.SWPR_CH4 > 1:
            logger.error('**制御データ範囲エラー** [SWPR_CH4:{}]'.format(self.SWPR_CH4))
            ret = False

        if self.SWPR_CO < 0 or self.SWPR_CO > 1:
            logger.error('**制御データ範囲エラー** [SWPR_CO:{}]'.format(self.SWPR_CO))
            ret = False

        if self.SWPR_SIF < 0 or self.SWPR_SIF > 1:
            logger.error('**制御データ範囲エラー** [SWPR_SIF:{}]'.format(self.SWPR_SIF))
            ret = False

        if len(self.BEGINDATE_PR) != 8:
            logger.error('**制御データ文字数エラー** [BEGINDATE_PR:{}]'.format(self.BEGINDATE_PR))
            ret = False

        if len(self.ENDDATE_PR) != 8:
            logger.error('**制御データ文字数エラー** [ENDDATE_PR:{}]'.format(self.ENDDATE_PR))
            ret = False

        if self.COLORID_PRCH4 < 0 or self.COLORID_PRCH4 > 10:
            logger.error('**制御データ範囲エラー** [COLORID_PRCH4:{}]'.format(self.COLORID_PRCH4))
            ret = False

        if self.MAPRNG_PRCH4 < 1 or self.MAPRNG_PRCH4 > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_PRCH4:{}]'.format(self.MAPRNG_PRCH4))
            ret = False

        if self.COLORID_PRCO < 0 or self.COLORID_PRCO > 10:
            logger.error('**制御データ範囲エラー** [COLORID_PRCO:{}]'.format(self.COLORID_PRCO))
            ret = False

        if self.MAPRNG_PRCO < 1 or self.MAPRNG_PRCO > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_PRCO:{}]'.format(self.MAPRNG_PRCO))
            ret = False

        if self.COLORID_PRSIF < 0 or self.COLORID_PRSIF > 10:
            logger.error('**制御データ範囲エラー** [COLORID_PRSIF:{}]'.format(self.COLORID_PRSIF))
            ret = False

        if self.MAPRNG_PRSIF < 1 or self.MAPRNG_PRSIF > 3:
            logger.error('**制御データ範囲エラー** [MAPRNG_PRSIF:{}]'.format(self.MAPRNG_PRSIF))
            ret = False

        #バイアス用データ設定チェック
        #それぞれのバイアス補正パラメータ設定数と、計算式の個数が整合しているかなどを確認すること
        if self.CO2_X_NUM < 1 or self.CO2_X_NUM > 29:
            logger.error('**制御データ範囲エラー** [CO2_X_NUM:{}]'.format(self.CO2_X_NUM))
            ret = False
        
        if self.CH4_X_NUM < 1 or self.CH4_X_NUM > 29:
            logger.error('**制御データ範囲エラー** [CH4_X_NUM:{}]'.format(self.CH4_X_NUM))
            ret = False

        if self.CO_X_NUM < 1 or self.CO_X_NUM > 29:
            logger.error('**制御データ範囲エラー** [CO_X_NUM:{}]'.format(self.CO_X_NUM))
            ret = False
        
        if len(self.CO2_X) != self.CO2_X_NUM:
            logger.error('**制御データ範囲エラー** [CO2_X設定数:{}]'.format(len(self.CO2_X)))
            ret = False
        
        if len(self.CH4_X) != self.CH4_X_NUM:
            logger.error('**制御データ範囲エラー** [CH4_X設定数:{}]'.format(len(self.CH4_X)))
            ret = False
    
        if len(self.CO_X) != self.CO_X_NUM:
            logger.error('**制御データ範囲エラー** [CO_X設定数:{}]'.format(len(self.CO_X)))
            ret = False

        if len(self.CO2_X_CAL) != self.CO2_X_NUM:
            logger.error('**制御データ範囲エラー** [CO2_X_CAL設定数:{}]'.format(len(self.CO2_X_CAL)))
            ret = False
        
        if len(self.CH4_X_CAL) != self.CH4_X_NUM:
            logger.error('**制御データ範囲エラー** [CH4_X_CAL設定数:{}]'.format(len(self.CH4_X_CAL)))
            ret = False
    
        if len(self.CO_X_CAL) != self.CO_X_NUM:
            logger.error('**制御データ範囲エラー** [CO_X_CAL設定数:{}]'.format(len(self.CO_X_CAL)))
            ret = False

        

            
        if ret != True:
            print('制御データ設定エラー　出力ログファイルを確認してください。')
            
        return ret
        
    ##@brief 始点と終点日付取得
    ##@param [in] fileID ファイルID 
    def GetPeriod(self, fileID):
        if fileID == 'SWPR':
            return self.BEGINDATE_PR, self.ENDDATE_PR
        elif fileID == 'SWFP':
            return self.BEGINDATE_FP, self.ENDDATE_FP
