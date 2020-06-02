#!/usr/bin/python3

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["emails"]
mycol = mydb["emailsDetail"]

for i in range(0, 50):
    print(i)
    mycol.delete_one({})
