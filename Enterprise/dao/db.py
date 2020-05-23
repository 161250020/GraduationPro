import pymongo
from Enterprise.model.email import Email


class MongodbData:
    @staticmethod
    def get_data_from_db(emails):
        """读取MongoDB数据库内容"""
        client = pymongo.MongoClient(host='127.0.0.1')
        mydb = client["email"]  # 数据库
        mycollection = mydb["Collections"]
        data = mycollection.find({}, {'title': 1, 'from': 1, 'to': 1, 'doc': 1, 'split': 1})
        for d in data:
            temp_email = Email(d['title'], d['from'], d['to'], d['doc'], d['split'])
            emails.append(temp_email)
