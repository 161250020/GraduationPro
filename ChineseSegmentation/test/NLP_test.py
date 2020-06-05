import unittest
from ChineseSegmentation.JB import participle_text, suggest_freq, add_words
import time


class TestCase(unittest.TestCase):
    def test_participle_text(self):
        time_start = time.time()
        result = participle_text("一封测试邮件")
        time_end = time.time()
        self.assertEqual(result, "一封 测试 邮件")
        print('Time Cost:', time_end-time_start, 's')

    def test_suggest_freq_1(self):
        suggest_freq("测")
        result = participle_text("一封测试邮件")
        self.assertEqual(result, "一封 测 试 邮件")

    def test_suggest_freq_2(self):
        suggest_freq("测试邮件")
        result = participle_text("一封测试邮件")
        self.assertEqual(result, "一封 测试邮件")

    def test_add_word(self):
        add_words("试邮")
        result = participle_text("一封测试邮件")
        self.assertEqual(result, "一封 测 试邮 件")


if __name__ == '__main__':
    unittest.main()