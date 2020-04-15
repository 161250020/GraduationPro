import math
import numpy as np

def cal_doc_keyWords(weight,word,title,doc_keyWords):
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

def summary(file_list,doc_keyWords,splits,doc):
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
            if (len(split_words) > (threshold_value + 2)):
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