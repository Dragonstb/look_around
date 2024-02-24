from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats._result_classes import PearsonRResult
from scipy.stats import pearsonr
import numpy as np


def extract_vocab(docs: List[str], min_df=1, ngram_range: Tuple[int, int] = (1, 1), threshold: float = 0.98, verbose: bool = True):
    vect = TfidfVectorizer(min_df=min_df, use_idf=False,
                           binary=True, norm=None, ngram_range=ngram_range)

    matrix = vect.fit_transform(docs)
    vocab = vect.get_feature_names_out()

    # drop strongly correlated words
    droplist = []

    for word in range(len(vocab)-1):
        if verbose:
            print(
                f'\rchecking word {word+1} of {len(vocab)-1}, dropped {len(droplist)} words so far', end='')
        for other in range(word+1, len(vocab)):
            x = [matrix.getcol(word)[idx, 0] for idx in range(len(docs))]
            z = [matrix.getcol(other)[idx, 0] for idx in range(len(docs))]

            # check if all values in an array are the same
            xvar = np.absolute(np.var(x)) < .00001
            zvar = np.absolute(np.var(z)) < .00001
            if not xvar and not zvar:
                # could also take the confidence interval into account
                c = np.absolute(pearsonr(x, z).correlation)
            elif xvar and zvar:
                # either one is zeros and one is unities, or both are zeros, or both are unities
                # anyway, both are (anti)correlated
                c = 1
            else:
                # assume no correlation
                c = 0

            # drop this word?
            if c > threshold:
                droplist.append(word)
                break  # go on in outer loop

    print()
    arr = np.array([True for _ in range(len(vocab))])
    arr[droplist] = False

    shortlist = vocab[arr]
    return shortlist
