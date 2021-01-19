from nltk import download
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
# Importing Gensim
import gensim
from gensim import corpora
import string

download('stopwords')
stop = set(stopwords.words('spanish'))
exclude = set(string.punctuation)

class TopicAna(object):
    def __init__(self, data):
        super().__init__()
        self.doc_clean = [self.clean(doc).split() for doc in data]

    def clean(self, doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        return punc_free

    def get_topics(self):
        dictionary = corpora.Dictionary(self.doc_clean)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in self.doc_clean]
        num_topics = 20
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50)
        top_topics = ldamodel.top_topics(doc_term_matrix)
        topics = []
        for doc_topic in top_topics:
            for topic in doc_topic[0]:
                topics.append(topic)
        topics = sorted(topics, key=lambda tup: tup[1])
        return set([topic[1] for topic in topics])