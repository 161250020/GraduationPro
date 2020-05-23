import pymongo


class User:
    @staticmethod
    def userLogin(email):
        """读取MongoDB数据库内容"""
        client = pymongo.MongoClient(host='127.0.0.1')
        mydb = client["email"]  # 数据库
        mycollection = mydb["Users"]
        data = mycollection.find_one({'email': email})
        return data
