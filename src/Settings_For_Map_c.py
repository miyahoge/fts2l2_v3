"""
@file Settings_For_Map_c.py
@brief 気体ごとのマップ設定パラメータを指定するモジュール
"""

##@class SetSysin_For_Map
##@brief 各気体マップ作成用データ設定クラス
class SetSysin_For_Map:

    ##@brief クラスの初期化メソッド（コンストラクタ）
    def __init__(self):
        ##マップタイトル
        self.map_title  = ''
        ##カラーID
        self.map_color  = '2'
        ##カラーバーラベル名
        self.cbar_title = ''
        ##カラーバーの最大値
        self.scale_max  = 2.0
        ##カラーバー最小値
        self.scale_min  = 0.0
        ##カラーバー刻み幅
        self.scale_step = 0.25
        ##データ始点日
        self.begin      = ''
        ##データ終点日
        self.end        = ''
    
    ##@brief 気体ごとのマップ設定パラメータを指定
    ##@param [in] mtitle マップタイトル
    ##@param [in] mcolor カラーID
    ##@param [in] cbartitle カラーバーラベル名
    ##@param [in] max カラーバー最大値
    ##@param [in] min カラーバー最小値
    ##@param [in] step カラーバー刻み幅
    ##@param [in] begin データ始点日
    ##@param [in] end データ終点日
    def Set_sysin(self, mtitle, mcolor, cbartitle, max, min, step, begin, end):
        self.map_title = mtitle
        self.map_color = mcolor
        self.cbar_title = cbartitle
        self.scale_max = max
        self.scale_min = min
        self.scale_step = step
        self.begin      = begin
        self.end        = end
