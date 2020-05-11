import pymongo
from sklearn.linear_model import LogisticRegression
from sklearn import svm, ensemble, naive_bayes
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import tfidf
from sklearn.externals import joblib

if __name__ == "__main__":
    np.random.seed(1)
    email_file_name = 'all_email.txt'
    label_file_name = 'label.txt'
    x, vectoring = tfidf.get_data_tf_idf(email_file_name)
    test, vectoring = tfidf.get_data_tf_idf('test.txt')
    y = tfidf.get_label_list(label_file_name)
    y = np.array(y)
    print('x.shape : ', x.shape)
    print('y.shape : ', y.shape)

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
    #clf.fit(x_train, y_train)
    #joblib.dump(clf, 'trained.model')
    clf = joblib.load('trained.model')
    y_pred = clf.predict(test)
    print('classification_report\n', metrics.classification_report(y_test, y_pred, digits=4))
    print('Accuracy:', metrics.accuracy_score(y_test, y_pred))
