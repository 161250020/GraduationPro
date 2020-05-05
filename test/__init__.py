from Enterprise.model.glo import Glo
#导入建模库
from gensim import corpora
import gensim

#对处理后的数据进行去停用词和分词
texts = Glo.splits

#利用词袋模型建立语料库
dictionary = corpora.Dictionary(texts)
print("dictionary:",dictionary)
corpus = [dictionary.doc2bow(text) for text in texts]
print("corpus:",corpus)

#建立lda模型
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
print(lda.log_perplexity())
for i in range(0,len(corpus)):
    print("topics:", lda.get_document_topics(bow=corpus[i]))