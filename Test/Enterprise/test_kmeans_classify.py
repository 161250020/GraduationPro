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
        self.assertEqual(len(cluster.keys()), 2)
        if 0 in cluster[0]:
            self.assertEqual(cluster[0], [0, 1, 4, 5, 8])
            self.assertEqual(cluster[1], [2, 3, 6, 7, 9])
        else:
            self.assertEqual(cluster[0], [2, 3, 6, 7, 9])
            self.assertEqual(cluster[1], [0, 1, 4, 5, 8])


if __name__ == '__main__':
    unittest.main()
