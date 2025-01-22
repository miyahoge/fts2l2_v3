"""
@file Get_Reexe_Num.py
@brief 過去データ再処理実行時の再処理回数を算出するモジュール
"""

import sys
# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")

##@brief 再処理時の繰り返し処理回数を求める
##@param [in] sysin  制御データクラス
##@param [in] begin 始まりの日付
##@param [in] end 終わりの日付
##@return 再処理回数
def Get_Reexe_Num(sysin, begin, end):
    from datetime import datetime
    begin_t = datetime.strptime(begin, '%Y%m%d')
    end_t   = datetime.strptime(end, '%Y%m%d')

    #時間平均期間から
    month_period = monthdelta(begin_t, end_t)
    if month_period % sysin.TIMEAVEID != 0:
        logger.error('時間平均区間と計算範囲が不整合です。')
        sys.exit(1)

    #print('month_period= {}'.format(month_period))
    num = int(month_period / sysin.TIMEAVEID)
    return num

##@brief 月の差分を算出
##@param [in] begin_t 始まりの日付(datetime構造)
##@param [in] end_t 終わりの日付(datetime構造)
##@return 月の差（ヶ月）
def monthdelta(begin_t, end_t):
    import dateutil
    import datetime
    from dateutil.relativedelta import relativedelta

    deltamonth = 1
    while True:
        begin_t = begin_t + relativedelta(months=1)
        if begin_t <= end_t:
            deltamonth += 1
            continue
        break

    return deltamonth