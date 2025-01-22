"""
@file Read_h5.py
@brief HDF5形式のプロダクトデータファイルから、各データを読み込むモジュール
"""
import h5py
import numpy as np
from datetime import datetime

##@brief HDF5形式ファイルを読み込み、日付を取得
##@param [in]  h5path HDF5ファイルパス
def Get_Date(h5path):


    with h5py.File(h5path,'r') as f:
        date_tmp = f['Metadata']['startDate'][()]
        dt = datetime.strptime(date_tmp[0][:10].decode(), '%Y-%m-%d')

    return dt


##@brief HDF5形式ファイルを読み込み、観測点数、撮像中心緯度・経度、視野内陸率を取得
##@param [in]  h5path HDF5ファイルパス
##@param [out] lat_center_arr 撮像中心点緯度リスト
##@param [out] lon_center_arr 撮像中心点経度リスト
##@param [out] land_fraction 視野内陸率リスト
##@note lat_center_arr, lon_center_arr,land_fractionはLISTタイプ
##@return 観測点数, 観測日付
def read_h5_common(h5path, lat_center_arr, lon_center_arr, land_fraction):
    

    # with構文はインデントブロックが終わると自動でファイルクローズしてくれるので便利
    with h5py.File(h5path,'r') as f:

        nSounding = int(f['SceneAttribute']['numSounding'][()][0])  #観測点数


        lat_center_arr.append(f['SoundingGeometry']['latitude'][()])      #撮像中心点緯度
        lon_center_arr.append(f['SoundingGeometry']['longitude'][()])     #撮像中心点経度
        land_fraction.append(f['SoundingGeometry']['landFraction'][()])   #視野内陸率

        date_tmp = f['Metadata']['startDate'][()]
        dt = datetime.strptime(date_tmp[0][:10].decode(), '%Y-%m-%d')

    return nSounding, dt


##@brief SWPRプロダクトのHDF5形式ファイルを読み込み、気体濃度、品質を取得
##@param [in]  h5path HDF5ファイルパス
##@param [in]  id 気体識別　id=0:CH4, id=1:CO, id=2:SIF
##@param [out] data_arr 濃度抽出結果np配列
##@param [out] quality_arr 品質抽出結果np配列
##@return 気体等名称
def read_h5_air_pr(h5path, id, data_arr, quality_arr):

    # with構文はインデントブロックが終わると自動でファイルクローズしてくれるので便利
    with h5py.File(h5path,'r') as f:

        #data_list = list(f)
        #print(data_list)
        if id == 0:
            data_arr.append(f['GasColumn_Proxy']['XCH4_proxy'][()])
            quality_arr.append(f['GasColumn_Proxy']['XCH4_proxy_quality_flag'][()])
            return 'CH4'
        elif id == 1:
            data_arr.append(f['GasColumn_Proxy']['XCO_proxy'][()])
            quality_arr.append(f['GasColumn_Proxy']['XCO_proxy_quality_flag'][()])
            return 'CO'
        elif id == 2:
            data_arr.append(f['SolarInducedFluorescence']['SIF'][()])
            quality_arr.append(f['SolarInducedFluorescence']['SIF_quality_flag'][()])
            return 'SIF'

##@brief SWFPプロダクトのHDF5形式ファイルを読み込み、気体濃度、品質を取得
##@param [in]  h5path HDF5ファイルパス
##@param [in]  id 気体識別　id=0:CO2, id=1:CH4, id=2:CO
##@param [out] data_arr 濃度抽出結果np配列
##@param [out] quality_arr 品質抽出結果np配列
##@return 気体等名称
# ファイルパス、ID、濃度、品質
def read_h5_air_fp(h5path, id, data_arr, quality_arr):

    # with構文はインデントブロックが終わると自動でファイルクローズしてくれるので便利
    with h5py.File(h5path,'r') as f:

        if id == 0:   #CO2データ入力
            data_arr.append(f['RetrievalResult']['xco2'][()])
            quality_arr.append(f['RetrievalResult']['xco2_quality_flag'][()])
            return 'CO2'
        elif id == 1:
            data_arr.append(f['RetrievalResult']['xch4'][()])
            quality_arr.append(f['RetrievalResult']['xch4_quality_flag'][()])
            return 'CH4'
        elif id == 2:
            data_arr.append(f['RetrievalResult']['xco'][()])
            quality_arr.append(f['RetrievalResult']['xco_quality_flag'][()])
            return 'CO'