import pymongo
from Enterprise.model.email import Email

class Mongodb_data:
    def get_data_from_db(emails):
        # 读取MongoDB数据库内容
        client = pymongo.MongoClient(host='127.0.0.1')
        mydb = client["email"]  # 数据库
        collection_names = mydb.collection_names()
        for collection_name in collection_names:
            mycollection = mydb["{}".format(collection_name)]
            data = mycollection.find({}, {'title': 1, 'from': 1, 'to': 1,'cc':1, 'doc': 1, 'split': 1})
            for d in data:
                temp_email=Email(d['title'],d['from'],d['to'],d['cc'],d['doc'],d['split'])
                emails.append(temp_email)
