from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from Enterprise.service.get_data import loadData
from Enterprise.service.process import words_tokenize

class Glo:
    # 全局变量
    # 读取MongoDB数据库内容
    title, from_email, to_email, splits, doc, file_list, doc_list = loadData()
    cluster = {}
    cluster_topics = {}
    doc_keyWords = []
    summary = []

    vectorizer = CountVectorizer(min_df=2, tokenizer=words_tokenize, lowercase=False)  # 将文本中的词转换成词频矩阵，至少出现两次的来生成文本表示向量
    # vectorizer = CountVectorizer(min_df=2)
    transformer = TfidfTransformer()  # 统计每个词语的TF-IDF权值
    X = vectorizer.fit_transform(file_list)
    tfidf = transformer.fit_transform(X)
    word = vectorizer.get_feature_names()  # 获取词袋模型中词语
    weight = tfidf.toarray()  # 计算TF-IDF权重


