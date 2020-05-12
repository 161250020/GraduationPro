import math
import numpy as np


class KeyWords:
    @staticmethod
    def cal_doc_keywords(weight, word, title, doc_keywords):
        for i in range(len(weight)):
            list_word = weight[i]

            # 关键词数量
            word_clu_num = 0
            for j in range(len(list_word)):
                if list_word[j] != 0:
                    word_clu_num += 1
            word_clu_num = int(math.sqrt(word_clu_num))

            # 获取关键词：top n 的words 和 邮件的title
            distIndexArr = np.argsort(weight[i])
            topN_index = distIndexArr[:-(word_clu_num + 1):-1]  # top n 的indexs
            topN_words = np.asarray(word)[topN_index]  # top n 的words
            topN_words2 = [l for l in topN_words]
            topN_words2 = topN_words2 + title[i].split(' ')
            doc_keywords.append(topN_words2)
