import sys
import os

import pyocr
import pyocr.builders
import pyautogui
import cv2

import numpy as np

from PIL import Image
from time import sleep
from discordwebhook import Discord



tools = pyocr.get_available_tools()
discord = Discord(url="https://discord.com/api/webhooks/887696502821105664/CyiKjOX-c8I6BLY2PGmHgJMqLHGgsSEv2zaHsjSQIOITqPGzqAfRblSoqttC-UNHgWSc")
history = ""

if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.

# ↑PyOCR使う時の呪文、おまじない。

# 範囲指定のためのマウスカーソル座標取得関数。メッセージボックスの左上隅と右下隅で囲まれた範囲をスクリーンショット
def PosGet():
    # クリックを検知したらそこの座標を取得　←なんか難しいからやめました
    # 3秒待ってからカーソル位置の座標を取得
    print("左上隅の座標を取得します")
    sleep(3)
    x1, y1 = pyautogui.position()
    print(str(x1) + "," + str(y1))

    # 3秒待ってからカーソル位置の座標を取得
    print("右下隅の座標を取得します")
    sleep(3)
    x2, y2 = pyautogui.position()
    print(str(x2) + "," + str(y2))

    # PyAutoGuiのregionの仕様のため、相対座標を求める
    x2 -= x1
    y2 -= y1

    return(x1, y1, x2, y2)

# スクリーンショット撮影 → グレースケール → 画像を拡大
def ScreenShot(x1, y1, x2, y2):
    sc = pyautogui.screenshot('TransActor.png',region=(x1, y1, x2, y2)) # PosGet関数で取得した座標を使用
    im = Image.open(r"TransActor.png").convert("RGB")
    #ScreenShot(260, 195, 345, 140)
    #ScreenShot(145, 190, 445, 150)
    im.crop((0, 1, 100, 100)).save("TransActor_Avator.png")
    gap = 40
    #im.crop((0, 0, x2, gap)).save("TransActor_User.png")
    user = im.crop((0, 0, x2, gap))
    OptimizeUser(user).save("TransActor_User.png")
    #im.crop((0, gap, x2, y2)).save("TransActor_Comment.png")
    comment = im.crop((0, gap, x2, y2))
    OptimizeComment(comment).save("TransActor_Comment.png")


def OptimizeUser(image):
    border = 105
    arr = np.array(image)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
#            if j < 90:
            if j < 200:
                arr[i][j] = [255,255,255]
            elif pix[0] < border or pix[1] < border or pix [2] < border:
                arr[i][j] = [255,255,255]
            elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
                arr[i][j] = [0,0,0]

    return Image.fromarray(arr)

def OptimizeComment(image):
    border = 130
    arr = np.array(image)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
#            if i < 10 or j < 15 or j > 330:
            if i < 15 or j < 150 or j > 440:
                arr[i][j] = [255,255,255]
            elif pix[0] < border or pix[1] < border or pix [2] < border:
                arr[i][j] = [0,0,0]
            elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
                arr[i][j] = [255,255,255]

    return Image.fromarray(arr)

    #im.save(r"TransActor.jpg")
    # あとは画像拡大してみましょうか グレースケールも有効？ OpenCVにも頼ってみよう
    #img = cv2.imread('TransActor.jpg')
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #th, im_th = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    #th, tmp = cv2.threshold(gray, 128, 192, cv2.THRESH_OTSU)
    #tmp = cv2.resize(gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv2.INTER_LINEAR)
    #tmp = cv2.resize(im_th, (im_th.shape[1]*2, im_th.shape[0]*2), interpolation=cv2.INTER_LINEAR)
    #cv2.imwrite('TransActor.jpg', tmp)

# Image.openメソッドで画像が開かれる。PyOCRで文字認識、文字起こし
# 関数名は翻訳実装の名残
def TranslationActors(img):
    txt = tool.image_to_string(
        Image.open(img),
        lang="jpn",
        builder=pyocr.builders.TextBuilder()
    ) # 英文を読み取る時はlang="eng"
    print(txt)
    return(txt.replace('\n',""))
    #return(txt.replace("ギル",""))

# 読み取る範囲を決める
# x1, y1, x2, y2 = PosGet()

# ギルチャ
# 左上隅の座標を取得します
# x1=142,y1=187
# 右下隅の座標を取得します
# x2=579-142=437,y2=339-187=152
# ScreenShot(260, 187, 347, 140)
# 通常
# 左上隅の座標を取得します
# 13,384
# 右下隅の座標を取得します
# 408,425
#ScreenShot(10, 384, 395, 41)

#ScreenShot(260, 195, 345, 140)

#ScreenShot(145, 190, 445, 150)
#user = TranslationActors("TransActor_User.png")
#comment = TranslationActors("TransActor_Comment.png")
#discord.post(content=comment,username=user)

#post = TranslationActors()

#if history != post:
#    discord.post(content=post)
#    history = post

if __name__ == "__main__":
    while True:
        ScreenShot(145, 190, 445, 150)
    #    ScreenShot(10, 384, 395, 41)
    #    ScreenShot(x1, y1, x2, y2)
        user = TranslationActors("TransActor_User.png")
        comment = TranslationActors("TransActor_Comment.png")

        if (user is not "") and (comment is not "") and (comment != history):
            discord.post(content=comment,username=user)
            history = comment
        sleep(1)                   # 1秒ごとに繰り返す
