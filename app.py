from flask import Flask, render_template
from Enterprise.controller.enterprise import enterprise
from Enterprise.controller.topics import topics_con
from Enterprise.controller.summary import summary_con

app = Flask(__name__) # 确定APP的启动路径
app.register_blueprint(enterprise,url_prefix='/enterprise')
app.register_blueprint(topics_con,url_prefix='/topic')
app.register_blueprint(summary_con,url_prefix='/summary')

'''
from flask import request
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from Enterprise.glo import Glo
from Enterprise.service.get_data import loadData
from Enterprise.service.interpersonal_network import InterpersonalNetwork
from Enterprise.service.choose import classify
from Enterprise.service.process import words_tokenize
from Enterprise.service.topic import calLda
from Enterprise.service.docs import get_summary
from Enterprise.service.key_words import cal_doc_keyWords

# 读取MongoDB数据库内容
title, from_email, to_email, splits, doc, file_list,doc_list = loadData()
cluster = {}
cluster_topics = {}
doc_keyWords = []
summary=[]
# sklearn：分词函数
vectorizer = CountVectorizer(min_df=2,tokenizer=words_tokenize,lowercase=False)  # 将文本中的词转换成词频矩阵，至少出现两次的来生成文本表示向量
#vectorizer = CountVectorizer(min_df=2)
transformer = TfidfTransformer()  # 统计每个词语的TF-IDF权值
X = vectorizer.fit_transform(file_list)
tfidf = transformer.fit_transform(X)
word = vectorizer.get_feature_names()  # 获取词袋模型中词语
weight = tfidf.toarray()  # 计算TF-IDF权重

@app.route('/')
def dir():
    return render_template('dir.html')


@app.route('/drawChart', methods=['GET'])
def showChart():
    date = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    number = [820, 932, 901, 934, 1290, 1330, 1320]
    return jsonify({'date': date, 'number': number})


@app.route('/getUserName', methods=['GET', 'POST'])
def Try():
    userID = request.form.get('id')
    return 'Nie Wentao'


@app.route('/choose',methods=['POST'])
def choose():
    choose=request.form.get('func')
    if choose=='category':
        if(len(cluster)==0):
            classify(file_list, weight,cluster)
        show = {}
        for clu in cluster.items():
            show[clu[0]] = len(clu[1])
        show = sorted(show.items(), key=lambda x: x[0])
        return render_template('categories.html', show=show)
    else:
        #人际关系网络
        interpersonalNetwork = InterpersonalNetwork()
        for i in range(0, len(from_email)):
            interpersonalNetwork.addNode(from_email[i], to_email[i])
        return render_template('relationship.html')

@app.route('/topics')
def topics():
    cate=request.args.get("category")
    # 对于每一类的文档们将进行如下几步操作：
    if(len(cluster_topics)==0):
        calLda(cluster, file_list, cluster_topics)
        print("cluster_topics:", cluster_topics)
    print("value:",cluster_topics[int(cate)])
    return render_template('Topics.html', c=cate, value=cluster_topics[int(cate)])

@app.route('/docs')
def docs():
    cate=request.args.get('cate')
    topic=request.args.get('topic')
    
    #计算文章的关键词（存特征值的index）
    #取该文章词类型数量的根号作为关键词数量
    if(len(doc_keyWords)==0):
        cal_doc_keyWords(weight, word, title, doc_keyWords)
        print("doc_keyWords:", np.asarray(doc_keyWords))

    #对文章进行摘要
    if(len(summary)==0):
        get_summary(file_list, doc_keyWords, splits, doc,summary)
        print("summary:",summary)

    # 进行响应值的计算
    docs=cluster_topics[int(cate)][int(topic)][2]
    print("docs:",docs)
    from_list=[]
    to_list=[]
    title_list=[]
    key_list=[]
    summary_list=[]
    doc2_list=[]
    for i in docs:
        from_list.append(from_email[i])
        to_list.append(to_email[i])
        title_list.append(title[i])
        key_list.append(doc_keyWords[i])
        summary_list.append(summary[i])
        doc2_list.append(doc_list[i])
    return render_template('docs.html', cate=cate, topic=topic, len=len(docs), from_list=from_list, to_list=to_list, title_list=title_list, \
                           key_list=key_list, summary_list=summary_list, doc_list=doc2_list)
'''

@app.route('/')
def dir():
    return render_template('dir.html')


if __name__ == '__main__':
    app.run(debug=True,port=80) # 127.0.0.1:回路，自己访问自己
