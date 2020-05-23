from Enterprise.model.glo import Glo
from Enterprise.service.feature_extraction import FeatureExtraction
from Enterprise.service.get_data import GetData
from Enterprise.service.kmeans_classify import KmeansClassify
from Enterprise.service.topic import TopicsAnalyse
from userLogin.service.login import Login

if __name__ == '__main__':
    print(Login.userLogin('shi@ccert.edu.cn', 'Shi123456'))

    GetData.load_data()
    Glo.word, Glo.weight = FeatureExtraction.feature_extraction(Glo.file_list)

    KmeansClassify.classify(Glo.file_list, Glo.weight, Glo.cluster)
    print("cluster:", Glo.cluster)
    print("------------------------------------------------")

    TopicsAnalyse.cal_lda(Glo.cluster, Glo.file_list, Glo.cluster_topics)
    print("cluster_topics:", Glo.cluster_topics)
