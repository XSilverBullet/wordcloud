# -*- encoding:utf-8 -*-
from __future__ import print_function
import pandas as pd


def get_Data(filename):
    try:
        data = pd.read_csv(filename)

        data = data["abstract"] + data["main_right"]

        data = data.tolist()

        return data
    except:
        print("read error")
        return None

def textrank(number_keyword):
    data = get_Data("1995.csv")

    with open("1995.txt", "w", encoding="utf-8") as f:
        f.write(str(data))

    import codecs
    from textrank4zh import TextRank4Keyword, TextRank4Sentence

    text = codecs.open('1995.txt', 'r', 'utf-8').read()
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象


    word2count = {}

    print('关键词：')

    #需要返回关键词的个数

    for item in tr4w.get_keywords(number_keyword, word_min_len=1):
        word2count[item.word] = item.weight
        print(item.word, item.weight)

    return word2count

if __name__=="__main__":
    word2count = textrank(100)
    print(word2count)

# print()
# print('关键短语：')
# for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
#     print(phrase)
#
# tr4s = TextRank4Sentence()
# tr4s.analyze(text=text, lower=True, source='all_filters')
#
# print()
# print('摘要：')
# for item in tr4s.get_key_sentences(num=3):
#     print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重
