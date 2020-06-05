import unittest
from ChineseSegmentation.getEmail import get_local_emails
from ChineseSegmentation.getEmail import find_min_date_pos
from ChineseSegmentation.getEmail import get_date
from _datetime import datetime


class TestCase(unittest.TestCase):
    def test_get_emails(self):
        emails_number = get_local_emails()
        self.assertEquals(emails_number, 340)

    def test_find_min_date_pos(self):
        pos = find_min_date_pos("Tue, hello world! Mon")
        self.assertEquals(pos, 0)

    def test_get_date(self):
        time = get_date("Date: Sun, 14 Aug 2005 10:19:02 +0800")
        self.assertEquals(time, datetime.strptime("Sun, 14 Aug 2005 10:19:02 +0800", "%d %b %Y %H:%M:%S"))


if __name__ == '__main__':
    unittest.main()
