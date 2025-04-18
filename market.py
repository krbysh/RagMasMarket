#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from time import sleep, time
from datetime import datetime
from os.path import join, dirname

import pyocr
import pyautogui
import pyperclip
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from notion_client import Client
from discordwebhook import Discord
import dropbox
import cv2

class Config:
    """環境変数をロードし設定を管理するクラス"""
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.notion_db = os.getenv("NOTION_DB")
        self.notion_secret = os.getenv("NOTION_SECRET")
        self.discord_url = os.getenv("6V_URL")
        self.dp_token = os.getenv("DP_TOKEN")
        self.dp_avatar_url = os.getenv("DP_AVATOR_URL")
        self.dp_origin_url = os.getenv("DP_ORIGIN_URL")


class NotionHelper:
    """Notion APIの操作を簡素化するためのクラス"""
    def __init__(self, config: Config):
        self.client = Client(auth=config.notion_secret)

    def get_page_ids(self, database_id):
        """データベースから全ページIDを取得する"""
        page_ids = []
        has_more = True
        next_cursor = None

        while has_more:
            params = {"database_id": database_id}
            if next_cursor:
                params["start_cursor"] = next_cursor

            response = self.client.databases.query(**params)
            has_more = response.get("has_more", False)
            next_cursor = response.get("next_cursor")
            results = response.get("results", [])
            page_ids.extend([result["id"] for result in results])

        return page_ids

    def get_page(self, page_id):
        """ページ情報を取得"""
        try:
            return self.client.pages.retrieve(page_id=page_id)
        except Exception as e:
            print(f"Failed to retrieve page: {e}")
            return None

    def update_page(self, page_id, image_url=None, loot=None, skip=None):
        """ページを更新"""
        properties = {}
        
        if image_url is not None:
            properties["Image"] = {
                "type": "files",
                "files": [{
                    "name": "Origin.png",
                    "type": "external",
                    "external": {"url": image_url}
                }]
            }

        if loot is not None:
            properties["Loot"] = {"type": "checkbox", "checkbox": loot}

        if skip is not None:
            properties["Skip"] = {"type": "checkbox", "checkbox": skip}

        try:
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
        except Exception as e:
            print(f"Failed to update page: {e}")

class DropboxHelper:
    """Dropboxを操作するためのクラス"""
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, file_from, file_to):
        """ファイルをDropboxにアップロード"""
        try:
            with open(file_from, "rb") as f:
                self.dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
        except Exception as e:
            print(f"Failed to upload file to Dropbox: {e}")


class OCRProcessor:
    """OCRツールを使用するクラス"""
    def __init__(self):
        tools = pyocr.get_available_tools()
        if not tools:
            print("No OCR tool found")
            sys.exit(1)
        self.tool = tools[0]
        print(f"Using OCR tool: {self.tool.get_name()}")

    def extract_text(self, img_path, lang="script/Japanese"):
        """画像からテキストを抽出"""
        try:
            return self.tool.image_to_string(
                Image.open(img_path),
                lang=lang,
                builder=pyocr.builders.TextBuilder(tesseract_layout=6)
            ).replace("\n", "")
        except Exception as e:
            print(f"Failed to extract text from image: {e}")
            return None


class ImageProcessor:
    """画像処理を行うクラス"""
    @staticmethod
    def process_image(img_np, output_path, dpi=300):
        """画像をグレースケール変換しリサイズ"""
        block_size, C = 101, 15
        open_ksize, close_ksize = (5, 5), (3, 3)
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        scale_factor = dpi / 60
        new_size = (int(img_gray.shape[1] * scale_factor), int(img_gray.shape[0] * scale_factor))
        resized_img = cv2.resize(img_gray, new_size, interpolation=cv2.INTER_LINEAR)
        adaptive_img = cv2.adaptiveThreshold(
            resized_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C
        )
        img_morph = cv2.morphologyEx(adaptive_img, cv2.MORPH_CLOSE, np.ones(close_ksize, np.uint8))
        cv2.imwrite(output_path, img_morph)


class MarketSearcher:
    """市場検索を行うクラス"""
    @staticmethod
    def search_item(item_name):
        """アイテムを市場で検索"""
        pyautogui.click(944, 917)  # カード取得
        pyautogui.click(312, 265)
        sleep(0.5)
        pyautogui.click(1028, 302)
        sleep(0.5)
        pyperclip.copy("^" + item_name)
        pyautogui.mouseDown(209, 952)
        sleep(1.5)
        pyautogui.mouseUp()
        sleep(1)
        pyautogui.click(200, 950)  # 貼り付け
        sleep(1.5)
        pyautogui.click(1356, 304)  # 検索
        sleep(0.5)
        pyautogui.click(908, 444)  # 検索結果
        sleep(0.5)
        pyautogui.screenshot(f'img/Origin.png', region=(605, 307, 530, 140))
        im = Image.open(f'img/Origin.png').convert("RGB")
        im.crop((26, 10, 128, 138)).save("img/Avatar.png")
        p = im.crop((287, 82, 496, 115))
        img_price = np.array(p)
        ImageProcessor.process_image(img_price, f"img/Price.png", dpi=200)
        t = im.crop((440, 38, 516, 62))
        img_time = np.array(t)
        ImageProcessor.process_image(img_time, f"img/Time.png", dpi=200)


def process_item(page_id, notion_helper, discord, dropbox_helper, ocr_processor, config):
    """アイテムごとの処理"""
    item = notion_helper.get_page(page_id)
    if not item:
        print(f"Failed to retrieve item for page_id: {page_id}")
        return

    if item["properties"]["Skip"]["checkbox"]:
        print(f"Skipping processing for page_id: {page_id}")
        # Skip フラグを False にリセット
        notion_helper.update_page(page_id, image_url=None, loot=None, skip=False) 
        return

    if not item["properties"]["Ignore"]["checkbox"]:
        item_name = item["properties"]["Name"]["title"][0]["plain_text"]
        id = str(item["properties"]["ID"]["unique_id"]["number"]) 
        image_url = item["properties"]["URL"]["url"].strip()

        MarketSearcher.search_item(item_name)

        # 価格と時間のOCR抽出
        p = ocr_processor.extract_text("img/Price.png")
        t = ocr_processor.extract_text("img/Time.png")

        if p and t:
            dropbox_helper.upload_file("img/Avatar.png", "/Avatar.png")
            dropbox_helper.upload_file("img/Origin.png", f"/{id}.png")
            notion_helper.update_page(page_id, f"{image_url}&{time()}", loot=True, skip=False)
            sleep(3)

            with open("img/Origin.png", "rb") as f:
                discord.post(username=item_name, avatar_url=f"{config.dp_avatar_url}&{time()}", content=item_name, file={"attachment": f})

            mention = ""
            if item["properties"]["DM"]["rich_text"]:
                for acc in item["properties"]["DM"]["rich_text"][0]["text"]["content"].split(','):
                    mention = mention + acc + " "
            discord.post(username=item_name, avatar_url=f"{config.dp_avatar_url}&{time()}", content=mention)

        elif p and not t:
            dropbox_helper.upload_file("img/Origin.png", f"/{id}.png")
            notion_helper.update_page(page_id, f"{image_url}&{time()}", loot=False, skip=True) 


def main():
    config = Config()
    notion_helper = NotionHelper(config)
    dropbox_helper = DropboxHelper(config.dp_token)
    discord = Discord(url=config.discord_url)
    ocr_processor = OCRProcessor()

    for page_id in notion_helper.get_page_ids(config.notion_db):
        process_item(page_id, notion_helper, discord, dropbox_helper, ocr_processor, config)


if __name__ == "__main__":
    main()