import requests
from PySide2 import QtCore, QtScxml


url = 'https://www.googleapis.com/books/v1/volumes?q='


def get_author(text):
    return text


def get_title(text):
    return text


def get_purpose(text):
    if text == 'あらすじ':
        text = 'description'
    elif text == '著者':
        text = 'author'
    elif text == '発売日':
        text = 'publishedDate'
    elif text == 'タイトル':
        text = 'title'
    elif text == '出版社':
        text = 'publisher'
    return text


def get_info(response, purpose):
    if purpose == '表紙':
        return response.json()['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
    else:
        return response.json()['items'][0]['volumeInfo'][purpose]


# Qtに関するおまじない
app = QtCore.QCoreApplication()
el = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> 知りたい本に関するキーワードから目的の情報を推測します。")

# 状態とシステム発話を紐づけた辞書
uttdic = {"ask_purpose": "調べたい内容を教えてください[タイトル][著者][あらすじ][発売日][表紙][詳細]",
          "ask_isbn": "調べたい本のisbnを知っていたら教えてください。",
          "ask_author": "著者名を言ってください(キーワード)",
          "ask_title": "タイトルを言ってください(キーワード)"}

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
        try:
            search = url + 'isbn:' + isbn
            response = requests.get(search)
            print(get_info(response, purpose))
        except:
            try:
                search = url + 'inauthor:' + author + '+intitle:' + title
                response = requests.get(search)
                print(get_info(response, purpose))
            except:
                try:
                    search = url + 'inauthor:' + author
                    response = requests.get(search)
                    print('検索に失敗しました。')
                    print('お探しの本のタイトルは、以下ではないでしょうか？')
                    for i in range(5):
                        print(response.json()['items']
                              [i]['volumeInfo']['title'])
                except:
                    print('情報の取得に失敗しました。')
        break
    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[current_state]
        print("SYS>", sysutt)

# 終了発話
print("ご利用ありがとうございました")
