import unittest
from Enterprise.service.doc_summary import DocSummary


class TestTopic(unittest.TestCase):
    def test_lda(self):
        splits = [['  太太 结婚 两年 父母 见过面',
                   '  婚宴 两地 办',
                   '    四川 MM 江苏 北京 读书',
                   '想 MM MM 说 父母 他家 父母 父母 提亲',
                   '路途遥远 父母 身体 不好 想 父母 表达 想 娶 女儿 心',
                   'MM',
                   '想 问问 过来人  ',
                   'MM 思想 传统   老套 劝导 劝导 体谅 体谅 父母']]
        doc = [[" 我和太太结婚两年半了，双方父母还没见过面。",
                " 婚宴在两地各办了一次。",
                "我是四川的，MM是江苏的，我们是在北京读书的时候认识的。",
                "我想和MM在一起，可是MM说我父母必须去他家见他父母，向他父母提亲才可以。",
                "我觉得路途遥远，父母的身体又不好，我想去见她父母，向他们表达我想娶他们女儿的心不也一样么。",
                "可是MM很坚持。",
                "我想问问过来人，你们的 。",
                "你MM的思想还真是传统 老套，多劝导劝导，让她也体谅体谅你父母吧。"]]
        doc_keywords = [['父母', '体谅', 'MM', '婚宴', '结婚']]
        summary = []
        DocSummary.get_summary(doc_keywords, splits, doc, summary)
        self.assertEqual(summary, ['我想和MM在一起，可是MM说我父母必须去他家见他父母，向他父母提亲才可以。你MM的思想还真是传统 老套，多劝导劝导，让她也体谅体谅你父母吧。'])


if __name__ == '__main__':
    unittest.main()
