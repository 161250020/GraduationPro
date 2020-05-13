import math
import numpy as np


class DocSummary:
    @staticmethod
    def get_summary(doc_keywords, splits, doc, summary):
        threshold_value = 5  # 门槛值：5
        for i in range(len(splits)):  # 对于每篇文章而言
            key_words = doc_keywords[i]  # 该篇文章对应的关键词
            sub_split = splits[i]
            sub_doc = doc[i]

            # 计算每句话的重要性
            cluster_value = []
            DocSummary.__sentence_value(sub_split, key_words, threshold_value, cluster_value)  # 存储每一句话的重要性
            # print("cluster_value:",cluster_value)

            # 选出簇的重要性排名靠前的作为该篇文章的摘要
            n = int(math.sqrt(len(sub_split)))  # 摘要的句子的个数：开根号句子的个数
            # print("n:",n)
            dist_index_arr = np.argsort(cluster_value)
            topn_index = dist_index_arr[:-(n + 1):-1]
            topn_index.sort()  # 摘要的句子按照句子在原文中的顺序进行摘要
            # print("topN_index:",topN_index)
            sub_summary = ''  # 该篇文章的摘要
            for j in topn_index:
                sub_summary = sub_summary + sub_doc[j]
                # print("sub_summary:",sub_summary)
            summary.append(sub_summary)

    @staticmethod
    def __sentence_value(sub_split, key_words, threshold_value, cluster_value):
        for j in range(len(sub_split)):  # 对于该文章的每一句话
            # 计算该句子的簇的重要性
            v = 0  # 初始化该句子重要性
            split_words = sub_split[j].split(' ')
            for k in range(len(split_words)):  # 对于每一句话的每个词
                if split_words[k] in key_words:  # 第一个词为关键词
                    key_word_num = 1  # 该句的关键词个数
                    cluster_len = threshold_value + 2  # 簇的长度
                    last_key_word = False
                    # 往后数门槛值+1个词
                    if (len(split_words) > (threshold_value + 2)):
                        tmp_split_words = split_words[k + 1:k + 2 + threshold_value]
                    else:
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
