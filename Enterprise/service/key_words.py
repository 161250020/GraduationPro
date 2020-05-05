import math
import numpy as np

class Key_words:
    def cal_doc_keyWords(weight, word, title, doc_keyWords):
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