from flask import Blueprint, request, jsonify
from Enterprise.model.glo import Glo
from Enterprise.service.doc_summary import DocSummary
from Enterprise.service.key_words import KeyWords
import numpy as np

summary_con = Blueprint('summary', __name__)


@summary_con.route('/')
def docs():
    cate = request.values.get('category')[2:]
    topic = request.values.get('topic')[2:]

    # 计算文章的关键词（存特征值的index）
    # 取该文章词类型数量的根号作为关键词数量
    if len(Glo.doc_keywords) == 0:
        KeyWords.cal_doc_keywords(Glo.weight, Glo.word, Glo.doc_keywords)
    print("doc_keyWords:", np.asarray(Glo.doc_keywords))

    # 对文章进行摘要
    if len(Glo.summary) == 0:
        DocSummary.get_summary(Glo.doc_keywords, Glo.splits, Glo.doc, Glo.summary)
    print("summary:", Glo.summary)

    # 进行响应值的计算
    docs = Glo.cluster_topics[int(cate)][int(topic)][2]
    print("docs:", docs)
    ret_data = []
    for i in docs:
        ret_data.append({
            "title": Glo.title[i],
            "from": Glo.from_email[i],
            "to": Glo.to_email[i],
            "keyword": Glo.doc_keywords[i],
            "abstract": Glo.summary[i],
            "docs": Glo.doc_list[i]
        })
    # print(ret_data)
    return jsonify(ret_data)
