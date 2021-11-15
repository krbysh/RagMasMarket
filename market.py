#!/usr/bin/env python3
# condig: utf-8

import sys
import pyocr
import pyocr.builders
import pyautogui
import pyperclip
import numpy as np
import os
import tweepy

from subprocess import Popen, PIPE
from time import sleep, time
from PIL import Image
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

itemlist = [
	"ヴァルキリー・ラーズグリーズカード",
	"アーケインキューブカード",
	"思念集合体カード",
	"魔剣士タナトスカード",
	"骸龍カード",
	"怨霊武士カード",
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
	"オークロード★カード",
	"リバースオークロードカード",
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
	"ダークロード★カード",
	"リバースダークロードカード",
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
	"カトリーヌ・ケイロン（MVP）カード",
	"セシル・ディモン（MVP）カード",
	"エレメス・ガイル（MVP）カード",
	"ウルフおばあちゃんカード",
	"クトルラナックスカード",
	"ヒルウィンドカード",
	"グルームアンダーナイトカード",
	"妖蛇ゴルゴーンカード",
	"荒れ地の領主カード",
	"ボイタタカード",
	"アウドムラカード",
	"シードオブイグドラシルカード",
	"魂の奏者カード",
	"タオグンカカード",
	"クラーケンカード",
	"スモーキーカード",
	"エクリプスカード",
	"エクリプス★カード",
	"マスターリングカード",
	"マスターリング★カード",
	"バジルリスクカード",
	"ボーカルカード",
	"ゴーストリングカード",
	"トードカード",
	"トード★カード",
	"ロータージャイロカード",
	"ロータージャイロ★カード",
	"ドラゴンフライカード",
	"ドラゴンフライ★カード",
	"さすらい狼カード",
	"さすらい狼★カード",
	"ウッドゴブリンカード",
	"ウッドゴブリン★カード",
	"アヌビスカード",
	"アヌビス★カード",
	"グリフォンカード",
	"グリフォン★カード",
	"ヒェグンカード",
	"ヒェグン★カード",
	"オークベイビーカード",
	"ジャックカード",
	"ミュータントドラゴンカード",
	"ミュータントドラゴン★カード",
	"ラフレシアカード",
	"ラフレシア★カード",
	"オウルデュークカード",
	"アリスカード",
	"アリス★カード",
	"ジルタスカード",
	"ミステルテインカード",
	"ミステルテイン★カード",
	"ダークイリュージョンカード",
	"ダークイリュージョン★カード",
	"ビッグベンカード",
	"時計塔管理者カード",
	"時計塔管理者★カード",
	"チェペットカード",
	"炎の魔女カード",
	"炎の魔女★カード",
	"パイドパイパーカード",
	"イグニゼム・セニア（MINI）カード",
	"アルマイア・デュンゼ（MINI）カード",
	"ロリルリカード",
	"ロリルリ★カード",
	"ゲイズティカード",
	"狂暴化したガリオンカード",
	"堕ちた大神官ヒバムカード",
	"妖狐ミョグェカード",
	"カエデの精霊イシュマカード",
	"銀魚湖のヌシカード",
	"火焔鳥ジュリーカード",
	"リムルカード",
	"クリスタルビーストカード",
	"キングドラモカード",
	"鉱石の精カード"
]


CK = os.getenv('CK')
CS = os.getenv('CS')
AT = os.getenv('AT')
AS = os.getenv('AS')

url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

dp_token = os.getenv('DP_TOKEN')

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

def MarketSearch(Item):
	pyautogui.moveTo(235,225)  # search Window
	pyautogui.click()
	pyautogui.moveTo(735,250)  # inputText Window
	pyautogui.click()

	pyperclip.copy("^"+Item)
	sleep(1)
	pyautogui.hotkey('command','v')
	pyautogui.hotkey('enter')
	pyautogui.hotkey('enter')
	pyautogui.moveTo(695,355)  # searchResult Window
	pyautogui.click()

	sleep(1)
	sc = pyautogui.screenshot('MarketResult.png',region=(443, 203, 405, 112))
	im = Image.open(r"MarketResult.png").convert("RGB")
	price = im.crop((220, 60, 400, 90))
	OptimizePrice(price).save("Price.png")
	time = im.crop((333, 20, 405, 48))
	OptimizeTime(time).save("Time.png")

def OptimizePrice(image):
	border = 175
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
	border = 175
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
	twitter = tweepy.API(auth)
	sleep(5)	
	for item in itemlist:
		MarketSearch(item)

		p = TranslationActors("Price.png").replace('.',",")
		t = TranslationActors("Time.png")
		
		if p is not "" and t is not "":
			print(item + ": " + p + " z 残り" + t)
			twitter.update_status_with_media(status = item + ": 残り" + t, filename = "MarketResult.png")