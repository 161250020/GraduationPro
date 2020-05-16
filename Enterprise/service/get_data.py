#!usr/bin/python
# -*-coding:utf-8-*-

from Enterprise.dao.db import MongodbData
from Enterprise.model.glo import Glo
import re


class GetData:
    """加载数据库的内容到全局变量"""

    @staticmethod
    def load_data():
        """读取MongoDB数据库内容"""
        emails = []
        MongodbData.get_data_from_db(emails)

        Glo.title = []
        Glo.from_email = []
        Glo.to_email = []
        Glo.splits = []
        Glo.doc = []
        Glo.file_list = []
        Glo.doc_list = []
        for d in range(len(emails)):
            Glo.title.append(emails[d].title)
            Glo.from_email.append(emails[d].from_email)
            Glo.to_email.append(emails[d].to_email)
            Glo.doc.append(emails[d].doc)

            # 去除长度为1的词语，英文，数字
            tmp_split = []
            for sentence in emails[d].split:
                sentence_split = sentence.split(' ')
                tmp_sentence = ''
                for sensp in sentence_split:
                    if len(sensp) > 1:
                        tmp_sentence += sensp + ' '
                remove_chars = '[A-Za-z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
                tmp_sentence = re.sub(remove_chars, '', tmp_sentence)
                tmp_split.append(tmp_sentence)
            Glo.splits.append(tmp_split)
            file = ''
            for sentence in tmp_split:
                file = file + sentence + ' '
            Glo.file_list.append(file)

            document = ''
            for sentence in emails[d].doc:
                document = document + sentence
            Glo.doc_list.append(document)
