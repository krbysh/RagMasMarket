import sys
import pyocr
import pyocr.builders
import pyautogui
import numpy as np
import time
import dropbox
import requests
import json

from PIL import Image
from time import sleep

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

tools = pyocr.get_available_tools()
# nirvana_rom
discord_url="https://discord.com/api/webhooks/887696502821105664/CyiKjOX-c8I6BLY2PGmHgJMqLHGgsSEv2zaHsjSQIOITqPGzqAfRblSoqttC-UNHgWSc"
# krbysh
# discord_url="https://discord.com/api/webhooks/887372286586413098/lDES7A_xl5GVr0ebklUpTV_8rUZvNSB09Hwl6-dLNAoq1nRVzJxIad-yi886mfF0DMPh"
discord_headers = {'Content-Type': 'application/json'}

access_token = 'cLCjFHhr-zsAAAAAAAAAAQh1y5kxdh1T_pqAm-kjGISri82aiEFngKpy11gy8fIF'
transferData = TransferData(access_token)

file_from = 'Avatar.png'
file_to = '/Avatar.png'  

dp_url="https://dl.dropboxusercontent.com/s/4ps95y182sbctrp/Avatar.png"

if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))

def PosGet():
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

def ScreenShot(x1, y1, x2, y2):
    sc = pyautogui.screenshot('Origin.png',region=(x1, y1, x2, y2)) # PosGet関数で取得した座標を使用
    im = Image.open(r"Origin.png").convert("RGB")
    im.crop((0, 1, 100, 100)).save("Avatar.png")
    gap = 40
    user = im.crop((0, 0, x2, gap))
    OptimizeUser(user).save("User.png")
    comment = im.crop((0, gap, x2, y2))
    OptimizeComment(comment).save("Comment.png")


def OptimizeUser(image):
    border = 100
    arr = np.array(image)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
            if j < 200:
                arr[i][j] = [255,255,255]
            elif pix[0] < border or pix[1] < border or pix [2] < border:
                arr[i][j] = [255,255,255]
            elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
                arr[i][j] = [0,0,0]

    return Image.fromarray(arr)

def OptimizeComment(image):
    border = 150
    arr = np.array(image)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
            if i < 15 or j < 150 or j > 440:
                arr[i][j] = [255,255,255]
            elif pix[0] < border or pix[1] < border or pix [2] < border:
                arr[i][j] = [0,0,0]
            elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
                arr[i][j] = [255,255,255]

    return Image.fromarray(arr)

def TranslationActors(img):
    txt = tool.image_to_string(
        Image.open(img),
        lang="jpn",
        builder=pyocr.builders.TextBuilder()
    )
    print(txt)
    return(txt.replace('\n',""))

# 読み取る範囲を決める
# x1, y1, x2, y2 = PosGet()

if __name__ == "__main__":
    comment_history = ""
    user_history = ""
    while True:
        ScreenShot(145, 190, 445, 150)

        user = TranslationActors("User.png")
        comment = TranslationActors("Comment.png")

        if (user is not "") and (comment is not "") and (comment != comment_history):
            if user is not user_history:
                transferData.upload_file(file_from, file_to)
                sleep(3)
            discord_contents = {
                'content': comment,
                'avatar_url': dp_url + "?" + str(time.time()),
                'username': user
            }
            requests.post(discord_url, json.dumps(discord_contents), headers=discord_headers)
            comment_history = comment
            user_histtory = user
        sleep(1)