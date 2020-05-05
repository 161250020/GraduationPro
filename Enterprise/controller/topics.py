from flask import Blueprint
from flask import render_template, request
from Enterprise.model.glo import Glo
from Enterprise.service.topic import Topics_analyse

topics_con = Blueprint('topics',__name__)

@topics_con.route('/')
def dir():
    return render_template('dir.html')

@topics_con.route('/topics')
def topics():
    cate=request.args.get("category")
    # 对于每一类的文档们将进行如下几步操作：
    if(len(Glo.cluster_topics)==0):
        Topics_analyse().calLda(Glo.cluster, Glo.file_list, Glo.cluster_topics)
        print("cluster_topics:", Glo.cluster_topics)
    print("value:",Glo.cluster_topics[int(cate)])
    return render_template('Topics.html', c=cate, value=Glo.cluster_topics[int(cate)])
