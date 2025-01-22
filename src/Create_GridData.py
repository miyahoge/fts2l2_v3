"""
@file Create_GridData.py
@brief 空間平均幅の格子を作り、撮像中心点座標から格子内の濃度平均値を算出するモジュール
"""

import numpy as np

##@brief 撮像中心点座標から格子内の濃度平均値を算出する
##@param [in] x 撮像中心点経度
##@param [in] y 撮像中心点緯度
##@param [in] z 濃度データ
##@param [in] step グリッドの1辺の度数（空間平均範囲）
##@return グリッドデータ（行列）
##@attention 本モジュールの返り値行列は[緯度, 経度]の順番であるため注意（X(経度),Y(緯度)の順番ではない）
def griddata(x, y, z, step = 2.5):
    # make coordinate arrays.
    xo      = np.arange(-180.0, 180.0, step)
    yo      = np.arange(-90.0, 90.0, step)
    xi, yi  = np.meshgrid(xo,yo)
    
    # make the grid.
    grid       = np.zeros(xi.shape, dtype=x.dtype)
    nrow, ncol = grid.shape
    x_low = np.zeros((nrow, ncol))
    y_low = np.zeros((nrow, ncol))
    x_high = np.zeros((nrow, ncol))
    y_high = np.zeros((nrow, ncol))
    
    # fill in the grid.
    for row in range(nrow):
        for col in range(ncol):
            #グリッドの上限の座標をX,Yそれぞれ求める
            x_high[row, col] = xo[col] + step
            y_high[row, col] = yo[row] + step
            
            posx1 = x - xo[col]           #格子の最小X座標との差
            posy1 = y - yo[row]           #格子の最小Y座標との差
            posx2 = x - x_high[row, col]  #格子の最大X座標との差
            posy2 = y - y_high[row, col]  #格子の最大Y座標との差

            bool1 = np.logical_and(0 <= posx1, 0 > posx2)  #X座標が格子の内側か？
            bool2 = np.logical_and(0 < posy1, 0 >= posy2)  #Y座標が格子の内側か？
            ibin  = np.logical_and(bool1, bool2)
            concentration = z[ibin]        #条件に当てはまる濃度を抽出
            if concentration.size != 0:
                grid[row, col] = np.mean(concentration)    #平均を算出
            else:
                grid[row, col] = np.nan    # 条件一致なしならnanで埋める
    
    # return the grid
    return grid

