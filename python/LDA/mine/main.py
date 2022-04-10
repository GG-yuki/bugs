import pdfplumber
import pandas as pd
def read(path):
    with pdfplumber.open(path) as pdf:
        content = ''
        for i in range(len(pdf.pages)):
            # 读取PDF文档第i+1页
            page = pdf.pages[i]

            # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
            content = content + page_content

doc1 = read(r'1.pdf')
doc2 = read(r'2.pdf')
# 整合文档数据
doc_complete = [doc1, doc2]

import nltk
from nltk.corpus import stopwords

from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]

import gensim
from gensim import corpora

# 创建语料的词语词典，每个单独的词语都会被赋予一个索引
dictionary = corpora.Dictionary(doc_clean)

# 使用上面的词典，将转换文档列表（语料）变成pip install python-Levenshtein DT 矩阵
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# 使用 gensim 来创建 LDA 模型对象
Lda = gensim.models.ldamodel.LdaModel

# 在 DT 矩阵上运行和训练 LDA 模型
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)


# 输出结果
print(ldamodel.print_topics(num_topics=3, num_words=3))
