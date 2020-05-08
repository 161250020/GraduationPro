import gensim
import lda
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class Topics_analyse:
    def calLda(cluster, file_list, cluster_topics):
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

            # 主题-文档分布
            doc_topic = model.doc_topic_
            for j in range(len(corpus)):
                topic_index = doc_topic[j].argmax()
                tmp2 = tmp[topic_index][2]
                tmp2.append(clu[1][j])
                tmp[topic_index][2] = tmp2
            cluster_topics[clu[0]] = tmp

    def calLda2(cluster, file_list, cluster_topics):
        pass
