# -*- coding: utf-8 -*-

import xml.dom.minidom      # XML parser
import urllib2              # XMLコンテンツの取得
import random               # リスト内からランダムで一つ要素を取得
import os                   # 環境変数を取得
import requests             # 記事情報を取得
import sys                  # exit利用のため
import json                 # HTTPリクエストのjson利用
from requests_oauthlib import OAuth1Session # Twitter認証用のライブラリ

# ブログのURLを環境変数から取得する
blogURL = os.environ.get('Hatena_Blog_URL')     # BlogURL(末尾/付き)
hashTag = os.environ.get('Twitter_Hash_Tag')    # ハッシュタグ #なし

## Twitter系の変数
# OAuth認証 セッションを開始
CK = os.getenv('Twitter_Consumer_Key')          # Consumer Key
CS = os.getenv('Twitter_Consumer_Secret_Key')   # Consumer Secret
AT = os.getenv('Twitter_Access_Token_Key')      # Access Token
AS = os.getenv('Twitter_Access_Token_Secret')   # Accesss Token Secert

#
# blogURL + sitemap.xml内の個別サイトマップリンクを取得
# 引数：XML取得するURL
# 戻り値：XMLのlocパラメーターの内容
#
def GetSiteMapList(url):

    siteList = []

    # XMLの取得
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))

    # 個別サイトマップリンクの取得
    for entry in dom.getElementsByTagName('loc'):
        siteList.append(entry.firstChild.data)

    return siteList

#
# HatenaAPIを利用し記事情報を取得
# 引数：記事URL
# 戻り値：記事情報
# http://developer.hatena.ne.jp/ja/documents/blog/apis/oembed
#
def URLContentsGet(articleURL):

    hatenaURL = 'http://hatenablog.com/oembed'
    data = {
        'url': articleURL,
        'format': 'json'
        }

    req = requests.get(hatenaURL, params = data)

    # HTTPステータスコードでエラー判定
    if req.status_code != 200:
        print ("Error: %d" % req.status_code)
        sys.exit()

    return json.loads(req.text)

#
# Tweetをする
# 引数：記事情報
#
def Tweet(articleInfo, articleURL):

    # 文章作成
    data = \
        u'ーこんな記事も読んでみませんか？ー\n#' + hashTag +'\n\n' \
        + articleInfo['title'] + '\n\n' \
        u'▼記事はこちらから！\n' + articleURL

    twitter = OAuth1Session(CK, CS, AT, AS)

    # ツイート本文
    params = {"status": data}

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証で POST method で投稿
    req = twitter.post(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)
        sys.exit()

#
# メイン処理
#
def lambda_handler(event, context):

    # 個別サイトマップリンクを取得
    # リンクのうちから１つランダムで取得
    individualSiteMapURL = \
        random.choice(GetSiteMapList(blogURL + 'sitemap.xml'))

    # ランダムで取得したURLを取得
    articleURL = \
        random.choice(GetSiteMapList(individualSiteMapURL))

    # 記事情報を取得
    articleInfo = URLContentsGet(articleURL)

    # ツイート
    Tweet(articleInfo, articleURL)

    return { "messages":"success!" }
