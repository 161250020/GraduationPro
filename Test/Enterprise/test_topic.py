import unittest
from Enterprise.service.feature_extraction import FeatureExtraction
from Enterprise.service.topic import TopicsAnalyse


class TestTopic(unittest.TestCase):
    def test_lda(self):
        file_list = ['新春 备 年货  新年 联欢晚会',
                     '新春 节目单  春节 联欢晚会 红火',
                     '大盘 下跌 股市 散户',
                     '下跌 股市 赚钱',
                     '金猴 新春 红火 新年',
                     '新车 新年 年货 新春',
                     '股市 反弹 下跌',
                     '股市 散户 赚钱',
                     '新年 看 春节 联欢晚会',
                     '大盘 下跌 散户 散户']
        cluster = {0: [0, 1, 4, 5, 8], 1: [2, 3, 6, 7, 9]}

        cluster_topics = {}
        TopicsAnalyse.cal_lda(cluster, file_list, cluster_topics)
        print(cluster_topics)


if __name__ == '__main__':
    unittest.main()
