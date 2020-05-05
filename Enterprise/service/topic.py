import gensim
import lda
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class Topics_analyse:
    def calLda(cluster, file_list, cluster_topics):
        for clu in cluster.items():
            '''
            对每一类进行lda的主题分类
            计算主题关键词
            '''
            corpus = []
            for file_index in clu[1]:
                corpus.append(file_list[file_index])
            # tmp_vectorizer = CountVectorizer(min_df=2,tokenizer=words_tokenize,lowercase=False)
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
                    # 计算不同topic个数的LDA
                    n_topics = i  # topic个数
                    tmp_lda = LatentDirichletAllocation(n_components=i)
                    tmp_lda.fit(np.asarray(tmp_nums))

                    # 困惑度
                    perplexity_list.append(tmp_lda.perplexity(tmp_nums))
                    # 判断是否结束困惑度计算：
                    # 两次计算困惑度比值：后/前>=0.95；后>=前；时结束
                    if (len(perplexity_list) >= 2):
                        if (((perplexity_list[-1] / perplexity_list[-2]) >= 0.95) or (
                                perplexity_list[-1] >= perplexity_list[-2])):
                            break

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

    def calLda2(cluster, file_list, cluster_topics):
        pass
