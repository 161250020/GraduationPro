import pymongo
from jieba.analyse import textrank
from pyecharts.charts import WordCloud
from pyecharts import options as opts


def get_keywords():
    myclient = pymongo.MongoClient(host="localhost", port=27017)

    mydb = myclient["email"]
    mycol = mydb["000"]

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
    myWordCloud.add('', data, shape='circle', word_gap=20, word_size_range=[50, 200], rotate_step=90)
    myWordCloud.render('templates/personal_keywords.html')
