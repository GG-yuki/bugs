# -*- coding = utf-8 -*-
# @Time : 2021/4/26 7:59
# @Author : 赵海伶
# @File : mmain.py
# @Software: PyCharm
import codecs
import re

import jieba as jb
import gensim

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence = re.sub(u'[0-9\.]+', u'', sentence)
    jb.add_word('anti-termination')		# 这里是加入用户自定义的词来补充jieba词典。
    jb.add_word('factor-dependent termination')			# 同样，如果你想删除哪个特定的未登录词，就先把它加上然后放进停用词表里。
    jb.add_word('termination factor ρ')
    jb.add_word('T7 phage')
    jb.add_word('gp2 protein')
    jb.add_word('host RNAP')
    jb.add_word('host transcription')

    jb.add_word('RNA polymerase')  # 这里是加入用户自定义的词来补充jieba词典。
    jb.add_word('exit tunnel')  # 同样，如果你想删除哪个特定的未登录词，就先把它加上然后放进停用词表里。
    jb.add_word('termination factor ρ')
    jb.add_word('T7 phage')
    jb.add_word('gp2 protein')
    jb.add_word('host RNAP')
    jb.add_word('host transcription')
    sentence_seged = jb.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords and word.__len__()>1:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


inputs = open('test.doc', 'r', encoding='utf-8')

outputs = open('result.txt', 'w',encoding='utf-8')
for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    outputs.write(line_seg + '\n')
outputs.close()
inputs.close()


from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary


train = []

fp = codecs.open('result.txt','r',encoding='utf8')
for line in fp:
    if line != '':
        line = line.split()
        train.append([w for w in line])

dictionary = corpora.Dictionary(train)
# corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
corpus = [dictionary.doc2bow(text) for text in train]

lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=1, passes=60)
# num_topics：主题数目
# passes：训练伦次
# num_words：每个主题下输出的term的数目

for topic in lda.print_topics(num_words = 40):
    termNumber = topic[0]
    print(topic[0], ':', sep='')
    listOfTerms = topic[1].split('+')
    for term in listOfTerms:
        listItems = term.split('*')
        print('  ', listItems[1], '(', listItems[0], ')', sep='')
