import MeCab
import re
import random
import json
import pandas as pd
import xml.etree.ElementTree

book_info = pd.read_csv('book_rank.csv')

authors = book_info['著者'].values

titles = book_info['タイトル'].values

# 情報種別のリスト
types = ["出版社", "タイトル", '著者', '詳細', 'あらすじ', '表紙']

# サンプル文に含まれる単語を置き換えることで学習用事例を作成


def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text, posdic
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "author":
            author = random.choice(authors)
            buf += author
            posdic["author"] = (pos, pos+len(author))
            pos += len(author)
        elif elem.tag == "title":
            title = random.choice(titles)
            buf += title
            posdic["title"] = (pos, pos+len(title))
            pos += len(title)
        elif elem.tag == "type":
            _type = random.choice(types)
            buf += _type
            posdic["type"] = (pos, pos+len(_type))
            pos += len(_type)
        if elem.tail is not None:
            buf += elem.tail
            pos += len(elem.tail)
    return buf, posdic

# 現在の文字位置に対応するタグをposdicから取得


def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"


# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# 学習用ファイルの書き出し先
fp = open("concept_samples.dat", "w")

da = ''
# eamples.txt ファイルの読み込み
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
        # 各サンプル文を1000倍に増やす
        if da == 'initialize' or da == 'correct-info':
            loop_count = 1000
            for i in range(1000):
                sample, posdic = random_generate(root)

                # lis は[単語，品詞，ラベル]のリスト
                lis = []
                pos = 0
                prev_label = ""
                for line in mecab.parse(sample).splitlines():
                    if line == "EOS":
                        break
                    else:
                        word, feature_str = line.split("\t")
                        features = feature_str.split(',')
                        # 形態素情報の0番目が品詞
                        postag = features[0]
                        # 現在の文字位置に対応するタグを取得
                        label = get_label(pos, posdic)
                        # label がOでなく，直前のラベルと同じであればラベルに'I-'をつける
                        if label == "O":
                            lis.append([word, postag, "O"])
                        elif label == prev_label:
                            lis.append([word, postag, "I-" + label])
                        else:
                            lis.append([word, postag, "B-" + label])
                        pos += len(word)
                        prev_label = label

                # 単語，品詞，ラベルを学習用ファイルに書き出す
                for word, postag, label in lis:
                    fp.write(word + "\t" + postag + "\t" + label + "\n")
                fp.write("\n")
        else:
            for i in range(3000):
                sample, posdic = random_generate(root)

                # lis は[単語，品詞，ラベル]のリスト
                lis = []
                pos = 0
                prev_label = ""
                for line in mecab.parse(sample).splitlines():
                    if line == "EOS":
                        break
                    else:
                        word, feature_str = line.split("\t")
                        features = feature_str.split(',')
                        # 形態素情報の0番目が品詞
                        postag = features[0]
                        # 現在の文字位置に対応するタグを取得
                        label = get_label(pos, posdic)
                        if postag == '名詞' or postag == '助動詞' or postag == '動詞' or postag == '記号':
                            # label がOでなく，直前のラベルと同じであればラベルに'I-'をつける
                            if label == "O":
                                lis.append([word, postag, "O"])
                            elif label == prev_label:
                                lis.append([word, postag, "I-" + label])
                            else:
                                lis.append([word, postag, "B-" + label])
                            pos += len(word)
                            prev_label = label
                        else:
                            continue

                # 単語，品詞，ラベルを学習用ファイルに書き出す
                for word, postag, label in lis:
                    fp.write(word + "\t" + postag + "\t" + label + "\n")
                fp.write("\n")            

fp.close()
