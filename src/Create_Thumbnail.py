"""
@file Create_Thumbnail.py
@brief 作成画像ファイルをデータ圧縮し、縮小してサムネイル画像を作成するモジュール
"""

# ログのライブラリ
from logging import getLogger

## main.pyで宣言したloggerの子loggerオブジェクトの宣言
logger = getLogger("Log").getChild("sub")


##@brief 作成画像ファイルをデータ圧縮し、縮小してサムネイル画像を作成する
##@param [in] sysin  制御データクラス
def CreateThumbnail(sysin):

    import os
    import glob
    from PIL import Image

    #指定フォルダのjpegファイル一覧を取得
    files = glob.glob(sysin.IMGPATH + '\*tmp.png')
    if len(files) == 0:
        logger.warn('画像ファイルが1つも存在しません。')
        return

    wsize = 250  #サムネイルサイズ(横)pixcel
    cbar_img = sysin.IMGPATH + '\\cbar_tmp.png'
    #ファイル一覧をループ
    for f in files:

      img = Image.open(f)

      #
      #=========================
      #サムネイル画像作成      =
      #=========================
      #

      #指定幅からリサイズレートを算出
      rate = wsize / img.width
      #リサイズレートから高さを算出
      hsize = int(img.height * rate)
      #リサイズ実行
      img_resize = img.resize((wsize, hsize))
      thumbfname = f[:-8] + '_thumb.png'
      #リサイズ画像を指定ファイル名で保存
      img_resize.save(thumbfname, dpi =(96, 96))

      #
      #=========================
      #メイン画像のデータ圧縮  =
      #=========================
      #
      comp_img  = f[:-8] + '.png'
      img.save(comp_img, compress_level=9, dpi=(96, 96))

      #圧縮前のtmp画像は削除
      os.remove(f)
