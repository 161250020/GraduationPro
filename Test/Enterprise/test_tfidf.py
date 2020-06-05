import unittest
import numpy as np
from Enterprise.service.feature_extraction import FeatureExtraction


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
        print("特征项：\n", np.asarray(word))
        print("特征向量：\n", np.asarray(weight))


if __name__ == '__main__':
    unittest.main()
