#!usr/bin/python
#-*-coding:utf-8-*-

import pymongo

'''
获得数据库的内容
'''
def loadData():
    # 读取MongoDB数据库内容
    client = pymongo.MongoClient(host='127.0.0.1')
    mydb = client["email"]  # 数据库
    mycollection = mydb.Collections
    data = mycollection.find({}, {'_id': 0, 'title': 1, 'from': 1, 'to': 1, 'doc': 1, 'split': 1})
    title = []  # 对于每个文章的关键词带上title
    from_email = []
    to_email = []
    splits = []
    doc = []
    file_list = []
    doc_list = []
    for d in data:
        title.append(d['title'])
        from_email.append(d['from'])
        to_email.append(d['to'])
        splits.append(d['split'])
        doc.append(d['doc'])
        file = ''
        for sentence in d['split']:
            file = file + sentence + ' '
        file_list.append(file)
        document=''
        for sentence in d['doc']:
            document=document+sentence
        doc_list.append(document)
    # print("title:",title)
    # print("doc:",np.asarray(doc))
    # print("file_list:",file_list)
    return title,from_email,to_email,splits,doc,file_list,doc_list

