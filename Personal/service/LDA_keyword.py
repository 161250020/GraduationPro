import re

import json
import gensim
from gensim import corpora
import Personal.dao.db_connector as db
from _datetime import datetime

def clean_str(string):
    string = re.sub(r"[^\u4e00-\u9fff]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = ' '.join(filter(lambda x: x, string.split(' ')))
    return string.strip()

def all_mail():
    emails = db.get_all_email()
    return LDA(emails)

def mail_by_date(et:datetime,ct:datetime):
    emails = db.get_mail_by_date(et,ct)
    return LDA(emails)

def LDA(doc_list):
    # 2.形成标准gensim语料
    texts = [[word for word in doc.lower().split()] for email, doc in doc_list]
    # print(len(texts))
    # print(texts[0])

    # 3.建立语料库corpus（单词标记化）
    dictionary = corpora.Dictionary(texts)  # id -> word
    corpus = [dictionary.doc2bow(text) for text in texts]

    # 4.建立LDA模型(点到驼峰表达式才是要用的类) 先人工设定5个主题
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
    lda.save('lda.model')
    #list = []
    #    list.append(lda.show_topic(i,topn=5))
    #    print('topic = ' + str(i+1) + '  ' + lda.print_topic(i, topn=5))  # 主题i的常用的topn个词
    #    print('----------------------------------------------')
    #for i in range(0,len(list)):
    #    print("topic", i)
    #    for keyword in list[i]:
    #        print("    ",keyword[0])
    new_vec = []
    result = []
    temp = []
    for i in range(0, 5):
        result.append(temp)
    for email, i in doc_list:
        new_vec.append(dictionary.doc2bow(str(i).split(' ')))
    for j in lda.print_topics(num_topics=5, num_words=10):
        for i, n in enumerate(new_vec):
            for d in lda[n]:
                if j[0]==d[0] and d[1]>=0.6:
                    #print(str(i)+'属于的主题：'+str(j[0])+'主题概率：'+str(d[1])+'\n')
                    result[j[0]].append([doc_list[i][0],d[1]])
    return json.dumps(result)

def main():
    doc_list = all_mail()  # 形成邮件列表
    LDA(doc_list)  # 主题分类

if __name__ == '__main__':
    main()