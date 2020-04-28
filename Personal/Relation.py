#encoding = utf-8
from collections import defaultdict

import pymongo
from pyecharts.charts import Graph
from pyecharts import options as opts

def get_personal_realtionship():
    myclient = pymongo.MongoClient('mongodb://localhost:27017')

    mydb = myclient["email"]
    mycol = mydb["000"]

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

    graph= (
            Graph(init_opts=opts.InitOpts(width="1500px", height="1000px"))
            .add("", node_list, links,
                repulsion=8000,
                linestyle_opts=opts.LineStyleOpts(width=2,curve=0.1),
                label_opts=opts.LabelOpts(is_show=False),)
            .set_global_opts(title_opts=opts.TitleOpts(title="邮箱关系网"))
        )
    graph.render('../templates/personal_relationship.html')