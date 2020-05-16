import unittest
from Enterprise.service.feature_extraction import FeatureExtraction
from Enterprise.service.kmeans_classify import KmeansClassify


class TestKmeansClassify(unittest.TestCase):
    def test_classify(self):
        file_list = ['新春 备 年货 ， 新年 联欢晚会',
                     '新春 节目单 ， 春节 联欢晚会 红火',
                     '大盘 下跌 股市 散户',
                     '下跌 股市 赚钱',
                     '金猴 新春 红火 新年',
                     '新车 新年 年货 新春',
                     '股市 反弹 下跌',
                     '股市 散户 赚钱',
                     '新年 , 看 春节 联欢晚会',
                     '大盘 下跌 散户 散户']
        word, weight = FeatureExtraction.feature_extraction(file_list)
        cluster = {}
        KmeansClassify.classify(file_list, weight, cluster)
        self.assertIn(len(cluster.keys()), [2, 3])  # 仅测试分类的数量，因为k-means初始化的中心点不确定，无法确定每次聚类的文档分配


if __name__ == '__main__':
    unittest.main()
