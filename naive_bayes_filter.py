from utils import *
from corpus import Corpus

SPAM_INDEX = 0
HAM_INDEX = 1


class NaiveBayesFilter:

    def __init__(self, pattern):
        self.pattern = pattern

        self.is_trained = False
        self.samples = set()
        self.samples_value = {}
        self.threshold = 0.

    def train(self, truth_dict, corpus):
        filename_samples = {}
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
            self.samples_value[sample] = samples_freqs[sample][SPAM_INDEX] / (samples_freqs[sample][SPAM_INDEX] +
                                                                              samples_freqs[sample][HAM_INDEX])

        ham_value = {}
        for filename, samples in filename_samples.items():
            if truth_dict[filename] == 'OK':
                ham_value[filename] = 0
                for sample in samples:
                    ham_value[filename] += self.samples_value[sample]
                if len(filename_samples[filename]) != 0:
                    ham_value[filename] /= len(filename_samples[filename])

        self.threshold = sorted(ham_value.items(), key=lambda t: t[1], reverse=True)[0][1]
        self.is_trained = True

    def classify(self, email_body):
        if self.is_trained:
            value_count = 0
            match_count = 0
            for sample in self.samples:
                if sample in email_body:
                    match_count += 1
                    value_count += self.samples_value[sample]
            if match_count:
                value_count /= match_count

            if value_count > self.threshold:
                return SPAM_TAG
            else:
                return HAM_TAG

        else:
            my_truth_dict = read_classification_from_file('my_dataset/_truth.txt')
            corpus = Corpus("my_dataset")

            self.train(my_truth_dict, corpus)
            return self.classify(email_body)




