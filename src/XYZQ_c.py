"""
@file XYZQ_c.py
@brief プロダクトから読み込んだデータを編集・気体濃度バイアス補正し、計算用に内部パラメータ設定するモジュール
"""

import numpy as np
# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

import Read_h5 as rh5
import Read_h5_Bias as rh5bias
import Calc_Correct_Param as biasprm
import Bias_Correct as bias

#@class XYZQ
##@brief プロダクトデータ設定クラス
class XYZQ:

    ##@brief クラスの初期化メソッド（コンストラクタ）
    def __init__(self):
        ##撮像中心点経度
        self.X = np.array([])  
        ##撮像中心点緯度
        self.Y = np.array([])
        ##気体濃度または蛍光輝度値
        self.Z = np.array([])  
        ##品質
        self.Q = np.array([])
        ##プロダクトファイル名
        self.file_name = []  
        ##ファイル数
        self.file_num = 0 
        ##ファイルインデックス
        self.file_idx = 0  
        ##ファイルインデックスの始点
        self.start = 0      
        ##データ個数
        self.nSounding = np.array([]) 
        ##視野内陸率
        self.LandFrac = np.array([])   
        ##処理中の気体名称
        self.whoami = ''
        ##ファイルがない月数保存用
        self.month_noexist = 0
        ##バイアス補正パラメータデータセットパス
        self.X_PATH = []
        ##バイアス補正パラメータデータ数
        self.X_NUM = 0
        ##バイアス補正パラメータ計算式
        self.X_CAL = []
        ##バイアス補正係数
        self.A = np.array([])

    ##@brief フォルダ内の全ファイル名を取得
    ##@param [in] fileID プロダクト識別 SWFP or SWPR
    ##@param [in] folder プロダクトフォルダパス
    ##@return ファイル名リスト
    def GetFileNameListFrom_Folder(self, fileID, folder):
        import glob
        filelist = glob.glob(folder + "\*" + fileID + "*.h5")
        return sorted(filelist)  #ファイル名リストをソートして返す

    
    ##@brief 処理始点のファイル名を取得
    ##@param [in] fileID プロダクト識別 SWFP or SWPR
    ##@param [in] folder プロダクトフォルダパス
    ##@return ファイル名(ファイルが無い場合は'none')
    def GetFileNameFrom_Folder(self, fileID, folder):
        import glob
        filelist = glob.glob(folder + "\*" + fileID + "*.h5")
        if len(filelist) == 0:
            return 'none'

        return filelist[self.file_idx]  #ファイル名を返す

    
    ##@brief ファイルリストの日付と数のチェックと範囲外ファイルをリストから削除
    ##@param [in, out] file_list ファイルリスト
    ##@param [in] begin_t 指定開始日付
    ##@param [in] end_t 指定終了日付
    def Remove_OutofDateFiles(self, file_list, file_id, begin_t, end_t):
        for file in self.file_name[:]:
            check_date_t = rh5.Get_Date(file)
            if (0 != self.CheckPeriod(check_date_t, begin_t, end_t)) or ((file_id in file) == False):
                    logger.warn('制御データ指定期間外のファイルが含まれています：{}'\
                        .format(str(check_date_t.year) + '年' + str(check_date_t.month) + '月' + str(check_date_t.day) + '日'))
                    file_list.remove(file)
    
    ##@brief プロダクトファイルの共通部のデータを抽出
    ##@param [in] sysin  制御データクラス
    ##@param [in] fileID プロダクト識別 SWFP or SWPR
    ##@param [in] file_folder プロダクトフォルダパス
    ##@param [in] begin_t 処理始点
    ##@param [in] end_t 処理終点
    ##@return ERR = 0：正常, -1：FILE_OPEN_ERROR, 1~12：取得できなかった月
    ##@return file_idx ファイルリストインデックス
    ##@return calcbegin_t 計算開始日付
    ##@return calcend_t 計算終了日付
    def Input_common(self, sysin, fileID, file_folder, begin_t, end_t):

        from datetime import date
        from datetime import datetime as dtm
        from Get_Reexe_Num import monthdelta

        nSounding = np.array([])

        #計算始点と終点用datetimeを初期化
        string_date = '2000/01/01'
        # string to datetime
        calcbegin_t = dtm.strptime(string_date, '%Y/%m/%d')
        calcend_t   = dtm.strptime(string_date, '%Y/%m/%d')
        date_t      = dtm.strptime(string_date, '%Y/%m/%d')
        date_save   = dtm.strptime(string_date, '%Y/%m/%d')
        #エラーフラグ0
        ERR = 0

        self.file_name = self.GetFileNameListFrom_Folder(fileID, file_folder)
        #ファイルリストの期間外ファイルを削除
        self.Remove_OutofDateFiles(self.file_name, fileID, begin_t, end_t)
        self.file_num  = len(self.file_name) #読み込みプロダクト数
        if self.file_num == 0:
            logger.warn('FILE_OPEN_ERROR：読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format(fileID))
            print('読み込み可能なプロダクトファイルが指定フォルダに存在しません : {}'.format(fileID))
            return ERR, self.file_idx, calcbegin_t, calcend_t

        fst_flg     = 1    #初回フラグ
        month_save  = 0    #取得プロダクト内の月保存用
        month_delta = 0
        m_cnt       = 1    #月替りカウンタ

        #メンバ変数の初期化
        self.X = np.array([])
        self.Y = np.array([])
        self.Z = np.array([])
        self.Q = np.array([])
        self.LandFrac  = np.array([])
        self.nSounding = np.array([])

        #指定期間のファイルが無くなった場合(再処理の1ヶ月平均で期間内月ファイルが無かった場合等)
        if self.file_idx > self.file_num - 1:
            ERR = self.month_noexist

        else:
            self.LandFrac  = []
            self.nSounding = []
            for file in self.file_name[self.file_idx:]:
                tmp_lat = []  #毎回初期化
                tmp_lon = []
                land_fraction = []
                #共通ヘッダから年月、観測点数、観測中心点緯度経度を取得
                tmp_nSounding ,date_t = rh5.read_h5_common(file, tmp_lat, tmp_lon, land_fraction)
                if tmp_nSounding == 0:
                    logger.warn('データ個数0のファイル：{}'.format(self.file_name[self.file_idx]))

                if fst_flg == 1:  #初回か？
                    calcbegin_t    = date_t
                else:
                    d1 = date_save.replace(day=1)
                    d2 = date_t.replace(day=1)
                    month_delta = monthdelta(d1, d2) - 1

                #月の変わり目？
                m_cnt = m_cnt + month_delta
                if month_delta == 1:
                    #時間範囲は指定期間外？
                    if int(sysin.TIMEAVEID) < m_cnt:
                        #1日戻す
                        date_t = date_save
                        break
                elif month_delta > 1: #月が飛ばされた場合
                    if int(sysin.TIMEAVEID) == 1:  #1ヶ月平均なら続ける
                        self.month_noexist = month_save + 1
                        #1日戻す
                        date_t = date_save
                        break
                    else:                           #2ヶ月以上なら終了
                        ERR = month_save + 1
                        break


                print('読み込み日付：{}'.format(date(date_t.year, date_t.month, date_t.day)))        
                self.Y = np.append(self.Y, np.array(tmp_lat))
                self.X = np.append(self.X, np.array(tmp_lon))
                self.X = np.where(self.X == 180.0, -180.0, self.X)  #180.0度ぴったりは-180.0度に変換
                self.LandFrac = np.append(self.LandFrac, np.array(land_fraction))
                self.nSounding = np.append(nSounding, tmp_nSounding)
                fst_flg = 0    #初回フラグOFF
                #ファイルインデックスをインクリメント
                self.file_idx = self.file_idx + 1
                month_save = date_t.month
                date_save  = date_t

        calcend_t = date_t
        return ERR, self.file_idx, calcbegin_t, calcend_t

    ##@brief 全域分のデータ設定
    ##@param [in] prod プロダクト識別 SWFP or SWPR
    ##@param [in] file_idx ファイル番号
    ##@param [in] id 気体識別ID
    def Set_ProdData(self, prod, file_idx, id):
        end = file_idx
        for file in self.file_name[self.start:end]:   #計算対象全ファイル分のデータを1次元配列として入手
            ppm  = []  #毎回初期化
            qflg = []

            if prod == 'SWPR':
                self.whoami = rh5.read_h5_air_pr(file, id, ppm, qflg)
            elif prod == 'SWFP':
                self.whoami = rh5.read_h5_air_fp(file, id, ppm, qflg)
            
            self.Q = np.append(self.Q, np.array(qflg))
            self.Z = np.append(self.Z, np.array(ppm))

        self.start = end    #最後のインデックスを指定
        #品質フラグが0以外は不使用
        self.Z = np.delete(self.Z, np.where(self.Q != 0)[0])
        self.X = np.delete(self.X, np.where(self.Q != 0)[0])
        self.Y = np.delete(self.Y, np.where(self.Q != 0)[0])
        self.LandFrac = np.delete(self.LandFrac, np.where(self.Q != 0)[0])

    ##@brief 全域分のデータ設定(バイアス補正あり)
    ##@param [in] prod プロダクト識別 SWFP or SWPR
    ##@param [in] file_idx ファイル番号
    ##@param [in] id 気体識別ID
    def Set_ProdData_Bias(self, file_idx, id):
        end = file_idx
        for file in self.file_name[self.start:end]:   #計算対象全ファイル分のデータを1次元配列として入手
            ppm  = []  #毎回初期化
            qflg = []
            #SWFPのみ
            self.whoami = rh5.read_h5_air_fp(file, id, ppm, qflg)
            self.Q = np.append(self.Q, np.array(qflg))
            # 一時変数に濃度データをnumpy変換して格納
            Z_tmp = np.array(ppm)
            # バイアス補正パラメータ計算元データセット取得
            BiasParam_DatSet = rh5bias.Read_Bias_Param(self.X_PATH, self.X_NUM, file)
            # バイアス補正パラメータ計算
            BiasParam = biasprm.Calc_Correct_Pram(self.X_NUM, self.X_CAL, BiasParam_DatSet)
            # バイアス補正実施
            Corrected_Z = bias.Bias_Correct(Z_tmp, self.A, BiasParam)
            # 補正後の濃度をZに格納 Corrected_Zはnumpyに自動変換
            self.Z = np.append(self.Z, Corrected_Z)

        self.start = end    #最後のインデックスを指定
        #品質フラグが0以外は不使用
        self.Z = np.delete(self.Z, np.where(self.Q != 0)[0])
        self.X = np.delete(self.X, np.where(self.Q != 0)[0])
        self.Y = np.delete(self.Y, np.where(self.Q != 0)[0])
        self.LandFrac = np.delete(self.LandFrac, np.where(self.Q != 0)[0])
                
    
    ##@brief 陸域のみの描画時の設定
    ##@param [in] threshold しきい値　10.0%
    ##@return しきい値未満の個数
    def Set_byLandFraction_Land(self, threshold):

        #陸率がしきい値以上で陸域と判断する（しきい値より小を削除）
        self.Z = np.delete(self.Z, np.where(self.LandFrac < threshold)[0])
        self.X = np.delete(self.X, np.where(self.LandFrac < threshold)[0])
        self.Y = np.delete(self.Y, np.where(self.LandFrac < threshold)[0])

        return sum([i > threshold for i in self.LandFrac])

    ##@brief 海域のみの描画時の設定
    ##@param [in] threshold しきい値　10.0%
    ##@return しきい値以上の個数
    def Set_byLandFraction_Sea(self, threshold):

        #陸率がしきい値以下で海域と判断する（しきい値以上を削除）
        self.Z = np.delete(self.Z, np.where(self.LandFrac >= threshold)[0])
        self.X = np.delete(self.X, np.where(self.LandFrac >= threshold)[0])
        self.Y = np.delete(self.Y, np.where(self.LandFrac >= threshold)[0])
        
        return sum([i < threshold for i in self.LandFrac])
    
    ##@brief ファイルデータ取得判定
    ##@return True:取得あり, False:取得なし  
    def IsGetInfo(self):
        if self.X.size != 0:
            return True
        else:
            return False

    ##@brief プロダクトファイルから取得したデータを取得
    def GetData(self):
        return self.X, self.Y, self.Z, self.Q, self.LandFrac, self.whoami

    ##@brief 入力日付が始点終点期間内であるかを確認する
    ##@param [in] date_t チェック対象日付
    ##@param [in] begin_t 期間始点
    ##@param [in] end_t 期間終点
    ##@return -1 : 期間外　0：期間内
    def CheckPeriod(self, date_t, begin_t, end_t):
        from datetime import date
        #指定の期間内ではない場合
        if (date(date_t.year, date_t.month, date_t.day) < date(begin_t.year, begin_t.month, begin_t.day)) or \
            (date(date_t.year, date_t.month, date_t.day) > date(end_t.year, end_t.month, end_t.day)):
            return -1
        else:
            return 0
    
    ##@brief バイアス補正関連パラメータの設定
    ##@param [in] x_path バイアス補正パラメータデータセットパス
    ##@param [in] x_num バイアス補正パラメータの数
    ##@param [in] x_cal バイアス補正パラメータ計算式
    ##@param [in] A バイアス補正係数
    def SetBiasSysin(self, x_path, x_num, x_cal, A):
        self.X_PATH = x_path
        self.X_NUM = x_num
        self.X_CAL = x_cal
        self.A = np.array(A)  #numpy配列に変換して代入