# RagMasMarket

ラグマスの取引所の抽選情報を Twitter 経由で通知します。

# DEMO

下記のように Twitter に投稿されます。ボスカードを対象にした例になります。
<img width="597" alt="demo" src="https://user-images.githubusercontent.com/531279/141736037-5cc7a793-e45c-44f5-833c-4f08d3e7c790.png">

# Features

抽選状態のアイテムの情報を残り時間と共に通知します。

# Requirement

Mac での動作確認済。

* Android Emulator
* Python 3.7.3
* pyocr 0.8
* pyautogui 0.9.53
* pyperclip 1.8.2
* numpy 1.21.4
* tweepy 4.3.0
* python-dotenv 0.19.2

# Installation

下記の手順で、必要なモジュールをインストールします。

```bash
pip3 install pyocr pyautogui pyperclip numpy tweepy python-dotenv
```

# Usage

下記の手順で `market.py` を実行後、ラグマスの画面に切り替えます。

```bash
git clone https://github.com/krbysh/RagMasMarket
cd RagMasMarket/
python3 market.py
```

# Note

利用時には、`.env.sample` を元に、`.env` を作成してください。
事前に Twitter API の利用登録が必要になります。キー、シークレット、トークンなどの取得方法については、[Twitter API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) を参照してください。

```bash
CK = <Twitter Consumer Key>
CS = <Twitter Consumer Secret>
AT = <Twitter Access Token>
AK = <Twitter Access Secret>
```

検索したいアイテム名を `itemlist` に登録してください。
また、`pyautogui.moveTo` や `pyautogui.screenshot` など環境に応じて調整が必要な値があります。

# Author

* krbysh
* y[at]krbysh.net

# License
RagMasMarket は [MIT license](https://en.wikipedia.org/wiki/MIT_License) を適用します。
