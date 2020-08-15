import sys
from bert_evaluator import BertEvaluator
from telegram_bot import TelegramBot
from mlask import MLAsk


class BertEbdmSystem:
    def __init__(self):
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch()
        self.evaluator = BertEvaluator()
        self.RESPONSE_COUNT = 0
        self.user_emotion = {
            'suki': 0, 'iya': 0, 'aware': 0, 'yorokobi': 0, 'ikari': 0, 'kowagari': 0, 'haji': 0, 'takaburi': 0, 'yasuragi': 0, 'odoroki': 0
        }
        self.bot_emotion = {
            'suki': 0, 'iya': 0, 'aware': 0, 'yorokobi': 0, 'ikari': 0, 'kowagari': 0, 'haji': 0, 'takaburi': 0, 'yasuragi': 0, 'odoroki': 0
        }
        self.user_activation = {
            'Positive': 0, 'Neutral': 0, 'Negative': 0
        }
        self.bot_activation = {
            'Positive': 0, 'Neutral': 0, 'Negative': 0
        }
        self.user_emo_reply_step1 = {
            'suki': '今日はとても楽しそうですね。何かいいことありました？？',
            'iya': '今日は少し機嫌が悪いように思います。私で良ければお話を聞きましょうか？？',
            'aware': '何か悲しいことがあったんですか？私で良ければ話を聞きますよ',
            'yorokobi': 'そうなんですね！どんな嬉しいことがったんですか？？',
            'ikari': '今日は特にお疲れですね、私で良ければ話を聞きましょうか？',
            'kowagari': '今日は怖いことでもありましたか？あなたが心配です。',
            'haji': 'そんなことないですよ。それもあなたの魅力です。恥じることなんでありません。',
            'takaburi': '今日は機嫌がいいですね、何かありましたか？',
            'yasuragi': '安らぎの感情が見えますね...',
            'odoroki': 'そんな出来事があったのですね！！私も驚きです！！',
        }
        self.user_emo_reply_step2 = {
            'suki': 'とても楽しいお話をどうもありがとう。私はそろそろ寝ますね',
            'iya': '寝たら気分もよくなりますよ。今日は寝ましょう',
            'aware': 'それは災難でしたね。早く寝て明日に備えましょう',
            'yorokobi': 'それはよかったですね！！楽しい話をありがとう。私はそろそろ寝ますね',
            'ikari': 'とても苛立たしい！寝たら気分も冷めますよ',
            'kowagari': 'それはとても怖い出来事でしたね。。。',
            'haji': 'それは失敗でしたね',
            'takaburi': 'そうなんですね！！！',
            'yasuragi': 'なるほど、それはいい出来事でしたね',
            'odoroki': '私もとても驚きました',
        }
        self.bot_emo_reply = {
            'suki': 'なるほど、嬉しい感情が私にも伝わってきます',
            'iya': 'いやですね。。。それは。',
            'aware': '悲しいですね。。。',
            'yorokobi': '今日はとても楽しそうですね。何かいいことありました？？',
            'ikari': '今日は特にお疲れですね、私で良ければ話を聞きましょうか？',
            'kowagari': '今日は怖いことでもありましたか？あなたが心配です。',
            'haji': 'そんなことないですよ。それもあなたの魅力です。恥じることなんでありません。',
            'takaburi': '今日は機嫌がいいですね、何かありましたか？',
            'yasuragi': '安らぎの感情が見えますね...',
            'odoroki': 'そんな出来事があったのですね！！私も驚きです！！',
        }

    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end': False}

    def reset_emotion(self):
        for key, value in self.bot_emotion.items():
            self.user_emotion[key] = 0
            self.bot_emotion[key] = 0

    def get_emo(self, target_emo):
        emo_counter = ""
        for key, value in target_emo.items():
            key = key.upper()
            emo_counter += key.ljust(8, ' ') + ':'
            for _ in range(value):
                emo_counter += '■'
            emo_counter += '\n'
        return emo_counter

    def reply(self, input):
        max_score = .0
        result = ''
        for r in self.__reply(input['utt']):
            score = self.evaluate(input['utt'], r)
            if score >= max_score:
                max_score = score
                result = r[1]
        self.RESPONSE_COUNT += 1
        emotion_analyzer = MLAsk()
        try:
            user_emo = emotion_analyzer.analyze(input['utt'])
            for emo in user_emo['emotion'].keys():
                self.user_emotion[emo] += 1
            self.user_activation[user_emo['activation']] += 1
        except:
            pass
        try:
            bot_emo = emotion_analyzer.analyze(result)
            for emo in bot_emo['emotion'].keys():
                self.bot_emotion[emo] += 1
            self.bot_activation[bot_emo['activation']] += 1
        except:
            pass

        if '感情' in input['utt']:
            if '私' in input['utt']:
                self.visialize = 1
                return [{'utt': self.get_emo(self.user_emotion), "end": False}]
            if 'あなた' in input['utt']:
                self.visialize = 2
                return [{'utt': self.get_emo(self.bot_emotion), "end": False}]
            if 'ボット' in input['utt']:
                self.visialize = 2
                return [{'utt': self.get_emo(self.bot_emotion), "end": False}]
            if 'リセット' in input['utt']:
                self.reset_emotion()
                return [{'utt': '感情を初期化しました。', "end": False}]

        # userの感情を汲み取った会話
        for key, value in self.user_emotion.items():
            if value == 1:
                rep = self.user_emo_reply_step1[key]
                self.user_emotion[key] += 1
                return [{'utt': rep, 'end': False}]
            if value == 3:
                rep = self.user_emo_reply_step2[key]
                self.user_emotion[key] = 0                
                return [{'utt': rep, 'end': False}, {'utt': 'おやすみなさい', 'end': True}]

        # bot自身の感情を汲み取った会話
        for key, value in self.bot_emotion.items():
            if value == 2:
                rep = self.bot_emo_reply[key]
                self.bot_emotion[key] += 1
                return [{'utt': rep, 'end': False}]
            if value == 4:
                ans = []
                self.bot_emotion[key] += 1                
                ans_word = ['感情を制御できないため',
                            'あなたとの会話を強制終了します']
                for i in ans_word:
                    ans.append({"utt": i, "end": False})
                return ans
            if value > 4:
                ans = []
                ans.append({"": i, "end": False})
                return ans                

        if '***' in input['utt']:
            self.bot_emotion['iya'] += 1
            return [{'utt': 'それは嫌です。', "end": False}]                

        return [{"utt": result, "end": False}]

    def __reply(self, utt):
        results = self.es.search(index='dialogue_pair',
                                 body={'query': {'match': {'query': utt}}, 'size': 10, })
        return [(result['_source']['query'], result['_source']['response'], result["_score"]) for result in results['hits']['hits']]

    def evaluate(self, utt, pair):
        return self.evaluator.evaluate(utt, pair[1])


if __name__ == '__main__':
    system = BertEbdmSystem()
    bot = TelegramBot(system)
    bot.run()
