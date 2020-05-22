from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class FeatureExtraction:
    """对邮件文本进行特征提取"""

    @staticmethod
    def feature_extraction(file_list):
        vectorizer = CountVectorizer()  # 将文本中的词转换成词频矩阵
        transformer = TfidfTransformer()  # 统计每个词语的TF-IDF权值
        X = vectorizer.fit_transform(file_list)
        tfidf = transformer.fit_transform(X)
        word = vectorizer.get_feature_names()  # 获取词袋模型中词语
        weight = tfidf.toarray()  # 计算TF-IDF权重
        return word, weight
