from Enterprise.dao.get_data import GetData


class Glo:
    # 全局变量
    # 读取MongoDB数据库内容
    title, from_email, to_email, splits, doc, file_list, doc_list = GetData.load_data()

    # 邮件文本特征提取结果
    word = []  # 获取词袋模型中词语
    weight = []  # 计算TF-IDF权重

    # 邮件聚类结果
    cluster = {}  # cluster数据结构：{类0:[文章0, ...], 类1:[文章2, ...], ...}

    # 对每类邮件进行主题分类
    cluster_topics = {}  # cluster_topics数据结构：{类0:[LdaClusterInfo型数据, ...], 类1:[LdaClusterInfo型数据, ...]}

    # 邮件关键词和主题摘要
    doc_keywords = []
    summary = []
