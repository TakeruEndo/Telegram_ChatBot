import sys
from PySide2 import QtCore, QtScxml
import requests
import json
from datetime import datetime, timedelta, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot


class WeatherSystem:

    # 状態とシステム発話を紐づけた辞書
    uttdic = {"ask_purpose": "調べたい内容を教えてください[title][author][ISBN]",
              "ask_isbn": "調べたい本のisbnを知っていたら教えてください。",
              "ask_author": "著者名を言ってください",
              "ask_title": "タイトルを言ってください"}

    url = 'https://www.googleapis.com/books/v1/volumes?q='

    def __init__(self):
        # Qtに関するおまじない
        app = QtCore.QCoreApplication()

        # 対話セッションを管理するための辞書
        self.sessiondic = {}

    def get_purpose(self, text):
        return text

    def get_author(self, text):
        return text

    def get_title(self, text):
        return text

    def get_book_info(self, author, title, isbn=None):
        if isbn is not None:
            search = self.url + 'isbn:' + isbn
        else:
            search = self.url + 'inauthor:' + author + '+intitle:' + title
        response = requests.get(search)
        return response.json()

    def initial_message(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        self.el = QtCore.QEventLoop()

        # SCXMLファイルの読み込み
        sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

        # セッションIDとセッションに関連する情報を格納した辞書
        # 複数人がアクセスしてもいいようにする
        self.sessiondic[sessionId] = {
            "statemachine": sm, "purpose": "", "author": "", "title": ""}

        # 初期状態に遷移
        sm.start()
        self.el.processEvents()

        # 初期状態の取得
        current_state = sm.activeStateNames()[0]
        print("current_state=", current_state)

        # 初期状態に紐づいたシステム発話の取得と出力
        sysutt = self.uttdic[current_state]

        return {"utt": "こちらは天気情報案内システムです。" + sysutt, "end": False}

    def reply(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        sm = self.sessiondic[sessionId]["statemachine"]
        current_state = sm.activeStateNames()[0]
        print("current_state=", current_state)

        # ユーザ入力を用いて状態遷移
        if current_state == "ask_purpose":
            purpose = self.get_purpose(text)
            if purpose == "title" or purpose == "isbn" or purpose == "author":
                sm.submitEvent("purpose")
                self.el.processEvents()
                self.sessiondic[sessionId]["purpose"] = purpose
        elif current_state == "ask_isbn":
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
            purpose = self.sessiondic[sessionId]["purpose"]
            author = self.sessiondic[sessionId]["author"]
            title = self.sessiondic[sessionId]["title"]
            try:
                book_info = self.get_book_info(author, title, isbn=None)
                utts.append(book_info["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"])
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
