#!/usr/bin/env python3

#Readme
#
# $ python3 main.py "画像ファイル名"で動く
#ファイル名：
#           gray.png  ：画像を二次元配列にするためにグレーアウトさせたもの
#           result.png：gray.pngを畳み込んだあとの結果 
#           out.gif   ：変化を見れるgif
#

from PIL import Image
import numpy as np
import time
import sys
import os

filter = np.array([  #係数になるフィルター
    [1.0, 1.0, 1.0],    #フィルターにどんな数字が良いかはわからない。。。
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0]
])

images = []#変更中の画像保存配列
page = 0

imagepath = sys.argv[1]  #コマンドライン引数で画像ファイルパス受け取り
im = np.array(Image.open(imagepath).convert('L'))    #グレースケール画像に変換しつつ、二次元配列に変換
out = Image.fromarray(im) #グレースケール画像に戻して保存
out.save("gray.png")
#im = np.linspace(1, 49, 49).reshape(7, 7)

result = im.copy() #結果が入る動的2次元配列

os.makedirs('tmp', exist_ok=True)

#畳み込み処理:アルゴリズム調べて出てきたやつの、気に入らない箇所直しました。
for index_row in range(1, len(im) - 1):
    for index_line in range(1, len(im[0]) - 1):
        for filter_row in range(-1, len(filter) - 1):
            for filter_line in range(-1, len(filter[0]) - 1):
                #フィルターの左上と画像データの左上を合わせてから1マスずつ元画像を左にずらすイメージ
                result[index_row - 1][index_line - 1] += im[index_row + filter_row][index_line + filter_line] * filter[filter_line + 1][filter_row + 1] / 9 #畳み込み計算の式
                # print(result)   #表示
                # os.system('clear') #コンソールクリア
                
    outputimage = Image.fromarray(np.uint8(result)) #配列を画像に
    outputimage.save(f"tmp/result{page}.png") #結果画像保存
    images.append(outputimage)  #配列imagesに追加
    page += 1 #page インクリメント

outputimage.save('out.gif', save_all = True, append_images=images[0:]) #gifファイル生成
os.system('rm -r ./tmp')

print("\n Result:")                
print(result)   #結果配列出力

outputimage = Image.fromarray(np.uint8(result))
outputimage.save("result.png") #結果画像保存

print("Finish!")