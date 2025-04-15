#!/usr/bin/env python3
# condig: utf-8

import sys
import pyocr
import pyocr.builders
import pyautogui
import pyperclip
import numpy as np
import os
import dropbox
import json
from notion_client import Client
from datetime import datetime
from time import sleep, time
from PIL import Image
from os.path import join, dirname
from dotenv import load_dotenv
from discordwebhook import Discord
import cv2


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ndb = os.getenv('NOTION_DB')
ns = os.getenv('NOTION_SECRET')
client = Client(auth=ns)

discord_url = os.getenv('6V_URL')
discord_headers = {'Content-Type': 'application/json'}

pyautogui.FAILSAFE = False

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

dp_token = os.getenv('DP_TOKEN')

transferData = TransferData(dp_token)

file_from = 'Avatar.png'
file_to = '/Avatar.png'  

dp_avator_url = os.getenv('DP_AVATOR_URL')
dp_origin_url = os.getenv('DP_ORIGIN_URL')
dp_token = os.getenv('DP_TOKEN')

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[5]
print("Will use lang '%s'" % (lang))

start_time=""
end_time=""
expired_items=[]

def pageFromDB(database_id):
    has_more = False
    response = client.databases.query(
        **{
            "database_id": database_id,
        }
    )

    has_more = response["has_more"]
    next_cursor = response["next_cursor"]
    results = response["results"]
    page_ids = []
    for result in results:
        #print(result)
        # print(f'page_id={result["id"]}')
        page_ids.append(result["id"])

    while has_more:
        response = client.databases.query(
            **{
                "database_id": database_id,
                'start_cursor': next_cursor,
            }
        )

        has_more = response["has_more"]
        next_cursor = response["next_cursor"]
        results = response["results"]

        for result in results:
            page_ids.append(result["id"])

    return page_ids

def readFromPage(page_id):
    response = client.pages.retrieve(
        **{
            "page_id": page_id,
        }
    )
    return response

def updatePageImageUrl(page_id, image_url, loot):
    client.pages.update(
        **{
            "page_id": page_id,
            "properties": {
                "Image": {
                    'type': 'files', 
                    'files': [{
                        'name': "Origin.png",
                        'type': 'external', 
                        'external': {
                            'url': image_url
                        }
                    }]
                },
                "Loot" : {
                    'type': 'checkbox',
                    'checkbox': loot
                }
            }
        }
    )


def MarketSearch(Item):
    pyautogui.click(944,917)  # card get
    pyautogui.click(312,265)
    sleep(0.5)
    pyautogui.click(1028,302) 
    sleep(0.5)
    pyperclip.copy("^"+Item)
    pyautogui.mouseDown(209,952)
    sleep(1.5)
    pyautogui.mouseUp()
    sleep(1)
    pyautogui.click(200,950)  # paste Window

    sleep(1.5)
    pyautogui.click(1356,304)  # search Window
    sleep(0.5)
    pyautogui.click(908,444)  # searchResult Window
    sleep(0.5)
    sc = pyautogui.screenshot(f'img/Origin.png',region=(605, 307, 530, 140))
    im = Image.open(f'img/Origin.png').convert("RGB")
    im.crop((26, 10, 128, 138)).save("img/Avatar.png")
    price = im.crop((287, 82, 496, 115))
    img_price = np.array(price)
    GrayscaleAndResize(img_price, f"img/Price.png", new_dpi=300)
    TranslationActors("img/Price.png")
    time = im.crop((440, 38, 516, 62))
    img_time = np.array(time)
    GrayscaleAndResize(img_time, f"img/Time.png", new_dpi=300)
    TranslationActors("img/Time.png")


def GrayscaleAndResize(img_np, output_path, new_dpi=300):
    block_size = 147           # Block size for adaptive thresholding. This should be positive and odd value more than 1. 
    C = 31                          # The constant to subtract from mean or weighted mean
    open_ksize = (5, 5)       # The kernel size to remove white patch in black region
    close_ksize = (3, 3)      # The kernel size to remove black patch in white region
    img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)  

    original_dpi = 60
    scale_factor = new_dpi / original_dpi
    
    new_width = int(img_gray.shape[1] * scale_factor)
    new_height = int(img_gray.shape[0] * scale_factor)
    new_size = (new_width, new_height)
    
    resized_img = cv2.resize(img_gray, new_size, interpolation=cv2.INTER_LINEAR)
    adaptive_img = cv2.adaptiveThreshold(resized_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    img_morph_open = cv2.morphologyEx(adaptive_img, cv2.MORPH_OPEN, np.ones(open_ksize, np.uint8))
    img_morph_close = cv2.morphologyEx(img_morph_open, cv2.MORPH_CLOSE, np.ones(close_ksize, np.uint8))
    
    cv2.imwrite(output_path, img_morph_close)

def TranslationActors(img):
    txt = tool.image_to_string(
        Image.open(img),
        lang="script/Japanese",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return(txt)


def process_item(page_id, discord, transfer_data):
    global expired_items
    global end_time
    p = 0
    t = 0
    item = readFromPage(page_id)
    if not item["properties"]["Ignore"]["checkbox"]: 
        item_name = item["properties"]["Name"]["title"][0]["plain_text"]
        id = str(item["properties"]["ID"]["unique_id"]["number"])
        image_url = item["properties"]["URL"]["url"].strip()

        mention = ""
        MarketSearch(item_name)
        p = TranslationActors("img/Price.png")
        t = TranslationActors("img/Time.png")

        sleep(1)

        if p and t:
            transfer_data.upload_file("img" + "/Avatar.png", "/Avatar.png")
            transfer_data.upload_file("img" + "/Origin.png", "/" + id +".png")
            updatePageImageUrl(page_id, image_url + "&" + str(time()), True)
            sleep(3)
            with open(f'img/Origin.png', 'rb') as f:
                discord.post(username=item_name, avatar_url=dp_avator_url + "&" + str(time()), content=item_name, file={"attachment": f})

            if item['properties']['DM']['rich_text']:
                for acc in item['properties']['DM']['rich_text'][0]['text']['content'].split(','):
                    mention = mention + acc + " "
            discord.post(username=item_name, avatar_url=dp_avator_url + "&" + str(time()), content=mention)
        elif p and not t:
            transfer_data.upload_file("img" + "/Origin.png", "/" + id +".png")
            updatePageImageUrl(page_id, image_url + "&" + str(time()), False)


if __name__ == "__main__":

    discord = Discord(url=discord_url)

    pyautogui.moveTo(944,917)  # card get
    for i in range(5):
        pyautogui.tripleClick()

    for page_id in pageFromDB(ndb):
        process_item(page_id, discord, transferData)

    pyautogui.moveTo(1006,934)  # back Window
    pyautogui.click()