from naive_bayes_filter import NaiveBayesFilter
from corpus import Corpus
from utils import *
import re

ipsPattern = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
linksPattern = 'http://.{,20}\..{,15}\.'
upperPattern = '[A-Z]{10,}'
marksPattern = '[<!*?#%>]{3,}'

# words
# IPs   (re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'))
# links (re.compile('http://.{,20}\..{,15}\.'))
# upper (re.compile('[A-Z]{10,}'))
# marks (re.compile('[<!*?#%>]{3,}'))


class Filter:

    def __init__(self):

        self.ipsFilter = NaiveBayesFilter(re.compile(ipsPattern))
        self.linksFilter = NaiveBayesFilter(re.compile(linksPattern))
        self.upperFilter = NaiveBayesFilter(re.compile(upperPattern))
        self.marksFilter = NaiveBayesFilter(re.compile(marksPattern))

    def train(self, train_dir):
        truth_dict = read_classification_from_file(train_dir + '/!truth.txt')
        corpus = Corpus(train_dir)

        # for