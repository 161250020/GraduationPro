import re

from sklearn.externals import joblib
import pymongo
import gensim
from gensim import corpora
from flask import jsonify

def clean_str(string):
    string = re.sub(r"[^\u4e00-\u9fff]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = ' '.join(filter(lambda x: x, string.split(' ')))
    return string.strip()

def mail():
    myclient = pymongo.MongoClient('mongodb://localhost:27017')

    mydb = myclient["admin"]
    mycol = mydb["mail"]
    clf = joblib.load('trained.model')

    emails = []
    index = []
    for i in mycol.find({}, {'_id': 1, 'split': 1}):
        email = ''
        for line in i['split']:
            email += ' ' + clean_str(line)
        email = email[1:]
        emails.append(email)
    return emails

def LDA(doc_list):
    # 2.形成标准gensim语料
    texts = [[word for word in doc.lower().split()] for doc in doc_list]
    # print(len(texts))
    # print(texts[0])

    # 3.建立语料库corpus（单词标记化）
    dictionary = corpora.Dictionary(texts)  # id -> word
    corpus = [dictionary.doc2bow(text) for text in texts]

    # 4.建立LDA模型(点到驼峰表达式才是要用的类) 先人工设定20个主题
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
    list = []
    for i in range(20):
        list.append(lda.show_topic(i,topn=5))
        print('topic = ' + str(i) + '  ' + lda.print_topic(i, topn=5))  # 主题i的常用的topn个词
        print('----------------------------------------------')
    for i in range(0,len(list)):
        print("topic", i)
        for keyword in list[i]:
            print("    ",keyword[0])
    return lda


def main():
    doc_list = mail()  # 形成邮件列表
    lda = LDA(doc_list)  # 主题分类

    # lda.get_document_topics(bow)  # 传入词袋化的文本
    for j in range(100):
        topic_id = lda.get_term_topics(word_id=j)  # 传入词袋化的单词


if __name__ == '__main__':
    main()