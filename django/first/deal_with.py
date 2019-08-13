
import jieba
from snownlp import SnowNLP
import pyLDAvis
import pyLDAvis.sklearn
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
import jieba.posseg as pseg
import datetime


# 所有日期
def all_day():
    all_day=[]
    start = datetime.date.today()
    all_day.append(start)
    for i in range(0,15):
        all_day.append(start - datetime.timedelta(days=i))
    return all_day


# 数据g清洗去掉无用字段
def load_data(data):
    new_data = []
    for i in data.values():
        new_data.append([i['title'],i['content'],i['p_date'],i['read_num'],i['like_num'],i['comment_num'],i['reward_num']])
        # print(i['title'])
    return new_data


# 情感分析
def emotion_analysis(data):
    title = [i[0] for i in data]
    score = [SnowNLP(i[1]).sentiments for i in data]
    score = [i for i in score ]
    # title = [title[score.index(i)] for i in score if i != 0]
    # print(title)
    return title,score

# tf-idf 热度词
def tf_word(data):
    stopwords = []
    cfp = open('static/stopwords.txt')

    for line in cfp:
        for word in line.split():
            stopwords.append(word)
    cfp.close()
    corpus = []
    all_days = all_day()
    for i in data:
        if i[2] in all_days:
            one = jieba.lcut(i[1])
            two = []
            for j in one:
                if j not in stopwords:
                    two.append(j)
            corpus.append(' '.join(two))
    # print(corpus)

    # for i in corpus:
    #     try:
    #         all_corpus.append(i.lower())
    #     except:
    #         pass
    # print(len(all_corpus))
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    result = []
    for i in range(len(weight)):
        for j in range(len(word)):
            result.append([word[j],weight[i][j]])
    this = sorted(result,key=lambda x:x[1],reverse=True)[:50]
    final_result = [{'name':i[0],'value':i[1]} for i in this]
    print(final_result)
    return final_result

# 文章赞赏数目
def reward_analysis(data):
    data = sorted(data,key=lambda k: k[5])
    article = [i[0] for i in data[-11:-1]]
    reward_count = [i[5] for i in data[-11:-1]]
    return article,reward_count

# 阅读分析
def read_analysis(data):
    data = sorted(data,key=lambda k: k[3])
    article = [i[0] for i in data[-11:-1]]
    reward_count = [i[3] for i in data[-11:-1]]
    return article,reward_count

# 喜欢最高
def like_analysis(data):
    data = sorted(data,key=lambda k: k[4])
    article = [i[0] for i in data[-11:-1]]
    reward_count = [i[4] for i in data[-11:-1]]
    return article,reward_count


# 阅读量变化曲线
def time_analysis(data):
    data = sorted(data,key=lambda k:k[2])
    date = [i[2].strftime('%Y-%m-%d') for i in data]
    read = [i[3] for i in data]
    return date,read


def make_html(data):
    stopwords = []
    cfp = open('static/stopwords.txt')

    for line in cfp:
        for word in line.split():
            stopwords.append(word)
    cfp.close()
    content = []
    for i in data:
        try:
            wordlist = jieba.lcut(i[1])
            wordlist = [w for w in wordlist if w not in stopwords and len(w)>2 ]
            document = ' '.join(wordlist)
            content.append(document)
        except:
            pass
    print('ahhh')
    vectorizer = CountVectorizer()
    doc_term_matrix = vectorizer.fit_transform(content)
    lda_model = LatentDirichletAllocation(n_components=2, random_state=888)
    lda_model.fit(doc_term_matrix)
    import pyLDAvis
    import pyLDAvis.gensim
    data = pyLDAvis.sklearn.prepare(lda_model, doc_term_matrix, vectorizer)
    return data