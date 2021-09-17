import sys
import pyocr
import pyocr.builders
import pyautogui
import pyperclip
import numpy as np
import dropbox

from subprocess import Popen, PIPE
from time import sleep, time
from PIL import Image
from discordwebhook import Discord

itemlist = [
#	"スモーキーカード",
#	"エクリプスカード",
	"マスターリングカード",
#	"バジルリスクカードカード",
#	"ボーカルカード",
	"ゴーストリングカード",
#	"トードカード",
#	"ロータージャイロカード",
	"ドラゴンフライカード",
#	"さすらい狼カード",
	"ウッドゴブリンカード",
#	"アヌビスカード",
#	"グリフォンカード",
#	"ヒェグンカード",
	"オークベイビーカード",
#	"ジャックカード",
#	"ミュータントドラゴンカード",
#	"ラフレシアカード",
#	"オウルデュークカード",
#	"アリスカード",
#	"ジルタスカード",
#	"ミステルテインカード",
#	"ダークイリュージョンカード",
#	"ひ弱な操り人形カード",
#	"ビッグベンカード",
#	"時計塔管理者カード",
	"チェペットカード",
#	"炎の魔女カード",
#	"パイドパイパーカード",
#	"イグニゼム＝セニアカード",
#	"アルマイア=デュンゼカード",
#	"ロリルリカード",
#	"ゲイズティカード",
	"狂暴化したガリオンカード",
#	"堕ちた大神官ヒバムカード",
#	"妖狐ミョグェカード",
#	"カエデの精霊イシュマカード",
#	"銀魚湖のヌシカード",
#	"火焔鳥ジュリーカード",
#	"リムルカード",
#	"クリスタルビースト",
	"ヴァルキリー・ラーズグリーズカード",
	"アーケインキューブカード",
	"思念集合体カード",
	"魔剣士タナトスカード",
	"エンジェリングカード",
	"レディータニーカード",
	"黄金蟲カード",
	"デビルリングカード",
	"デビルリング★カード",
	"リバースデビルリングカード",
	"ドレイクカード",
	"ドレイク★カード",
	"リバースドレイクカード",
	"ストラウフカード",
	"ストラウフ★カード",
	"リバースストラウフカード",
	"ゴブリンリーダーカード",
	"ゴブリンリーダー★カード",
	"リバースゴブリンリーダーカード",
	"ミストレスカード",
	"ミストレス★カード",
	"リバースミストレスカード",
	"マヤーカード",
	"マヤー★カード",
	"リバースマヤーカード",
	"フリオニカード",
	"フリオニ★カード",
	"リバースフリオニカード",
	"エドガカード",
	"エドガ★カード",
	"リバースエドガカード",
	"オシリスカード",
	"オシリス★カード",
	"リバースオシリスカード",
	"月夜花カード",
	"月夜花★カード",
	"リバース月夜花カード",
	"コボルドリーダーカード",
	"オークヒーローカード",
	"ドッペルゲンガーカード",
	"ドッペルゲンガー★カード",
	"リバースドッペルゲンガーカード",
	"アトロスカード",
	"アトロス★カード",
	"リバースアトロスカード",
	"オークロードカード",
#	"オークロード★カード",
#	"リバースオークロードカード",
	"データルザウルスカード",
	"データルザウルス★カード",
	"リバースデータルザウルスカード",
	"オウルバロンカード",
	"オウルバロン★カード",
	"リバースオウルバロンカード",
	"キメラカード",
	"キメラ★カード",
	"リバースキメラカード",
	"ブラッディナイトカード",
	"ブラッディナイト★カード",
	"リバースブラッディナイトカード",
	"ランドグリスカード",
	"ドラキュラカード",
	"ダークロードカード",
#	"ダークロード★カード",
#	"リバースダークロードカード",
	"バフォメットカード",
	"タイムホルダーカード",
	"タイムホルダー★カード",
	"リバースタイムホルダーカード",
	"ロメロスペシャレカード",
	"ロメロスペシャレ★カード",
	"リバースロメロスペシャレカード",
	"ストームナイトカード",
	"ストームナイト★カード",
	"リバースストームナイトカード",
	"ハティーカード",
	"炎の領主カホカード",
	"炎の領主カホ★カード",
	"リバース炎の領主カホカード",
	"アークエンジェリングカード",
	"ロードオブデスカード",
	"ブラッディマーダーカード",
	"カトリーヌ＝ケイロンカード",
	"セシル＝ディモンカード",
	"エレメス＝ガイルカード",
	"ウルフおばあちゃんカード",
	"クトルラナックスカード",
	"ヒルウィンドカード",
	"グルームアンダーナイトカード",
	"妖蛇ゴルゴーンカード",
	"荒れ地の領主カード",
	"ボイタタカード",
	"アウドムラカード",
	"シードオブイグドラシルカード",
	"魂の奏者カード"
]

# nirvana_rom
discord_url = "https://discord.com/api/webhooks/887696502821105664/CyiKjOX-c8I6BLY2PGmHgJMqLHGgsSEv2zaHsjSQIOITqPGzqAfRblSoqttC-UNHgWSc"
# krbysh
# discord_url = "https://discord.com/api/webhooks/887372286586413098/lDES7A_xl5GVr0ebklUpTV_8rUZvNSB09Hwl6-dLNAoq1nRVzJxIad-yi886mfF0DMPh"
discord_headers = {'Content-Type': 'application/json'}

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

access_token = 'cLCjFHhr-zsAAAAAAAAAAQh1y5kxdh1T_pqAm-kjGISri82aiEFngKpy11gy8fIF'
transferData = TransferData(access_token)

file_from = 'Avatar.png'
file_to = '/Avatar.png'  

dp_url="https://dl.dropboxusercontent.com/s/4ps95y182sbctrp/Avatar.png"

tools = pyocr.get_available_tools()
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

def MarketSearch(Item):
	pyautogui.moveTo(235,225)  # search Window
	pyautogui.click()
	pyautogui.moveTo(735,250)  # inputText Window
	pyautogui.click()

	pyperclip.copy("^"+Item)
	sleep(1)
	pyautogui.hotkey('command','v')
	pyautogui.hotkey('enter')
	pyautogui.moveTo(695,355)  # searchResult Window
	pyautogui.click()

	sleep(1)
	sc = pyautogui.screenshot('MarketResult.png',region=(443, 210, 405, 112))
	im = Image.open(r"MarketResult.png").convert("RGB")
	im.crop((4, 8, 103, 106)).save("Avatar.png")
	price = im.crop((220, 60, 400, 90))
	OptimizePrice(price).save("Price.png")
	time = im.crop((333, 20, 405, 48))
	OptimizeTime(time).save("Time.png")

def OptimizePrice(image):
	border = 170
	arr = np.array(image)
	for i in range(len(arr)):
		for j in range(len(arr[i])):
			pix = arr[i][j]
			if pix[0] < border or pix[1] < border or pix [2] < border:
				arr[i][j] = [0,0,0]
			elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
				arr[i][j] = [255,255,255]

	return Image.fromarray(arr)

def OptimizeTime(image):
	border = 165
	arr = np.array(image)
	for i in range(len(arr)):
		for j in range(len(arr[i])):
			pix = arr[i][j]
			if pix[0] < border or pix[1] < border or pix [2] < border:
				arr[i][j] = [0,0,0]
			elif pix[0] >= border or pix[1] >= border or pix [2] >= border:
				arr[i][j] = [255,255,255]

	return Image.fromarray(arr)

def TranslationActors(img):
	txt = tool.image_to_string(
		Image.open(img),
		lang="eng",
		builder=pyocr.builders.TextBuilder(tesseract_layout=4)
	)
	print(txt.replace("\n",""))
	return(txt)

if __name__ == "__main__":
	p = ""
	t = ""
	discord = Discord(url=discord_url)
	sleep(5)

#	while True:		
	for item in itemlist:
		MarketSearch(item)

		p = TranslationActors("Price.png").replace('.',",")
		t = TranslationActors("Time.png").replace('.|;|-',":")
		
		if p is not "" :
			transferData.upload_file(file_from, file_to)
			sleep(3)

			if t is not "":
				discord.post(content=p + " z @" + t, username=item, avatar_url=dp_url + "?" + str(time()))
			#else:
			#	discord.post(content=p + " z", username=item, avatar_url=dp_url + "?" + str(time()))
#		sleep(3600)