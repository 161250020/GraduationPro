#encoding = utf-8
from collections import defaultdict

import pymongo
from pyecharts.charts import Graph
from pyecharts import options as opts

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["admin"]
mycol = mydb["mail"]

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
    node_list.append({"name": key, "symbolSize": val*3})

print(node_list)

print(links)

graph= (
    Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add(
        "",
        nodes=node_list,
        links=links,
        layout="none",
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7),
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-NPM Dependencies"))
    )
graph.render()
