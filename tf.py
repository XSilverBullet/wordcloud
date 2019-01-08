import pandas as pd
import jieba
import collections
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import wordcloud


class Lang:
    def __init__(self):
        self.word2index = {}
        self.word2count = {}
        self.index2word = {}
        self.stopwords = self.getStopwords()
        self.n_words = 0.0

    def addSentence(self, sentence):
        for word in str(sentence).split(" "):
            if word not in self.stopwords:
                self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def getStopwords(self):
        words = []
        with open("stopwords.txt", encoding="utf-8") as f:
            for line in f.readlines():
                words.append(line.strip("\n"))
        return words

    def getWord2count(self):
        return self.word2count


def get_Data(filename):
    try:
        data = pd.read_csv(filename)

        data = data["abstract"] + data["main_right"]

        data = data.tolist()

        return data
    except:
        print("read error")
        return None


# return dictionary (word: count)
def getTF():
    data = get_Data("1995.csv")
    data = [str(line) for line in data]
    data = [' '.join(jieba.cut(s, cut_all=False, )) for s in data]

    lang = Lang()

    for sentence in data:
        lang.addSentence(sentence)

    return lang.getWord2count()


word2count = getTF()

mask = np.array(Image.open('wordcloud.jpg'))  # 定义词频背景
wc = wordcloud.WordCloud(
    font_path='simhei.ttf',  # 设置字体格式
    mask=mask,  # 设置背景图
    max_words=200,  # 最多显示词数
    max_font_size=100  # 字体最大值
)

wc.generate_from_frequencies(word2count)  # 从字典生成词云
image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
#wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
plt.imshow(wc)  # 显示词云
plt.axis('off')  # 关闭坐标轴
plt.show()  # 显示图像
