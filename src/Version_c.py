"""
@file Version_c.py
@brief プロダクトファイル共通部から日付とバージョン情報を取得するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

##@class Version
##@brief プロダクトファイル共通部から日付とバージョン情報を取得するクラス
class Version:

    ##@brief クラスの初期化メソッド（コンストラクタ）
    def __init__(self):
        ##バージョン
        self.ver  = ''

    ##@brief 抽出したデータからマップに記載する文字列に変換してクラスのメンバ変数に設定
    ##@param [in] folder プロダクトフォルダパス
    ##@param [in] XYZQ プロダクトデータ設定クラス
    ##@param [in] fileID プロダクト識別 SWFP or SWPR
    def Set_Version(self, folder, XYZQ, fileID):
        from datetime import datetime
        import h5py
        fname = XYZQ.GetFileNameFrom_Folder(fileID, folder)
        if fname == 'none':  #ファイルが存在しない場合は設定無し
            self.ver = 'none'
            return
    
        # バージョンを取得
        with h5py.File(fname, 'r') as f:  #処理始めのファイルのデータを取得
            ver_tmp  = f['Metadata']['productVersion'][()][0]

            ver_prim = ver_tmp[:2].decode()
            ver_sub  = ver_tmp[2:5].decode()
            self.ver = ver_prim + '.' + ver_sub
    
    ##@brief メンバ変数に設定された文字列を取得する
    def Get_Version(self):
        return self.ver



