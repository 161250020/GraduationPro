import unittest
from ChineseSegmentation.DataClean import clean_regular, clean_symbol, clean_stop_word


class TestCase(unittest.TestCase):
    def test_clean_regular(self):
        result = clean_regular("这a是b测c试1用2信3息。")
        self.assertEqual(result, "这是测试用信息。")

    def test_clean_symbol(self):
        result = clean_symbol("这a是b测c试1用2信3息。")
        self.assertEqual(result, "这a是b测c试1用2信3息")

    def test_clean_stop_word(self):
        result = clean_stop_word(["这", "是", "测试", "用", "信息"])
        self.assertEqual(result, "测试 信息")


if __name__ == '__main__':
    unittest.main()