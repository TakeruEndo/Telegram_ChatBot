# Telegram ChatBot

『[Pythonでつくる対話システム](https://www.ohmsha.co.jp/book/9784274224799/)』を参考に作成したtelegramで操作するチャットボット。

## 書籍検索bot
google_books_apiを使ってキーワードから書籍を検索（推測）するタスク指向型チャットボット

## 感情対話bot
MLAskを使って発話から感情を分析して、ルールベースで感情発話を行う。通常の対話は用例ベースで行っている。これにはElasticSearchとBERTによる対話選択を用いています。