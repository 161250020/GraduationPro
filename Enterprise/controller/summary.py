from flask import Blueprint, render_template, request
from Enterprise.glo import Glo
from Enterprise.service.docs import get_summary
from Enterprise.service.key_words import cal_doc_keyWords
import numpy as np

summary_con = Blueprint('summary',__name__)

@summary_con.route('/')
def dir():
    return render_template('dir.html')

@summary_con.route('/docs')
def docs():
    cate = request.args.get('cate')
    topic = request.args.get('topic')

    # 计算文章的关键词（存特征值的index）
    # 取该文章词类型数量的根号作为关键词数量
    if (len(Glo.doc_keyWords) == 0):
        cal_doc_keyWords(Glo.weight, Glo.word, Glo.title, Glo.doc_keyWords)
        print("doc_keyWords:", np.asarray(Glo.doc_keyWords))

    # 对文章进行摘要
    if (len(Glo.summary) == 0):
        get_summary(Glo.file_list, Glo.doc_keyWords, Glo.splits, Glo.doc, Glo.summary)
        print("summary:", Glo.summary)

    # 进行响应值的计算
    docs = Glo.cluster_topics[int(cate)][int(topic)][2]
    print("docs:", docs)
    from_list = []
    to_list = []
    title_list = []
    key_list = []
    summary_list = []
    doc2_list = []
    for i in docs:
        from_list.append(Glo.from_email[i])
        to_list.append(Glo.to_email[i])
        title_list.append(Glo.title[i])
        key_list.append(Glo.doc_keyWords[i])
        summary_list.append(Glo.summary[i])
        doc2_list.append(Glo.doc_list[i])
    return render_template('docs.html', cate=cate, topic=topic, len=len(docs), from_list=from_list, to_list=to_list,
                           title_list=title_list, \
                           key_list=key_list, summary_list=summary_list, doc_list=doc2_list)
