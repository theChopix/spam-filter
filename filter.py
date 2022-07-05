from naive_bayes_filter import NaiveBayesFilter
from corpus import Corpus
from utils import *
import re

ipsPattern = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
linksPattern = 'http://.{,20}\..{,15}\.'
upperPattern = '[A-Z]{10,}'  # word written in lowercase
lowerPattern = '[a-z]{10,}'  # word written in uppercase
marksPattern = '[<!*?#%>]{3,}'


class Filter:

    def __init__(self):
        # instances of NaiveBayesFilter, each with different pattern

        # self.ipsFilter = NaiveBayesFilter(re.compile(ipsPattern))
        # self.linksFilter = NaiveBayesFilter(re.compile(linksPattern))
        # self.upperFilter = NaiveBayesFilter(re.compile(upperPattern))
        self.lowerFilter = NaiveBayesFilter(re.compile(lowerPattern))
        # self.marksFilter = NaiveBayesFilter(re.compile(marksPattern))

    # trains each filter instance in self-attributes
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
                # if any of filter instances classifies email as spam
                #   iteration over filters breaks and concerned email is classified as spam
                if result == SPAM_TAG:
                    break
            # file with classification based on the strategy is stored in '!prediction.txt'
            #   in concerned folder (in spam-data..)
            with open(test_dir + "/!prediction.txt", "a+", encoding="utf-8") as prediction:
                prediction.write(filename + " " + result + "\n")


if __name__ == '__main__':
    my_filter = Filter()
    my_filter.train("spam-data/1")
    my_filter.test("spam-data/2")



