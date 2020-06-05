import numpy as np

def cal_doc_keywords(weight, word, doc_keywords):
    for i in range(len(weight)):
        list_word = weight[i]

        # 关键词数量
        word_clu_num = 0
        ...

        # 获取关键词：top n 的words
        distIndexArr = np.argsort(weight[i])
        topN_index = distIndexArr[:-(word_clu_num + 1):-1]  # top n 的indexs
        topN_words = np.asarray(word)[topN_index]  # top n 的words
        topN_words2 = [l for l in topN_words]
        doc_keywords.append(topN_words2)


