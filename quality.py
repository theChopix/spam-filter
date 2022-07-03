from utils import *
from confmat import BinaryConfusionMatrix


def quality_score(tp, tn, fp, fn):
    quality = (tp + tn) / (tp + tn + 10 * fp + fn)
    return quality


def compute_quality_for_corpus(corpus_dir):
    truth_dict = read_classification_from_file(corpus_dir + '/!truth.txt')
    prediction_dict = read_classification_from_file(corpus_dir + '/!prediction.txt')

    cm = BinaryConfusionMatrix(pos_tag=SPAM_TAG, neg_tag=HAM_TAG)
    cm.compute_from_dicts(truth_dict, prediction_dict)

    return quality_score(cm.tp, cm.tn, cm.fp, cm.fn)


if __name__ == '__main__':
    result = compute_quality_for_corpus('1')
    print(result)