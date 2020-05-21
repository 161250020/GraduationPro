from flask import Blueprint, jsonify
from flask import request
from Enterprise.model.glo import Glo
from Enterprise.service.topic import TopicsAnalyse

topics_con = Blueprint('topics', __name__)


@topics_con.route('/')
def topics():
    cate = request.values.get("category")[2:]
    # 对于每一类的文档们将进行如下几步操作：
    TopicsAnalyse.cal_lda(Glo.cluster, Glo.file_list, Glo.cluster_topics)
    # print("cluster_topics:", Glo.cluster_topics)
    # print("value:", Glo.cluster_topics[int(cate[2:])])
    ret_data = []
    for topic in Glo.cluster_topics[int(cate)]:
        ret_data.append({"topicName": "主题" + str(topic[0]), "keywords": topic[1]})
    return jsonify(ret_data)
