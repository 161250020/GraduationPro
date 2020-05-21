#encoding = utf-8
from collections import defaultdict

import json
import pymongo
from flask import jsonify
from pyecharts.charts import Graph
from pyecharts import options as opts

myclient = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myclient["email"]
mycol = mydb["000"]

def get_all_realtionship():
    print(mycol)
    edges_weight_temp = defaultdict(list)
    for x in mycol.find({}, {"_id": 0, "from": 1, "to": 1}):
        temp = (x["from"], x["to"])
        if temp not in edges_weight_temp:
            edges_weight_temp[temp] = 1
        else:
            edges_weight_temp[temp] += 1

    temp_node_list = {}
    node_list = []
    links = [{"source": key[0], "target":key[1], "weight":val} for key, val in edges_weight_temp.items() if key[0] != key[1]]
    for i in links:
        if i["source"] in temp_node_list:
            temp_node_list[i["source"]] += i["weight"]
        else:
            temp_node_list[i["source"]] = i["weight"]
        if i["target"] in temp_node_list:
            temp_node_list[i["target"]] += i["weight"]
        else:
            temp_node_list[i["target"]] = i["weight"]

    for key,val in temp_node_list.items():
        node_list.append({"name": key, "symbolSize": val*5})
    data = [{'node': node_list, 'link': links}]
    return jsonify({'node': node_list, 'link': links})


def get_personal_relationship(mail:str):
    from_dict = {}
    to_dict = {}
    link = []

    temp_node_list = {}
    node_list = []
    for x in mycol.find({"from": mail}, {"_id": 0, "to": 1}):
        print(x)
        if x["to"] not in to_dict:
            to_dict[x["to"]] = 1
        else:
            to_dict[x["to"]] += 1

    for x in mycol.find({"to": mail}, {"_id": 0, "from": 1}):
        print(x)
        if x["from"] not in to_dict:
            to_dict[x["from"]] = 1
        else:
            to_dict[x["from"]] += 1
    print(to_dict)
    print(from_dict)
    for key,val in from_dict.items():
        if key!=mail:
            link.append({"source": key, "target":mail, "weight":val})
    for key,val in to_dict.items():
        if key!=mail:
            link.append({"source": mail, "target":key, "weight":val})
    for i in link:
        if i["source"] in temp_node_list:
            temp_node_list[i["source"]] += i["weight"]
        else:
            temp_node_list[i["source"]] = i["weight"]
        if i["target"] in temp_node_list:
            temp_node_list[i["target"]] += i["weight"]
        else:
            temp_node_list[i["target"]] = i["weight"]

    for key,val in temp_node_list.items():
        node_list.append({"name": key, "symbolSize": val*5})
    data = [{'node':node_list,'link':link}]
    print(node_list)
    return jsonify({'node': node_list, 'link': link})


def main():
    data = [{'email': '874307889@qq.com'}]
    jsonData=json.dumps(data)
    #data = json.loads(jsonData)
    #print(data[1]['email'])


if __name__ == '__main__':
    main()