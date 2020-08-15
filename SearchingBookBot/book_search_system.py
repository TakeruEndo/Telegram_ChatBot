import sys
from PySide2 import QtCore, QtScxml
import requests
import json
from datetime import datetime, timedelta, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot


class WeatherSystem:

    # 状態とシステム発話を紐づけた辞書
    uttdic = {"ask_purpose": "調べたい内容を教えてください[タイトル][著者][あらすじ][発売日][表紙][出版社]",
              "ask_isbn": "調べたい本のisbnを知っていたら教えてください。",
              "ask_author": "著者名を言ってください(キーワード)",
              "ask_title": "タイトルを言ってください(キーワード)"}

    url = 'https://www.googleapis.com/books/v1/volumes?q='

    def __init__(self):
        # Qtに関するおまじない
        app = QtCore.QCoreApplication()

        # 対話セッションを管理するための辞書
        self.sessiondic = {}

    def get_purpose(self, text):
        if text == 'あらすじ':
            text = 'description'
        elif text == '著者':
            text = 'authors'
        elif text == '発売日':
            text = 'publishedDate'
        elif text == 'タイトル':
            text = 'title'
        elif text == '出版社':
            text = 'publisher'
        return text

    def get_author(self, text):
        return text

    def get_title(self, text):
        return text

    def get_book_info(self, author, title, isbn, purpose):
        if isbn:
            print(isbn)
            search = self.url + 'isbn:' + isbn
        elif title == '知らない':
            search = self.url + 'inauthor:' + author
        elif author == '知らない':
            search = self.url + 'intitle:' + title
        else:
            search = self.url + 'inauthor:' + author + '+intitle:' + title
        response = requests.get(search)
        print(search)
        print(purpose)
        if purpose == '表紙':
            return response.json()['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
        elif purpose == 'authors':
            return response.json()['items'][0]['volumeInfo']['authors'][0]
        elif purpose == 'some_title':
            answer = "お探しの本のタイトルは、以下ではないでしょうか？"
            for i in range(5):
                answer = answer + '"' + \
                    str(response.json()['items'][i]
                        ['volumeInfo']['title']) + '"'
                if i != 4:
                    answer += ','
            return answer
        else:
            return response.json()['items'][0]['volumeInfo'][purpose]

    def initial_message(self, input):
        text = input["utt"]
        print(text)
        sessionId = input["sessionId"]

        self.el = QtCore.QEventLoop()

        # SCXMLファイルの読み込み
        sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

        # セッションIDとセッションに関連する情報を格納した辞書
        # 複数人がアクセスしてもいいようにする
        self.sessiondic[sessionId] = {
            "statemachine": sm, "purpose": "", "isbn": "", "author": "", "title": ""}

        # 初期状態に遷移
        sm.start()
        self.el.processEvents()

        # 初期状態の取得
        current_state = sm.activeStateNames()[0]
        print("current_state=", current_state)

        # 初期状態に紐づいたシステム発話の取得と出力
        sysutt = self.uttdic[current_state]

        return {"utt": "知りたい本に関するキーワードから目的の情報を推測します。\n" + sysutt, "end": False}

    def reply(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        sm = self.sessiondic[sessionId]["statemachine"]
        current_state = sm.activeStateNames()[0]
        print("current_state=", current_state)

        # ユーザ入力を用いて状態遷移
        if current_state == "ask_purpose":
            purpose = self.get_purpose(text)
            if purpose != "":
                sm.submitEvent("purpose")
                self.el.processEvents()
                self.sessiondic[sessionId]["purpose"] = purpose
        if current_state == "ask_isbn":
            isbn = text
            if isbn != "":
                sm.submitEvent("isbn")
                self.el.processEvents()
                self.sessiondic[sessionId]["isbn"] = isbn
        elif current_state == "ask_author":
            author = self.get_author(text)
            if author != "":
                sm.submitEvent("author")
                self.el.processEvents()
                self.sessiondic[sessionId]["author"] = author
        elif current_state == "ask_title":
            title = self.get_title(text)
            if title != "":
                sm.submitEvent("title")
                self.el.processEvents()
                self.sessiondic[sessionId]["title"] = title

        # 遷移先の状態を取得
        current_state = sm.activeStateNames()[0]
        print("current_state=", current_state)

        # 遷移先がtell_infoの場合は情報を伝えて終了

        if current_state == "tell_info":
            utts = []
            utts.append("お伝えします")
            isbn = self.sessiondic[sessionId]['isbn']
            purpose = self.sessiondic[sessionId]["purpose"]
            author = self.sessiondic[sessionId]["author"]
            title = self.sessiondic[sessionId]["title"]
            try:
                # isbnで検索
                book_info = self.get_book_info(
                    author, title, isbn=isbn, purpose=purpose)
                utts.append(book_info)
            except:
                try:
                    book_info = self.get_book_info(
                        author, title, isbn=None, purpose=purpose)
                    utts.append(book_info)
                except:
                    try:
                        book_info = self.get_book_info(
                            author, title='知らない', isbn=None, purpose='some_title')
                        utts.append("情報の取得に失敗しました...")
                        utts.append(book_info)
                    except:
                        utts.append("情報の取得に失敗しました。")

            utts.append("ご利用ありがとうございました")
            del self.sessiondic[sessionId]
            return {"utt": "。".join(utts), "end": True}
        else:
            # その他の遷移先の場合は状態に紐づいたシステム発話を生成
            sysutt = self.uttdic[current_state]
            return {"utt": sysutt, "end": False}


if __name__ == '__main__':
    system = WeatherSystem()
    bot = TelegramBot(system)
    bot.run()

# end of file
