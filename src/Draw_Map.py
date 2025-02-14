"""
@file Draw_Map.py
@brief 地図データとグリッドデータからマップを作成するモジュール
"""

##@brief 画像設定、地図の描画、濃度データのプロットを実施
##@param [in] sysin  制御データクラス
##@param [in] air_sysin 気体ごと制御データセットクラス
##@param [in] begin 計算始点
##@param [in] end 計算終点
##@param [in] grid グリッドデータ
##@param [in] data_ver 日付、バージョン情報
##@param [in] myid 気体等名称
##@param [in] is_swfp SWFPの時にTrueとしてBIAS_FLAGの判定をする. SWPRの場合は初期値でFalseが設定される.
def Draw_Map(sysin, air_sysin, begin, end, grid, data_ver, myid, is_swfp=False):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from matplotlib.ticker import AutoMinorLocator
    #フォントはIPAexGothicに固定
    plt.rcParams["font.family"] = "IPAexGothic"
    
    extent = [-180., 180., -90., 90.]
    mydpi  = 96  #dpi設定
    fig = plt.figure(figsize=(4528/mydpi, 2362/mydpi), dpi = mydpi)
    plt.rcParams["xtick.minor.visible"] = True     #x軸補助目盛りの追加
    plt.rcParams["ytick.minor.visible"] = True     #y軸補助目盛りの追加
    plt.rcParams["axes.linewidth"]      = 4.0      #図の枠線の太さ
    #plt.rcParams['text.antialiased']    = False     #アンチエイリアス
    plt.subplots_adjust(left=0.06, right=0.9, bottom=0.1, top=0.9)
    #rect = [left, bottom, width, height] 
    ax = plt.axes([0.07, 0.0, 1.03, 1.0], projection=ccrs.PlateCarree(central_longitude=0.))  #経度0度を中心
    ax.tick_params(which = 'both',  # 目盛で囲む
                           right = 'on',
                           top = 'on')
    ax.tick_params(which = 'major',  # 目盛をもう少し長く
                           length = 15,width =4.)
    ax.tick_params(which = 'minor',
                           length = 10,width =2.)
    #目盛のサイズを指定
    ax.axes.tick_params(labelsize=50, top="true")
    # 軸ラベルの設定
    ax.set_xlabel(sysin.XLABEL, size = 50, weight = "light")
    ax.set_ylabel(sysin.YLABEL, size = 50, weight = "light")

    #マップの描画
    #カラー種別設定
    if air_sysin.map_color == 1:
        mapcolor = 'jet'
    #以下は拡張機能としてコメントで残す
    #else:
    #    import GetColorMap
    #    import matplotlib.colors
    #    colors = GetColorMap.GetCM(sysin.CMAPFILE)
    #    mapcolor= matplotlib.colors.ListedColormap(colors) #test['#FFFFFF', '#00FFFF', '#00B0FF', '#0070FF', '#228B22', '#00FF00', '#FFFF00', '#FF8000', '#FF0000', '#FF00FF']

    
    #湖用解像度設定
    lakes_10m = cfeature.NaturalEarthFeature('physical', 'lakes', '10m', 
                                             edgecolor='black',
                                             facecolor='#ffffff00')  #透明
    
    #湖の描画
    ax.add_feature(lakes_10m, lw = 1.5, antialiased = False)
    #10m解像度の海岸線の描画
    ax.coastlines(resolution='10m', lw = 1.5, antialiased = False)

    #濃度平均値を描画
    ax.imshow(grid, extent=extent, cmap=mapcolor, origin='lower', 
              vmin=air_sysin.scale_min, vmax=air_sysin.scale_max)  

    #グリッドと軸目盛を描く緯度経度を設定するための配列
    dlon,dlat=30,30
    xticks=np.arange(-180,180.1,dlon)
    yticks=np.arange(-90,90.1,dlat)
    #目盛を描く緯度経度の値を設定
    ax.set_xticks(xticks,crs=ccrs.PlateCarree())
    ax.set_yticks(yticks,crs=ccrs.PlateCarree())
    
    #補助メモリは3本
    ax.xaxis.set_minor_locator(AutoMinorLocator(3)) 
    ax.yaxis.set_minor_locator(AutoMinorLocator(3))

    #タイトルを設定
    plt.title(air_sysin.map_title, size=60, x=0.5, y=1.06)

    # グラフ右下部にバージョンを表示する
    ax.text(130, -105, begin + '-' + end + ' (V' + data_ver + ')', \
            ha='center', va='bottom', fontsize=40)
    # SWFPかつバイアスフラグONの場合のみグラフ左下部に＜Bais-corrected＞を表示する
    if (is_swfp):
        if (sysin.BIAS_FLAG):
            ax.text(-130, -105, '<Bias-corrected>', \
                    ha='center', va='bottom', fontsize=50)
    
    if myid == 'SIF':
        # SIF場合はマップ上オーストラリアと南極の間にクレジットを表示する
        ax.text( 120, -60, '©JAXA/NIES/MOE', ha='center', va='bottom', fontsize=40)
    else:
        # SIF以外の場合はマップ右下部にクレジットを表示する
        ax.text( 120, -85, '©JAXA/NIES/MOE', ha='center', va='bottom', fontsize=40)

    #カラーバーの設定
    # matplotlib-add-colorbar-to-a-sequence-of-line-plots
    sm = plt.cm.ScalarMappable(cmap=mapcolor, norm=plt.Normalize(vmin=air_sysin.scale_min, vmax=air_sysin.scale_max))
    # Fake up the array of the scalar mappable
    sm._A = []
    
    # Customize colorbar tick labels
    p = (air_sysin.scale_max - air_sysin.scale_min) / air_sysin.scale_step
    num = range(int(p)+1)
    mytks = list(map(lambda j:air_sysin.scale_min + j * air_sysin.scale_step, num))
    mytks.append(air_sysin.scale_max)
    if myid == 'CO2':
        ticklabels = ['{:.0f}'.format(n) for n in mytks]  #CO2のみ小数点以下なしに統一
    else:
        ticklabels = ['{:.2f}'.format(n) for n in mytks]  #小数点以下2桁に統一
    
    cbar = plt.colorbar(sm, ax=ax, alpha=1, shrink=0.8)
    cbar.solids.set_edgecolor("face")
    cbar.set_ticks(mytks)
    cbar.set_ticklabels(ticklabels)

    # Fontsize & pad for colorbar ticklabels
    cbar.ax.tick_params(labelsize = 40, pad = 30)

    # Colorbar label, customize fontsize and distance to colorbar
    cbar.set_label(air_sysin.cbar_title, alpha=1, 
                   rotation=270, fontsize=50, labelpad=77)
    
    caxpos = cbar.ax.get_position() # colorbar自体の座標
    cbar.ax.set_position([ax.get_position().x1 + 0.02, caxpos.y0, 0.2, caxpos.height])

    return plt