import math

import pymongo
from lda import lda
from pandas.tests.extension.numpy_.test_numpy_nested import np
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from Enterprise.interpersonal_network import InterpersonalNetwork

'''
分词函数，按照空格进行分词
'''
def words_tokenize(text):
    return text.split(' ')


'''
获得数据库的内容
'''
def loadData():
    # 读取MongoDB数据库内容
    client = pymongo.MongoClient(host='localhost', port=27017)
    mydb = client["email"]  # 数据库
    collection_names = mydb.collection_names()

    title = []  # 对于每个文章的关键词带上title
    from_email = []
    to_email = []
    splits = []
    doc = []
    file_list = []
    doc_list = []
    for collection_name in collection_names:
        mycollection = mydb["{}".format(collection_name)]
        data = mycollection.find({}, {'_id': 0, 'title': 1, 'from': 1, 'to': 1, 'doc': 1, 'split': 1})
        for d in data:
            title.append(d['title'])
            from_email.append(d['from'])
            to_email.append(d['to'])
            splits.append(d['split'])
            doc.append(d['doc'])
            file = ''
            for sentence in d['split']:
                file = file + sentence + ' '
            file_list.append(file)
            document=''
            for sentence in d['doc']:
                document=document+sentence
            doc_list.append(document)
    print("title:", len(title))
    # print("doc:",np.asarray(doc))
    # print("file_list:",file_list)
    return title,from_email,to_email,splits,doc,file_list,doc_list

'''
获得k-means的k：符合标准：inertia,dunn index
'''
def fin_k(file_list,weight):
    fin_n = 1  # 最终簇数量，小于等于：根号n
    inertias = []  # 簇内距离：越小越好
    dunn_index = []  # 簇间距离：越大越好
    finish1 = False  # 是否结束簇数量的尝试：inertia
    finish2 = False  # 是否结束簇数量的尝试：dunn index
    cur_n = 1  # n=1,2,3,4,5,6,...直到inertia/dunn index的变化不再是剧烈的
    while True:
        if cur_n <= len(file_list):
            kmeans = KMeans(n_clusters=cur_n, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
            kmeans.fit(weight)
            # 计算inertia
            inertias.append(kmeans.inertia_)
            # 判断inertia的变化是否是剧烈的：inertias倒数2个值a,b，当b/a>=0.99即符合要求
            if len(inertias) >= 2:
                if inertias[-1] / inertias[-2] >= 0.99:
                    finish1 = True
                    fin_n = cur_n
                    # print("finish1:fin_n:",fin_n)

            '''
            #计算dunn index
            min_inter_cluster_distance=float('inf')#计算簇间距离（欧氏距离）的最小值
            kmeans.cluster_centers_#簇心们
            #max_intra_cluster_distance=#簇内距离（欧氏距离）的最大值
            '''
            i = 0
            cluster = {}
            while i < len(file_list):
                tmp = cluster.get(kmeans.labels_[i], [])
                tmp.append(i)
                cluster[kmeans.labels_[i]] = tmp
                i += 1
            intra_clusters = kmeans.cluster_centers_  # 所有的簇心
            # print("cluster_centers:",intra_clusters)
            # 计算所有簇心簇内距离和是否等于自带的inertia：大致类似
            sum = 0
            max_intra_cluster_distance = 0  # 分母：最大簇内距离
            for i in range(len(intra_clusters)):  # 对于每一个簇心
                intra_cluster_distance = 0  # 计算簇内距离
                for j in range(len(cluster[i])):  # 对于该簇心对应的分类的每一个文章的index
                    v = weight[cluster[i][j]]
                    w = intra_clusters[i]
                    # print("v:",v)
                    # print("w:",w)
                    square = [(v[k] - w[k]) ** 2 for k in range(len(v))]
                    squares = 0
                    for l in square:
                        squares += l
                    dis = squares ** 0.5
                    intra_cluster_distance += dis
                sum += intra_cluster_distance
                # print("pre_max_intra_cluster_distance:",max_intra_cluster_distance)
                max_intra_cluster_distance = max(max_intra_cluster_distance, intra_cluster_distance)
                # print("max_intra_cluster_distance:",max_intra_cluster_distance)
            # print("sum:",sum)
            # print("kmeans.inertia_:",kmeans.inertia_)
            min_inter_cluster_distance = float('inf')  # 分子：最小簇间距离
            for i in range(len(intra_clusters)):
                for j in range(i + 1, len(intra_clusters)):
                    sub = [w_k - v_k for w_k, v_k in zip(intra_clusters[i], intra_clusters[j])]
                    # print("sub:",sub)
                    square = [sub_k ** 2 for sub_k in sub]
                    # print("square:",square)
                    tmp_sum = 0
                    for k in square:
                        tmp_sum += k
                    tmp_inter_cluster_distance = tmp_sum ** 0.5
                    min_inter_cluster_distance = min(min_inter_cluster_distance, tmp_inter_cluster_distance)
            # print("min_inter_cluster_distance:",min_inter_cluster_distance)
            dunn = min_inter_cluster_distance / max_intra_cluster_distance
            dunn_index.append(dunn)

            '''
            # 判断dunn index的变化是否是剧烈的
            '''
            if len(dunn_index) >= 2:
                if dunn_index[- 1] / dunn_index[- 2] >= 0.99:  # 包括[...,a,b]：b/a>=0.9以及b>a的情况
                    finish2 = True
                    fin_n = cur_n
                    # print("finish2:fin_n:",fin_n)

            if finish1 and finish2:
                break
            cur_n += 1
        else:
            fin_n = int(math.sqrt(len(file_list)))
            break
    fin_n = min(fin_n, int(math.sqrt(len(file_list))))
    print("fin_n:", fin_n)
    return fin_n

if __name__=='__main__':
    #读取MongoDB数据库内容
    title, from_email, to_email, splits, doc, file_list, doc_list=loadData()

    '''
    人际关系网络
    '''
    interpersonalNetwork = InterpersonalNetwork()
    for i in range(0,len(from_email)):
        interpersonalNetwork.addNode(from_email[i],to_email[i])
    # 测试
    print("人际关系网络:",interpersonalNetwork.set)
    print("人际关系网络:",interpersonalNetwork.countEgdes)
    print("人际关系网络:",interpersonalNetwork.outDegree)
    print("人际关系网络:",interpersonalNetwork.inDegree)

    '''
    sklearn自带分词：
    '''
    vectorizer = CountVectorizer(min_df=2)  # 将文本中的词转换成词频矩阵，至少出现两次的来生成文本表示向量
    transformer = TfidfTransformer()  # 统计每个词语的TF-IDF权值
    X = vectorizer.fit_transform(file_list)
    tfidf = transformer.fit_transform(X)
    word = vectorizer.get_feature_names()  # 获取词袋模型中词语
    weight = tfidf.toarray()  # 计算TF-IDF权重
    # print("词袋模型：", word)
    # print("TF-IDF权重：",weight)

    '''
    第一次分类：进行K-means聚类
    '''
    fin_n=fin_k(weight)

    # 使用合适的簇数量进行kmeans的计算
    fin_kmeans = KMeans(n_clusters=fin_n, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
    fin_kmeans.fit(weight)

    # 对文档进行分类
    i = 0
    cluster = {}
    while i < len(file_list):
        tmp = cluster.get(fin_kmeans.labels_[i], [])
        tmp.append(i)
        cluster[fin_kmeans.labels_[i]] = tmp
        i += 1
    print("分类：", cluster)

    # 对于每一类的文档们将进行如下几步操作：
    cluster_topics = {}
    for clu in cluster.items():
        '''
        对每一类进行lda的主题分类
        计算主题关键词
        '''
        corpus = []
        for file_index in clu[1]:
            corpus.append(file_list[file_index])
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
            for i in range(1, len(corpus)+1):
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
    print("cluster_topics:", np.asarray(cluster_topics))

    '''
    计算文章的关键词（存特征值的index）
    取该文章词类型数量的根号作为关键词数量
    '''
    doc_keyWords = []
    for i in range(len(weight)):
        list_word = weight[i]
        word_clu_num = 0  # 关键词数量
        for j in range(len(list_word)):
            if list_word[j] != 0:
                word_clu_num += 1
        word_clu_num = int(math.sqrt(word_clu_num))
        distIndexArr = np.argsort(weight[i])
        topN_index = distIndexArr[:-(word_clu_num + 1):-1]  # top n 的indexs
        topN_words=np.asarray(word)[topN_index] # top n 的words---关键词
        # print("topic_word:",topN_words)
        topN_words2=[l for l in topN_words]
        topN_words2=topN_words2+title[i].split(' ')
        # print("title[i].split:",title[i].split(' '))
        doc_keyWords.append(topN_words2)
    print("doc_keyWords:", np.asarray(doc_keyWords))

    '''
    对文章进行摘要
    '''
    summary=[]
    threshold_value=5 # 门槛值：5
    for i in range(len(file_list)):# 对于每一个文章而言
        # 该篇文章对应的关键词
        key_words=doc_keyWords[i]
        # 该文章对应的三个属性
        sub_split=splits[i]
        sub_doc=doc[i]
        sub_file=file_list[i]
        cluster_value=[]# 存储每一句话的簇的重要性
        for j in range(len(sub_split)):# 对于该文章的每一句话
            # 计算该句子的簇的重要性
            v=0 # 初始化该句子重要性
            split_words=sub_split[j].split(' ')
            for k in range(len(split_words)):# 对于每一句话的每个单词
                if split_words[k] in key_words:# 第一个单词为关键词
                    key_word_num=1# 该句的关键词个数
                    cluster_len=threshold_value+2# 簇的长度
                    last_key_word=False
                    #往后数门槛值+1个单词
                    tmp_split_words=split_words[k+1:k+2+threshold_value]
                    tmp_split_words_len=len(tmp_split_words)
                    for w in range(0,tmp_split_words_len):
                        last_word=tmp_split_words.pop()
                        if last_word in key_words:
                            last_key_word=True
                            key_word_num+=1
                        if not last_key_word:
                            cluster_len-=1
                    v=max(v,key_word_num*key_word_num/cluster_len)
            cluster_value.append(v)
        #print("cluster_value:",cluster_value)
        # 选出簇的重要性排名靠前的作为该篇文章的摘要
        n=int(math.sqrt(len(sub_split)))# 摘要的句子的个数：开根号句子的长度
        #print("n:",n)
        distIndexArr=np.argsort(cluster_value)
        topN_index=distIndexArr[:-(n+1):-1]
        topN_index.sort()# 摘要的句子按照句子在原文中的顺序进行摘要
        #print("topN_index:",topN_index)
        sub_summary=''# 该篇文章的摘要
        for j in topN_index:
            sub_summary=sub_summary+sub_doc[j]
            #print("sub_summary:",sub_summary)
        summary.append(sub_summary)
    print("summary:",np.asarray(summary))
