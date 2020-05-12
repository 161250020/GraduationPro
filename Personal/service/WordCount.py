import pymongo
from jieba.analyse import textrank
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import Personal.dao.db_connector as db


def get_keywords(user):
    myclient = pymongo.MongoClient('mongodb://localhost:27017')

    mydb = myclient["admin"]
    mycol = mydb["mail"]

    result = {}
    emails = db.get_mail_by_user(user)
    email = ''
    for x, doc in emails:
        email += doc
        for key, weight in textrank(email, topK=50, withWeight=True):
            if key not in result:
                result[key] = weight
            else:
                result[key] += weight

    n = 50

    L = sorted(result.items(), key=lambda item: item[1], reverse=True)

    data = L[:n]

    print(data)

    myWordCloud = WordCloud(init_opts=opts.InitOpts(width="1500px", height="1000px"))
    myWordCloud.add('', data, shape='circle', word_gap=20, word_size_range=[50, 200], rotate_step=90)
    myWordCloud.render()
