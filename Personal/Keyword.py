import pymongo
from jieba.analyse import textrank
from pyecharts.charts import WordCloud
from pyecharts import options as opts


def get_keywords():
    myclient = pymongo.MongoClient('mongodb://localhost:27017')

    mydb = myclient["admin"]
    mycol = mydb["mail"]

    result = {}
    for x in mycol.find({}, {'_id': 0, 'split': 1}):
        email = ''
        for line in x['split']:
            email += line
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
    myWordCloud.add('', data, shape='circle', word_gap=20, word_size_range=[50, 200], rotate_step=90)\
        .set_global_opts(title_opts=opts.TitleOpts(title="关键词云"))
    myWordCloud.render('templates/personal_keywords.html')