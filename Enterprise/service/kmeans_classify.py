import math
from sklearn.cluster import KMeans


class KmeansClassify:
    @staticmethod
    def __fin_k(file_list, weight):
        """获得k-means的k：评估标准：inertia,dunn index"""
        fin_k = 1  # 最终簇数量，小于等于：根号n
        inertias = []  # 簇内距离：越小越好
        dunn_index = []  # 簇间距离：越大越好
        finish1 = False  # 是否结束簇数量的尝试：inertia
        finish2 = False  # 是否结束簇数量的尝试：dunn index
        cur_k = 1  # n=1,2,3,4,5,6,...直到inertia/dunn index的变化不再是剧烈的
        while True:
            if cur_k <= len(file_list):
                kmeans = KMeans(n_clusters=cur_k, init='k-means++')
                kmeans.fit(weight)

                # 计算inertia
                inertias.append(kmeans.inertia_)
                # 判断inertia的变化是否是剧烈的：inertias倒数2个值a,b，当b/a>=0.9即符合要求
                if len(inertias) >= 2:
                    if inertias[-1] / inertias[-2] >= 0.9:
                        finish1 = True
                        fin_k = cur_k

                # 计算dunn index
                dunn = KmeansClassify.__dunn_index(file_list, kmeans, weight)
                dunn_index.append(dunn)
                # 判断dunn index的变化是否是剧烈的
                if len(dunn_index) >= 2:
                    if dunn_index[- 1] / dunn_index[- 2] >= 0.9:  # 包括[...,a,b]：b/a>=0.9以及b>a的情况
                        finish2 = True
                        fin_k = cur_k

                if finish1 and finish2:
                    break
                cur_k += 1
            else:
                fin_k = int(math.sqrt(len(file_list)))
                break
        fin_k = min(fin_k, int(math.sqrt(len(file_list))))
        return fin_k

    @staticmethod
    def __dunn_index(file_list, kmeans, weight):
        """计算dunn index"""
        i = 0
        cluster = {}  # 将已聚类好的邮件集进行分配，eg:类1有文档1,2,...
        while i < len(file_list):
            tmp = cluster.get(kmeans.labels_[i], [])
            tmp.append(i)
            cluster[kmeans.labels_[i]] = tmp
            i += 1
        intra_clusters = kmeans.cluster_centers_  # 所有的簇心
        # 计算最大簇内距离
        max_intra_cluster_distance = 0  # 分母：存储最大簇内距离
        for i in range(len(intra_clusters)):  # 对于每一个簇心
            intra_cluster_distance = 0  # 计算簇内距离
            for j in range(len(cluster[i])):  # 对于该簇心对应的分类的每一个文章的index
                v = weight[cluster[i][j]]
                w = intra_clusters[i]
                square = [(v[k] - w[k]) ** 2 for k in range(len(v))]
                squares = 0
                for l in square:
                    squares += l
                dis = squares ** 0.5
                intra_cluster_distance += dis
            max_intra_cluster_distance = max(max_intra_cluster_distance, intra_cluster_distance)
        # 计算最小簇间距离
        min_inter_cluster_distance = float('inf')  # 分子：最小簇间距离
        for i in range(len(intra_clusters)):
            for j in range(i + 1, len(intra_clusters)):
                sub = [w_k - v_k for w_k, v_k in zip(intra_clusters[i], intra_clusters[j])]
                square = [sub_k ** 2 for sub_k in sub]
                tmp_sum = 0
                for k in square:
                    tmp_sum += k
                tmp_inter_cluster_distance = tmp_sum ** 0.5
                min_inter_cluster_distance = min(min_inter_cluster_distance, tmp_inter_cluster_distance)
        # dunn index值
        dunn = min_inter_cluster_distance / max_intra_cluster_distance
        return dunn

    @staticmethod
    def classify(file_list, weight, cluster):
        """使用合适的簇数量进行kmeans的计算"""
        fin_k = KmeansClassify.__fin_k(file_list, weight)
        print("fin_k--------------------------:", fin_k)
        fin_kmeans = KMeans(n_clusters=fin_k, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
        fin_kmeans.fit(weight)
        i = 0
        while i < len(file_list):
            tmp = cluster.get(fin_kmeans.labels_[i], [])
            tmp.append(i)
            cluster[fin_kmeans.labels_[i]] = tmp
            i += 1
