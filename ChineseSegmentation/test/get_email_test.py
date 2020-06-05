import unittest
from ChineseSegmentation.parseEmail import get_emails


class TestCase(unittest.TestCase):
    def test_get_emails(self):
        title, content = get_emails()
        self.assertEquals(title, "测试邮件")
        self.assertEquals(content, "这是一封测试邮件")


if __name__ == '__main__':
    unittest.main()
