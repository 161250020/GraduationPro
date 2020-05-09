#!usr/bin/python
#-*-coding:utf-8-*-

'''
加载数据库的内容
'''
from Enterprise.dao.db import Mongodb_data

class Get_data:
    def loadData(self):
        # 读取MongoDB数据库内容
        emails = []
        Mongodb_data.get_data_from_db(emails)

        title = []  # 对于每个文章的关键词带上title
        from_email = []
        to_email = []
        splits = []
        doc = []
        file_list = []
        doc_list = []
        for d in emails:
            title.append(d.title)
            from_email.append(d.from_email)
            to_email.append(d.to_email)
            doc.append(d.doc)
            splits.append(d.split)
            file = ''
            for sentence in d.split:
                file = file + sentence + ' '
            file_list.append(file)
            document = ''
            for sentence in d.doc:
                document = document + sentence
            doc_list.append(document)
        return title, from_email, to_email, splits, doc, file_list, doc_list
