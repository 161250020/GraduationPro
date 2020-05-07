#导入gensim与jieba包
from gensim import corpora, models, similarities
import jieba


#去除中英停用词
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file,encoding='utf-8')as f:
        stopwords=f.read()
    stopwords_list=stopwords.split('\n')
    custom_stopwords_list=[i for i in stopwords_list]
    return custom_stopwords_list


#调用停用词函数
stop_words_file="stopwordsHIT.txt"
stopwords=get_custom_stopwords(stop_words_file)
print(len(stopwords))


#jieba分词函数
def cut(sentence):
    generator = jieba.cut(sentence)
    return [word for word in generator if  word not in stopwords]


#连接数据库
import pyodbc
conn = 'DRIVER={SQL Server Native Client 10.0};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s'%('database', 'server', 'username', 'password')
mssql_conn = pyodbc.connect(conn)
cur = mssql_conn.cursor()
sql='select  ArticleId, 标题, 摘要, Taskid from table'
cur.execute(sql)
listl=cur.fetchall()
cur.close()
mssql_conn.commit()
mssql_conn.close()


# 数据处理——将数据库里的数据存入一个list
s=[]
for i in listl:
    s.append(list(i))


# 对上面的s列表的摘要一列文本数据进行分词
t=[]
for line in s:
    t.append(line[2])
texts = [cut(str(text)) for text in t[:]]


# 对分好词的文本数据建立语料词典
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id.keys())
corpus = [dictionary.doc2bow(text) for text in texts]


#对语料进行tfidf计算并对要做相似度的那批文本数据做词典向量转换
tfidf = models.TfidfModel(corpus)
new_vec=[]
for i in t[:]:
    new_vec.append(dictionary.doc2bow(cut(str(i))))


#LDA主题模型训练
lda = models.LdaModel(corpus=tfidf[corpus], id2word=dictionary, num_topics=50, passes=10)#初试设置lda的topics为50

#保存训练好的LDA
lda.save("lda.model")


#调用保存好的LDA模型
lda = models.ldamodel.LdaModel.load('lda.model')


l=[]
for j in lda.print_topics(num_topics=50,num_words=10):
    for i,n in enumerate(new_vec):
        for d in lda[n]:
            #print(doc_lda)
            if j[0]==d[0]and d[1]>=0.6:#找出主题概率大于0.6的主题
                print(i+1+'属于的主题：'+str(j[1])+'主题概率：'+str(d[1])+'\n')