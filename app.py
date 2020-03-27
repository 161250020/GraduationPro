import math, lda
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from flask import Flask, render_template, request
from Enterprise.process import loadData, fin_k, words_tokenize
from Enterprise.interpersonal_network import InterpersonalNetwork

# @app.route('/') # 路由
# return render_template('index.html') # 把HTML文件读进来，再交给浏览器
app = Flask(__name__) # 确定APP的启动路径

# 读取MongoDB数据库内容
title, from_email, to_email, splits, doc, file_list,doc_list = loadData()
cluster = {}
cluster_topics = {}
doc_keyWords = []
summary=[]
'''
sklearn：分词函数
'''
#vectorizer = CountVectorizer(min_df=2,tokenizer=words_tokenize,lowercase=False)  # 将文本中的词转换成词频矩阵，至少出现两次的来生成文本表示向量
vectorizer = CountVectorizer(min_df=2)
transformer = TfidfTransformer()  # 统计每个词语的TF-IDF权值
X = vectorizer.fit_transform(file_list)
tfidf = transformer.fit_transform(X)
word = vectorizer.get_feature_names()  # 获取词袋模型中词语
weight = tfidf.toarray()  # 计算TF-IDF权重
# print("词袋模型：", word)
# print("TF-IDF权重：", weight)

@app.route('/')
def dir():
    return render_template('dir.html')

@app.route('/choose',methods=['POST'])
def choose():
    choose=request.form.get('func')
    if choose=='category':
        if(len(cluster)==0):
            '''
            第一次分类：进行K-means聚类
            '''
            # 使用合适的簇数量进行kmeans的计算
            fin_n = fin_k(file_list, weight)
            fin_kmeans = KMeans(n_clusters=fin_n, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
            fin_kmeans.fit(weight)
            # 对文档进行分类
            i = 0
            while i < len(file_list):
                tmp = cluster.get(fin_kmeans.labels_[i], [])
                tmp.append(i)
                cluster[fin_kmeans.labels_[i]] = tmp
                i += 1
            print("分类：", cluster)
        show = {}
        for clu in cluster.items():
            show[clu[0]] = len(clu[1])
        show = sorted(show.items(), key=lambda x: x[0])
        return render_template('categories.html',show=show)
    else:
        '''
        人际关系网络
        '''
        interpersonalNetwork = InterpersonalNetwork()
        for i in range(0, len(from_email)):
            interpersonalNetwork.addNode(from_email[i], to_email[i])
        # 测试
        print("人际关系网络:", interpersonalNetwork.set)
        print("人际关系网络:", interpersonalNetwork.countEgdes)
        print("人际关系网络:", interpersonalNetwork.outDegree)
        print("人际关系网络:", interpersonalNetwork.inDegree)
        return render_template('relationship.html')

@app.route('/topics')
def topics():
    cate=request.args.get("category")
    # print("category:"+cate)

    # 对于每一类的文档们将进行如下几步操作：
    if(len(cluster_topics)==0):
        for clu in cluster.items():
            '''
            对每一类进行lda的主题分类
            计算主题关键词
            '''
            corpus = []
            for file_index in clu[1]:
                corpus.append(file_list[file_index])
            #tmp_vectorizer = CountVectorizer(min_df=2,tokenizer=words_tokenize,lowercase=False)
            tmp_vectorizer = CountVectorizer(min_df=2)
            tmp_X = tmp_vectorizer.fit_transform(corpus)
            tmp_word = tmp_vectorizer.get_feature_names()
            # print("tmp_word:", tmp_word)
            tmp_analyze = tmp_vectorizer.build_analyzer()
            tmp_nums = tmp_X.toarray()
            # print("tmp_nums:", tmp_nums)

            # 计算lda的n的值
            n_topics = min(len(corpus), 1)  # 取值范围：1，...，len(corpus)，1/0个文章，topic数量即为该数量
            perplexity_list = []  # 不同主题数量的困惑度
            if (len(corpus) > 1):
                for i in range(1, len(corpus) + 1):
                    n_topics = i
                    # print("tmp_n_topics", n_topics)
                    # 训练模型
                    tmp_lda = LatentDirichletAllocation(n_components=i)
                    tmp_lda.fit(np.asarray(tmp_nums))
                    # 困惑度
                    perplexity_list.append(tmp_lda.perplexity(tmp_nums))
                    # 判断是否结束困惑度计算：
                    # 两次计算困惑度比值：后/前>=0.95；后>=前；时结束
                    if (len(perplexity_list) >= 2):
                        if ((perplexity_list[-1] / perplexity_list[-2]) >= 0.95):
                            break
                        if (perplexity_list[-1] >= perplexity_list[-2]):
                            break
            # print("n_topics:", n_topics)

            # 训练模型
            model = lda.LDA(n_topics=n_topics)
            model.fit(np.asarray(tmp_nums))
            topic_word = model.topic_word_  # 生成主题以及主题中词的分布
            # print("topic-word:\n", topic_word)
            # 计算主题关键词：取前5个关键词
            n = 5
            tmp = cluster_topics.get(clu[0], [])
            for i, word_weight in enumerate(topic_word):
                distIndexArr = np.argsort(word_weight)
                # print("distIndexArr:",distIndexArr)
                topN_index = distIndexArr[:-(n + 1):-1]
                # print("topN_index:",topN_index)
                topN_words = np.array(tmp_word)[topN_index]
                # print("topN_words:", topN_words)
                # print("topN_words:",topN_words)
                tmp2 = []
                tmp2.append(i)
                tmp2.append(topN_words)
                tmp2.append([])
                tmp.append(tmp2)
            # 文档-主题分布
            doc_topic = model.doc_topic_
            for j in range(len(corpus)):
                topic_index = doc_topic[j].argmax()
                tmp2 = tmp[topic_index][2]
                tmp2.append(clu[1][j])
                tmp[topic_index][2] = tmp2
            cluster_topics[clu[0]] = tmp
        print("cluster_topics:", cluster_topics)
    print("value:",cluster_topics[int(cate)])
    return render_template('Topics.html',c=cate, value=cluster_topics[int(cate)])

@app.route('/docs')
def docs():
    cate=request.args.get('cate')
    topic=request.args.get('topic')
    # print("cate:",cate)
    # print("topic:",topic)
    '''
    计算文章的关键词（存特征值的index）
    取该文章词类型数量的根号作为关键词数量
    '''
    if(len(doc_keyWords)==0):
        for i in range(len(weight)):
            list_word = weight[i]
            word_clu_num = 0  # 关键词数量
            for j in range(len(list_word)):
                if list_word[j] != 0:
                    word_clu_num += 1
            word_clu_num = int(math.sqrt(word_clu_num))
            distIndexArr = np.argsort(weight[i])
            topN_index = distIndexArr[:-(word_clu_num + 1):-1]  # top n 的indexs
            topN_words = np.asarray(word)[topN_index]  # top n 的words---关键词
            # print("topic_word:",topN_words)
            topN_words2 = [l for l in topN_words]
            topN_words2 = topN_words2 + title[i].split(' ')
            # print("title[i].split:",title[i].split(' '))
            doc_keyWords.append(topN_words2)
        print("doc_keyWords:", np.asarray(doc_keyWords))

    '''
    对文章进行摘要
    '''
    if(len(summary)==0):
        threshold_value = 5  # 门槛值：5
        for i in range(len(file_list)):  # 对于每一个文章而言
            # 该篇文章对应的关键词
            key_words = doc_keyWords[i]
            # 该文章对应的三个属性
            sub_split = splits[i]
            sub_doc = doc[i]
            cluster_value = []  # 存储每一句话的簇的重要性
            for j in range(len(sub_split)):  # 对于该文章的每一句话
                # 计算该句子的簇的重要性
                v = 0  # 初始化该句子重要性
                split_words = sub_split[j].split(' ')
                if(len(split_words)>(threshold_value+2)):
                    for k in range(len(split_words)):  # 对于每一句话的每个单词
                        if split_words[k] in key_words:  # 第一个单词为关键词
                            key_word_num = 1  # 该句的关键词个数
                            cluster_len = threshold_value + 2  # 簇的长度
                            last_key_word = False
                            # 往后数门槛值+1个单词
                            tmp_split_words = split_words[k + 1:k + 2 + threshold_value]
                            tmp_split_words_len = len(tmp_split_words)
                            for w in range(0, tmp_split_words_len):
                                last_word = tmp_split_words.pop()
                                if last_word in key_words:
                                    last_key_word = True
                                    key_word_num += 1
                                if not last_key_word:
                                    cluster_len -= 1
                            v = max(v, key_word_num * key_word_num / cluster_len)
                else:
                    for k in range(len(split_words)):  # 对于每一句话的每个单词
                        if split_words[k] in key_words:  # 第一个单词为关键词
                            key_word_num = 1  # 该句的关键词个数
                            cluster_len = threshold_value + 2  # 簇的长度
                            last_key_word = False
                            # 往后数门槛值+1个单词
                            tmp_split_words = split_words[k + 1:]
                            tmp_split_words_len = len(tmp_split_words)
                            for w in range(0, tmp_split_words_len):
                                last_word = tmp_split_words.pop()
                                if last_word in key_words:
                                    last_key_word = True
                                    key_word_num += 1
                                if not last_key_word:
                                    cluster_len -= 1
                            v = max(v, key_word_num * key_word_num / cluster_len)
                cluster_value.append(v)
            # print("cluster_value:",cluster_value)
            # 选出簇的重要性排名靠前的作为该篇文章的摘要
            n = int(math.sqrt(len(sub_split)))  # 摘要的句子的个数：开根号句子的个数
            # print("n:",n)
            distIndexArr = np.argsort(cluster_value)
            topN_index = distIndexArr[:-(n + 1):-1]
            topN_index.sort()  # 摘要的句子按照句子在原文中的顺序进行摘要
            # print("topN_index:",topN_index)
            sub_summary = ''  # 该篇文章的摘要
            for j in topN_index:
                sub_summary = sub_summary + sub_doc[j]
                # print("sub_summary:",sub_summary)
            summary.append(sub_summary)
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
    return render_template('docs.html',cate=cate,topic=topic,len=len(docs),from_list=from_list,to_list=to_list,title_list=title_list,\
                           key_list=key_list,summary_list=summary_list,doc_list=doc2_list)

'''
@app.route('/g',methods=['GET','POST'])
def pg():
    if request.method=='GET':
        name = request.args.get("name")
        print("form-get-name:", name)
        return render_template('index.html')
    if request.method=='POST':
        name = request.form.get("name")
        print("form-post-name:", name)
        return render_template('index.html')

@app.route('/p', methods=['POST'])
def p():
    return render_template('index2.html',test='123')
'''
if __name__ == '__main__':
    app.run(debug=True,port=80) # 127.0.0.1:回路，自己访问自己
