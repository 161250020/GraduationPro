import math
from sklearn.cluster import KMeans

class Kmeans_classify:
    '''
    获得k-means的k：符合标准：inertia,dunn index
    '''

    def __fin_k(file_list, weight):
        fin_n = 1  # 最终簇数量，小于等于：根号n
        inertias = []  # 簇内距离：越小越好
        dunn_index = []  # 簇间距离：越大越好
        finish1 = False  # 是否结束簇数量的尝试：inertia
        finish2 = False  # 是否结束簇数量的尝试：dunn index
        cur_n = 1  # n=1,2,3,4,5,6,...直到inertia/dunn index的变化不再是剧烈的
        while True:
            if cur_n <= len(file_list):
                kmeans = KMeans(n_clusters=cur_n, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
                kmeans.fit(weight)
                # 计算inertia
                inertias.append(kmeans.inertia_)
                # 判断inertia的变化是否是剧烈的：inertias倒数2个值a,b，当b/a>=0.99即符合要求
                if len(inertias) >= 2:
                    if inertias[-1] / inertias[-2] >= 0.99:
                        finish1 = True
                        fin_n = cur_n
                        # print("finish1:fin_n:",fin_n)

                '''
                #计算dunn index
                min_inter_cluster_distance=float('inf')#计算簇间距离（欧氏距离）的最小值
                kmeans.cluster_centers_#簇心们
                #max_intra_cluster_distance=#簇内距离（欧氏距离）的最大值
                '''
                i = 0
                cluster = {}
                while i < len(file_list):
                    tmp = cluster.get(kmeans.labels_[i], [])
                    tmp.append(i)
                    cluster[kmeans.labels_[i]] = tmp
                    i += 1
                intra_clusters = kmeans.cluster_centers_  # 所有的簇心
                # print("cluster_centers:",intra_clusters)
                # 计算所有簇心簇内距离和是否等于自带的inertia：大致类似
                sum = 0
                max_intra_cluster_distance = 0  # 分母：最大簇内距离
                for i in range(len(intra_clusters)):  # 对于每一个簇心
                    intra_cluster_distance = 0  # 计算簇内距离
                    for j in range(len(cluster[i])):  # 对于该簇心对应的分类的每一个文章的index
                        v = weight[cluster[i][j]]
                        w = intra_clusters[i]
                        # print("v:",v)
                        # print("w:",w)
                        square = [(v[k] - w[k]) ** 2 for k in range(len(v))]
                        squares = 0
                        for l in square:
                            squares += l
                        dis = squares ** 0.5
                        intra_cluster_distance += dis
                    sum += intra_cluster_distance
                    # print("pre_max_intra_cluster_distance:",max_intra_cluster_distance)
                    max_intra_cluster_distance = max(max_intra_cluster_distance, intra_cluster_distance)
                    # print("max_intra_cluster_distance:",max_intra_cluster_distance)
                # print("sum:",sum)
                # print("kmeans.inertia_:",kmeans.inertia_)
                min_inter_cluster_distance = float('inf')  # 分子：最小簇间距离
                for i in range(len(intra_clusters)):
                    for j in range(i + 1, len(intra_clusters)):
                        sub = [w_k - v_k for w_k, v_k in zip(intra_clusters[i], intra_clusters[j])]
                        # print("sub:",sub)
                        square = [sub_k ** 2 for sub_k in sub]
                        # print("square:",square)
                        tmp_sum = 0
                        for k in square:
                            tmp_sum += k
                        tmp_inter_cluster_distance = tmp_sum ** 0.5
                        min_inter_cluster_distance = min(min_inter_cluster_distance, tmp_inter_cluster_distance)
                # print("min_inter_cluster_distance:",min_inter_cluster_distance)
                dunn = min_inter_cluster_distance / max_intra_cluster_distance
                dunn_index.append(dunn)

                '''
                # 判断dunn index的变化是否是剧烈的
                '''
                if len(dunn_index) >= 2:
                    if dunn_index[- 1] / dunn_index[- 2] >= 0.99:  # 包括[...,a,b]：b/a>=0.9以及b>a的情况
                        finish2 = True
                        fin_n = cur_n
                        # print("finish2:fin_n:",fin_n)

                if finish1 and finish2:
                    break
                cur_n += 1
            else:
                fin_n = int(math.sqrt(len(file_list)))
                break
        fin_n = min(fin_n, int(math.sqrt(len(file_list))))
        print("fin_n:", fin_n)
        return fin_n

    def classify(file_list, weight, cluster):
        '''
            第一次分类：进行K-means聚类
        '''
        # 使用合适的簇数量进行kmeans的计算
        fin_n = Kmeans_classify().__fin_k(file_list, weight)
        fin_kmeans = KMeans(n_clusters=fin_n, init='k-means++')  # 使用K-means++来初始化质心，指定初始化过程
        fin_kmeans.fit(weight)
        # 对文档进行分类
        i = 0
        while i < len(file_list):
            tmp = cluster.get(fin_kmeans.labels_[i], [])
            tmp.append(i)
            cluster[fin_kmeans.labels_[i]] = tmp
            i += 1
        print("分类：", cluster)
