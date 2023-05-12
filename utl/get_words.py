import pandas as pd
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class data:
    idiom = pd.read_json(f'{path}/data/idiom.json')
    words = pd.read_json(f'{path}/data/ci.json')
    word = pd.read_json(f'{path}/data/word.json')


def get_words(text):
    idiom_list = data.idiom[data.idiom.word.map(lambda x:True if text.strip() == x.strip() else False)]
    if len(idiom_list)>0:
        return ','.join(idiom_list.explanation.to_list())
    else:
        words_list = data.words[data.words.ci.map(lambda x:True if text.strip() == x.strip() else False)]
        if len(words_list):
            return ','.join(words_list.explanation.to_list())
        else:
            text_word_explain = {}
            for i in set(text):
                word_list = data.word[data.word.word.map(lambda x: True if text.strip() == x.strip() else False)]
                text_word_explain[i] = ','.join(word_list.explanation.to_list())
                ## 暂不解释单个字
            return ''
