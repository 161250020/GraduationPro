#!usr/bin/python
# -*-coding:utf-8-*-

class InterpersonalNetwork:
    """表示人际关系网"""

    def __init__(self):
        self.set = set()  # 关系网络包括的节点（包括的email）
        self.countEdges = 0  # 关系网络包括的边数（关系网络中发送的邮件数）
        self.outDegree = {}  # 关系网络的出度，为dict（email->dict:email->num）
        self.inDegree = {}  # 关系网络的入度，为dict（email->dict:email->num）

    def add_node(self, fromEmail, toEmail):
        """函数用途：添加节点到当前关系网络；参数：fromEmail, toEmail；返回值：无"""
        self.set.add(fromEmail)
        self.set.add(toEmail)
        self.countEdges = self.countEdges + 1
        # 修改出度
        if fromEmail not in self.outDegree:
            self.outDegree[fromEmail] = {}
        outNodes = self.outDegree.get(fromEmail)  # 为fromEmail的出度的Node的dict
        if toEmail not in outNodes:
            outNodes[toEmail] = 0
        outNodes[toEmail] += 1
        # 修改入度
        if toEmail not in self.inDegree:
            self.inDegree[toEmail] = {}
        inNodes = self.inDegree.get(toEmail)  # 为toEmail的入度的Node的dict
        if fromEmail not in inNodes:
            inNodes[fromEmail] = 0
        inNodes[fromEmail] += 1
