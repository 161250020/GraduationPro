import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["admin"]
mycol = mydb["mail"]

def tokenizer_jieba(line):
    # 结巴分词
    return [li for li in jieba.cut(line) if li.strip() != '']

def tokenizer_space(line):
    # 按空格分词
    return [li for li in line.split() if li.strip() != '']

def get_data_tf_idf(email_file_name):
    # 邮件样本已经分好了词，词之间用空格隔开，所以 tokenizer=tokenizer_space
    vectoring = TfidfVectorizer(input='content', tokenizer=tokenizer_space, analyzer='word')
    content = open(email_file_name, 'r', encoding='utf8').readlines()
    x = vectoring.fit_transform(content)
    return x, vectoring

def get_label_list(label_file_name):
    content = open(label_file_name, 'r', encoding='utf8').readlines()
    return content

def get_tfidf_vetorizer():
    return TfidfVectorizer(input='content', tokenizer=tokenizer_space, analyzer='word')
