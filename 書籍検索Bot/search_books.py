import requests
from PySide2 import QtCore, QtScxml


url = 'https://www.googleapis.com/books/v1/volumes?q='


def get_author(text):
    return text


def get_title(text):
    return text


def get_purpose(text):
    return text


# Qtに関するおまじない
app = QtCore.QCoreApplication()
el = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> 書籍検索をします")

# 状態とシステム発話を紐づけた辞書
uttdic = {"ask_purpose": "調べたい内容を教えてください[title][author][ISBN]",
          "ask_isbn": "調べたい本のisbnを知っていたら教えてください。",
          "ask_author": "著者名を言ってください",
          "ask_title": "タイトルを言ってください"}

# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)

# ユーザ入力の処理
while True:
    text = input("> ")

    # ユーザ入力を用いて状態遷移
    if current_state == "ask_purpose":
        purpose = get_purpose(text)
        if purpose != "":
            sm.submitEvent("purpose")
            el.processEvents()
    elif current_state == "ask_isbn":
        isbn = text
        if isbn != "":
            sm.submitEvent("isbn")
            el.processEvents()
    elif current_state == "ask_author":
        author = get_author(text)
        if author != "":
            sm.submitEvent("author")
            el.processEvents()
    elif current_state == "ask_title":
        title = get_title(text)
        if title != "":
            sm.submitEvent("title")
            el.processEvents()

    # 遷移先の状態を取得
    current_state = sm.activeStateNames()[0]
    print("current_state=", current_state)

    # 遷移先がtell_infoの場合は情報を伝えて終了
    if current_state == "tell_info":
        print("お伝えします")
        search = url + 'inauthor:' + author + '+intitle:' + title
        response = requests.get(search)
        print(response.json()['items'][0]['volumeInfo'][purpose])
        break
    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[current_state]
        print("SYS>", sysutt)

# 終了発話
print("ご利用ありがとうございました")
