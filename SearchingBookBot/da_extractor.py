import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

mecab = MeCab.Tagger()
mecab.parse('')

# SVMモデルの読み込み
with open("svc_book.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)

# 発話から対話行為タイプを推定


def extract_da(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)
    tokens_str = " ".join(words)
    X = vectorizer.transform([tokens_str])
    Y = svc.predict(X)
    # 数値を対応するラベルに戻す
    da = label_encoder.inverse_transform(Y)[0]
    return da


for utt in ["夏目漱石の吾輩は猫であるのあらすじ", "もう一度はじめから", "太宰治じゃなくて"]:
    da = extract_da(utt)
    print(utt, da)
