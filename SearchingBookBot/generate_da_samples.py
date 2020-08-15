import re
import random
import json
import pandas as pd
import xml.etree.ElementTree


book_info = pd.read_csv('book_rank.csv')

authors = book_info['著者'].values

title = book_info['タイトル'].values

# 情報種別のリスト
types = ["出版社", "タイトル", '著者', '詳細', 'あらすじ', '表紙']

# サンプル文に含まれる単語を置き換えることで学習用事例を作成


def random_generate(root):
    buf = ""
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "author":
            pref = random.choice(authors)
            buf += pref
        elif elem.tag == "title":
            date = random.choice(title)
            buf += date
        elif elem.tag == "type":
            _type = random.choice(types)
            buf += _type
        if elem.tail is not None:
            buf += elem.tail
    return buf


# 学習用ファイルの書き出し先
fp = open("da_samples.dat", "w")

da = ''
# examples.txt ファイルの読み込み
for line in open("examples.txt", "r"):
    line = line.rstrip()
    # da= から始まる行から対話行為タイプを取得
    if re.search(r'^da=', line):
        da = line.replace('da=', '')
    # 空行は無視
    elif line == "":
        pass
    else:
        # タグの部分を取得するため，周囲にダミーのタグをつけて解析
        root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
        # 各サンプル文を5000倍に増やす
        if da == 'initialize':
            for i in range(1000):
                sample = random_generate(root)
                # 対話行為タイプ，発話文，タグとその文字位置を学習用ファイルに書き出す
                fp.write(da + "\t" + sample + "\n")
        elif da == 'correct-info':
            for i in range(1000):
                sample = random_generate(root)
                # 対話行為タイプ，発話文，タグとその文字位置を学習用ファイルに書き出す
                fp.write(da + "\t" + sample + "\n")
        else:
            for i in range(4000):
                sample = random_generate(root)
                # 対話行為タイプ，発話文，タグとその文字位置を学習用ファイルに書き出す
                fp.write(da + "\t" + sample + "\n")

fp.close()
