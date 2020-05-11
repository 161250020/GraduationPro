import lda
import math
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import gensim
from gensim import corpora

class Topics_analyse:
    def calLda2(cluster, file_list, cluster_topics):
        for clu in cluster.items():
            # 单独计算该类邮件的特征矩阵等数据
            corpus = []
            for file_index in clu[1]:
                corpus.append(file_list[file_index])
            tmp_vectorizer = CountVectorizer(min_df=2)
            tmp_X = tmp_vectorizer.fit_transform(corpus)
            tmp_word = tmp_vectorizer.get_feature_names()
            tmp_analyze = tmp_vectorizer.build_analyzer()
            tmp_nums = tmp_X.toarray()
            print("tmp_nums:",tmp_nums)

            # 计算lda的n的值
            n_topics = min(len(corpus), 1)  # 取值范围：1，...，len(corpus)，1/0个文章，topic数量即为该数量
            perplexity_list = []  # 不同主题数量的困惑度存储
            if (len(corpus) > 1):
                for i in range(1, len(corpus) + 1):
                    n_topics = i  # topic个数
                    tmp_lda = LatentDirichletAllocation(n_components=i)
                    tmp_lda.fit(np.asarray(tmp_nums))

                    # 困惑度
                    perplexity_list.append(tmp_lda.perplexity(tmp_nums))

                    # 判断是否为该主题个数：
                    # 两次计算困惑度比值：后/前>=0.95 或 后>=前 时结束
                    if (len(perplexity_list) >= 2):
                        if (((perplexity_list[-1] / perplexity_list[-2]) >= 0.95) or (perplexity_list[-1] >= perplexity_list[-2])):
                            break

            # 训练模型
            model = lda.LDA(n_topics=n_topics)
            model.fit(np.asarray(tmp_nums))
            topic_word = model.topic_word_  # 生成主题以及主题中词的分布

            # 计算主题关键词：取前5个关键词
            n = 5
            tmp = cluster_topics.get(clu[0], [])
            for i, word_weight in enumerate(topic_word):
                distIndexArr = np.argsort(word_weight)
                topN_index = distIndexArr[:-(n + 1):-1]
                topN_words = np.array(tmp_word)[topN_index]
                # tmp2数据结构：[主题编号i, [主题关键词1,...], [分配到该主题的文章编号1,...]]
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

    def calLda(cluster, file_list, cluster_topics):
        for clu in cluster.items():
            tmp_file_list = []
            for file_index in clu[1]:
                tmp_file_list.append(file_list[file_index])

            # 形成标准gensim语料
            file_word_list = [[word for word in file.lower().split()] for file in tmp_file_list]

            # 建立语料库corpus
            dictionary = corpora.Dictionary(file_word_list)  # 构建模型词典：[特征词1, ...]
            # print("dic:", dictionary)
            corpus = [dictionary.doc2bow(text) for text in file_word_list]  # [[(特征词在字典中的位置, 特征词在该本文中的数量), ...],...]

            # 计算lda的n的值
            n_topics = min(len(corpus), 1)  # 取值范围：1，...，len(corpus)，1/0个文章，topic数量即为该数量
            perplexity_list = []  # 不同主题数量的困惑度存储
            if len(corpus) > 1:
                for i in range(1, len(corpus) + 1):
                    n_topics = i  # topic个数
                    tmp_lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topics)

                    # 困惑度
                    perplexity_list.append(Topics_analyse.__perplexity(tmp_lda,corpus,dictionary,len(dictionary.keys()),n_topics))

                    # 判断是否为该主题个数：
                    # 两次计算困惑度比值：后/前>=0.99 或 后>=前 时结束
                    if len(perplexity_list) >= 2:
                        if perplexity_list[-1] >= perplexity_list[-2]:
                            n_topics -= 1
                            break
                        if (perplexity_list[-1] / perplexity_list[-2]) >= 0.99:
                            break
            print("perplexity list:",perplexity_list)

            # 建立LDA模型
            lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topics)

            # 计算主题关键词：取前5个关键词
            n = 5
            tmp = cluster_topics.get(clu[0], [])
            for i in range(n_topics):
                show_topics=lda.show_topic(i,topn=5)
                topn_words = [w[0] for w in show_topics]
                print("主题前5个关键词：",topn_words)
                # tmp2数据结构：[主题编号i, [主题关键词1,...], [分配到该主题的文章编号1,...]]
                tmp2 = []
                tmp2.append(i)
                tmp2.append(topn_words)
                tmp2.append([])
                tmp.append(tmp2)

            # 主题-文档分布
            for j in range(len(corpus)):
                topic_indexs = lda.get_document_topics(corpus[j])
                topic_indexs_max_pro_index = 0
                for index in range(1,len(topic_indexs)):
                    if topic_indexs[index][1] > topic_indexs[topic_indexs_max_pro_index][1]:
                        topic_indexs_max_pro_index=index
                topic_index=topic_indexs[topic_indexs_max_pro_index][0]
                tmp2 = tmp[topic_index][2]
                tmp2.append(clu[1][j])
                tmp[topic_index][2] = tmp2
            cluster_topics[clu[0]] = tmp

    def __perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
        """calculate the perplexity of a lda-model"""
        # dictionary : {7822:'deferment', 1841:'circuitry',19202:'fabianism'...]
        print('num of testset: %s; size_dictionary: %s; num of topics: %s' % (len(testset), size_dictionary, num_topics))
        prep = 0.0
        prob_doc_sum = 0.0
        topic_word_list = []  # store the probablity of topic-word:[(u'business', 0.010020942661849608),(u'family', 0.0088027946271537413)...]
        for topic_id in range(num_topics):
            topic_word = ldamodel.show_topic(topic_id, size_dictionary)
            dic = {}
            for word, probability in topic_word:
                dic[word] = probability
            topic_word_list.append(dic)
        doc_topics_ist = []  # store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
        for doc in testset:
            doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
        testset_word_num = 0
        for i in range(len(testset)):
            prob_doc = 0.0  # the probablity of the doc
            doc = testset[i]
            doc_word_num = 0  # the num of words in the doc
            for word_id, num in doc:
                prob_word = 0.0  # the probablity of the word
                doc_word_num += num
                word = dictionary[word_id]
                for topic_id in range(num_topics):
                    # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                    prob_topic = doc_topics_ist[i][topic_id][1]
                    prob_topic_word = topic_word_list[topic_id][word]
                    prob_word += prob_topic * prob_topic_word
                prob_doc += math.log(prob_word)  # p(d) = sum(log(p(w)))
            prob_doc_sum += prob_doc
            testset_word_num += doc_word_num
        prep = math.exp(-prob_doc_sum / testset_word_num)  # perplexity = exp(-sum(p(d)/sum(Nd))
        print("the perplexity of this ldamodel is : %s" % prep)
        return prep