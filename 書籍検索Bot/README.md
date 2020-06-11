# 書籍検索
著者,本のタイトルのキーワードから以下の情報を提供します。  
[著者名,本のタイトル,あらすじ,本の表紙,出版社,詳細]  

# 使用方法
```
# python scriptで実行
$ python search_books.py
# telegramBotを起動
$ python book_search_system.py
```

# コードの詳細
## states.scxml
有限状態オートマトンを記述
```
$ pip3 install PySide2
```
## telegram_bot.py
telegramの操作

# フレーム表現による対話
SVMによる対話行為タイプ推定を行う
## 学習データの作成
### example.txt
データ拡張の方針を記述
### generate_da_samplespy
著者、タイトル、目的にあたる語を学習
## 著者・タイトルデータの収集
### book_scraping.py
下記noteのコードを使用して「ハイブリッド型総合書店HONTO」からデータを収集しcsv形式で保存  
https://note.com/hungair0925/n/nb9b3b5beefef  
## 学習
### train_da_model.py
SVMを学習
## 対話行為タイプ推定
### da_extractor.py
# コンセプト抽出
## generate_concept_samples.py
コンセプトの作成
## train_concept_model.py
CRFの学習
## concept_extactor.py
コンセプト推定
```
夏目漱石の吾輩は猫であるのあらすじ
{'author': '夏目漱石の', 'title': 'は猫である', 'type': 'あらすじ'}
もう一度はじめから
{}
太宰治じゃなくて
{'author': '太宰治'}
森絵都のカラフルの著者は？
{'author': 'カラフルの', 'title': 'は？'}
恩田陸の蜜蜂と遠雷のあらすじを教えて
{'author': '恩田陸', 'title': '蜜蜂と遠雷', 'type': 'あらすじ'}
ハムレットの著者は誰？
{'author': 'ハムレットの', 'title': 'は誰？'}
```
頑張っているがもうひと超えしてほしい....
### 助詞を学習対象外にする
```
夏目漱石の吾輩は猫であるのあらすじ {'title': '夏目漱石の吾輩は猫であるのあらすじ'}
もう一度はじめから {}
太宰治じゃなくて {'author': '太宰治'}
森絵都のカラフルの著者は？ {'title': '森絵都のカラフルの著者は？'}
恩田陸の蜜蜂と遠雷のあらすじを教えて {'title': '恩田陸の蜜蜂と遠雷のあらすじを教え'}
ハムレットの著者は誰？ {'title': 'ハムレットの著者は誰？'}
```
圧倒的失敗...





