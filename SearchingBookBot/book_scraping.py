import re
import csv
import requests
from bs4 import BeautifulSoup

URLs = [
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001020000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001020000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001020000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001020000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001030000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001040000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001040000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001040000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001040000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001050000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001070000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1201_011_029001080000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029003000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029003000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029003000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029003000000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029005000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029005000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029005000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029005000000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029007000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029007000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029007000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029007000000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029009000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029012000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029014000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029014000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029011000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029011000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029011000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029011000000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029023000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029023000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029037000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029037000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029037000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029037000000.html?pgno=4',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029026000000.html',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029026000000.html?pgno=2',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029026000000.html?pgno=3',
    'https://honto.jp/ranking/gr/bestseller_1101_1202_011_029026000000.html?pgno=4'
]


with open("book_rank.csv", "w", encoding="utf-8") as f:
    for url in URLs:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        product_list_html = soup.find_all("div", class_="stContents")
        field_name = ["タイトル", "著者", "値段(円)"]
        writer = csv.DictWriter(f, fieldnames=field_name)
        writer.writeheader()
        for i, tag in enumerate(product_list_html):
            try:
                author_tag = tag.find("ul", class_="stData")
                title_tag = tag.find("h2", class_="stHeading")
                price_tag = tag.find("li", class_="stPrice")
                author = author_tag.li.a.get_text()

                # 正規表現を使わなかったとき
                """
                replace_target = ["（著）", "（編著）", "（監修）"]
                for rep in replace_target:
                    if rep in author:
                        author = author.replace(rep, "")
                """
                author = re.sub("（.*?）", "", author).rstrip()
                title = title_tag.get_text()
                title = re.sub("（.*?）", "", title).rstrip()
                price = price_tag.span.get_text().replace("円", "")
                context = {"タイトル": title, "著者": author, "値段(円)": price}
                writer.writerow(context)
            except:
                pass
