from utils import *
from corpus import Corpus

# indexes in frequency array
SPAM_INDEX = 0
HAM_INDEX = 1


# takes a pattern (regular expression) that is applied to determine from the training data-set
#   characteristics of spam-emails based on the pattern (it's matches)
class NaiveBayesFilter:

    def __init__(self, pattern):
        self.pattern = pattern

        self.is_trained = False

        # matches of the given pattern in email-content
        self.samples = set()

        # dictionary of spam-values <0,1> of matches (samples)
        self.samples_value = {}

        # computed final value of the 'most spam' ham-email
        #   values greater than this limit are only achieved by spam in the training data-set
        self.threshold = 0.

    def train(self, truth_dict, corpus):
        # dictionary of filename & list of samples (matches) found in the file
        filename_samples = {}

        # dictionary of (all) matches & their frequencies in emails
        #   frequency = [s, h] where
        #       s = number of sample-occurrences in spam-emails
        #       h = number of sample-occurrences in ham-emails
        samples_freqs = {}

        for filename, email_body in corpus.emails():
            filename_samples[filename] = set()
            matches = self.pattern.findall(email_body)
            for match in matches:
                self.samples.add(match)
                filename_samples[filename].add(match)

                if match not in samples_freqs:
                    samples_freqs[match] = [0, 0]

                if truth_dict[filename] == 'SPAM':
                    samples_freqs[match][SPAM_INDEX] += 1
                elif truth_dict[filename] == 'OK':
                    samples_freqs[match][HAM_INDEX] += 1

        for sample in self.samples:
            # computation of spam-value <0,1> based on it's frequencies
            self.samples_value[sample] = samples_freqs[sample][SPAM_INDEX] / (samples_freqs[sample][SPAM_INDEX] +
                                                                              samples_freqs[sample][HAM_INDEX])
        # dictionary of (all) ham-emails & their average spam-value
        #   based on matches (and their values) found in concerned ham-email
        ham_value = {}
        for filename, samples in filename_samples.items():
            if truth_dict[filename] == 'OK':
                ham_value[filename] = 0
                for sample in samples:
                    ham_value[filename] += self.samples_value[sample]
                if len(filename_samples[filename]) != 0:
                    ham_value[filename] /= len(filename_samples[filename])

        # sorted ham_value dictionary
        #   so we can get one with the greatest 'value of spam'
        self.threshold = sorted(ham_value.items(), key=lambda t: t[1], reverse=True)[0][1]
        self.is_trained = True

    def classify(self, email_body):
        if self.is_trained:
            # number of samples (above) found in tested email-content
            match_count = 0

            # sum of 'spam-values' of found samples
            value_count = 0
            for sample in self.samples:
                if sample in email_body:
                    match_count += 1
                    value_count += self.samples_value[sample]
            if match_count:
                # average based on number of samples
                value_count /= match_count

            # if computed value is greater than threshold computed in train
            #   it is classified as spam; otherwise ham
            if value_count > self.threshold:
                return SPAM_TAG
            else:
                return HAM_TAG

        else:
            # in case of non-pretrained classification there is place
            #   for some heuristics, anyway I decided to stick with train technique with given data
            my_truth_dict = read_classification_from_file('spam-data/1/!truth.txt')
            corpus = Corpus("spam-data/1")

            self.train(my_truth_dict, corpus)
            return self.classify(email_body)




