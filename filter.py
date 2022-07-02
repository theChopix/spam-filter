from naive_bayes_filter import NaiveBayesFilter
from corpus import Corpus
from utils import *
import re

ipsPattern = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
linksPattern = 'http://.{,20}\..{,15}\.'
upperPattern = '[A-Z]{10,}'
lowerPattern = '[a-z]{10,}'
marksPattern = '[<!*?#%>]{3,}'


class Filter:

    def __init__(self):

        self.ipsFilter = NaiveBayesFilter(re.compile(ipsPattern))
        self.linksFilter = NaiveBayesFilter(re.compile(linksPattern))
        self.upperFilter = NaiveBayesFilter(re.compile(upperPattern))
        self.lowerFilter = NaiveBayesFilter(re.compile(lowerPattern))
        self.marksFilter = NaiveBayesFilter(re.compile(marksPattern))

    def train(self, train_dir):
        truth_dict = read_classification_from_file(train_dir + '/!truth.txt')
        corpus = Corpus(train_dir)

        filters = [getattr(self, attr) for attr in dir(self) if attr.endswith("Filter")]
        for filter in filters:
            filter.train(truth_dict, corpus)

    def test(self, test_dir):
        corpus = Corpus(test_dir)
        result = HAM_TAG

        filters = [getattr(self, attr) for attr in dir(self) if attr.endswith("Filter")]
        for filename, body in corpus.emails():
            for filter in filters:
                result = filter.classify(body)
                if result == SPAM_TAG:
                    break

            with open(test_dir + "/!prediction.txt", "a+", encoding="utf-8") as prediction:
                prediction.write(filename + " " + result + "\n")

