import pymongo
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import svm, ensemble, naive_bayes
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import Personal.Mail_Process.tfidf as tfidf
from sklearn.externals import joblib
import pickle
import Personal.dao.db_connector as db

myclient = pymongo.MongoClient('mongodb://localhost:27017')

mydb = myclient["admin"]
mycol = mydb["mail"]

def trans():
    test_content = []
    mail_list = []
    for x,doc in db.get_all_email():
        mail_list.append(x)
        test_content.append(doc)
    feature_path = '../../data/feature.pkl'
    loaded_vec = CountVectorizer(decode_error="repalce",vocabulary=pickle.load(open(feature_path, 'rb')))

    tfidftransformer_path = '../../data/tfidftransformer.pkl'
    tfidftransformer = pickle.load(open(tfidftransformer_path, 'rb'))

    test_tfidf = tfidftransformer.transform(loaded_vec.transform(test_content))
    return test_tfidf, mail_list

def predict():
    emails = []
    clf = LogisticRegression()
    clf = joblib.load('../../data/trained.model')
    result = []
    data,emails = trans()
    temp_result = clf.predict(data)
    for i in range(0, len(temp_result)):
        if temp_result[i][0] == 0:
            result.append(['spam', emails[i]])
        else:
            result.append(['ham', emails[i]])
    return result
def train():
    np.random.seed(1)
    email_file_name = '../../data/all_email.txt'
    label_file_name = '../../data/label.txt'
    x = tfidf.get_data_tf_idf(email_file_name)
    y = tfidf.get_label_list(label_file_name)
    y = np.array(y)

    # 随机打乱所有样本
    index = np.arange(len(y))
    #np.random.shuffle(index)
    x = x[index]
    y = y[index]


    # 划分训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    #clf = svm.LinearSVC()
    clf = LogisticRegression()
    #clf = ensemble.RandomForestClassifier()
    clf.fit(x_train, y_train)
    joblib.dump(clf, '../../data/trained.model')
    #clf = joblib.load('../../data/trained.model')
    y_pred = clf.predict(x_test)
    print('classification_report\n', metrics.classification_report(y_test, y_pred, digits=4))
    print('Accuracy:', metrics.accuracy_score(y_test, y_pred))


if __name__ == "__main__":
    #train()
    predict()
