import jieba
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
import pymongo
import pickle

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
    vectorizer = CountVectorizer(decode_error="replace")
    tfidftransformer = TfidfTransformer()
    #vectoring = TfidfVectorizer(input='content', tokenizer=tokenizer_space, analyzer='word')
    content = open(email_file_name, 'r', encoding='utf8').readlines()
    vec_train = vectorizer.fit_transform(content)
    tfidf = tfidftransformer.fit_transform(vec_train)
    feature_path = 'feature.pkl'
    with open(feature_path, 'wb') as fw:
        pickle.dump(vectorizer.vocabulary_,fw)
    tfidftransformer_path = 'tfidftransformer.pkl'
    with open(tfidftransformer_path, 'wb') as fw:
        pickle.dump(tfidftransformer, fw)
    #x = vectoring.fit_transform(content)
    return tfidf

def get_label_list(label_file_name):
    content = open(label_file_name, 'r', encoding='utf8').readlines()
    return content

def get_tfidf_vetorizer():
    return TfidfVectorizer(input='content', tokenizer=tokenizer_space, analyzer='word')
