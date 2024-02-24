from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def extract_vocab(docs: List[str], min_df=1, ngram_range: Tuple[int, int] = (1, 1), threshold: float = 0.98, verbose: bool = True, skip_dropping: bool = False):
    """
    Extracts the vocabulary from the list of documents. The appearance or non appearance of the
    words from this vocabulary in a document are the features that are eventually analyzed.

    In the standard settings, the algorithm checks the correlation of the apeearances of each pair of words.
    If the appearance of two words across all documents correlates or anticorrelates with each other, one
    of the words is dropped from the vocabulary.

    docs:
    The documents.

    min_df (default 1):
    A word is omitted for the vocabulary if it appears in less documents than this value is set to.

    ngram_range (default (1,1))
    The n-grams that make up the vocabulary.

    threshold (default 0.98):
    If the magnitude of the correlation between the documenmt appearance vectors of two words exceeds
    this threshold, one of the two words is dropped from the vocabulary.

    verbose (default True):
    If and only if, a progress indicator is printed to sout.

    skip_dropping (default False):
    Determines if the dropping of words thats appearance strongly (anti)correlates with another words
    shall be omitted.
    """
    vect = TfidfVectorizer(min_df=min_df, use_idf=False,
                           binary=True, norm=None, ngram_range=ngram_range)

    if verbose:
        print('getting vocab', end='')
    matrix = vect.fit_transform(docs)
    vocab = vect.get_feature_names_out()

    # drop strongly correlated words
    droplist = []

    # statistics on each word
    if verbose:
        print('\rpreparing stats', end='')
    means = np.zeros(len(vocab))
    vars = np.zeros(len(vocab))
    for word in range(len(vocab)):
        x = matrix.getcol(word).toarray().T[0]
        means[word] = np.mean(x)
        vars[word] = np.var(x)

    sqrtvars = np.sqrt(vars)
    consts = np.absolute(vars) < .00001

    for word in range(len(vocab)-1):
        if verbose:
            print(
                f'\rchecking word {word+1} of {len(vocab)-1}, dropped {len(droplist)} words so far', end='')
        x = matrix.getcol(word).toarray().T[0]
        xcen = x - means[word]
        for other in range(word+1, len(vocab)):
            # check if all values in an array are the same
            if not consts[word] and not consts[other]:
                z = matrix.getcol(other).toarray().T[0]
                # could also take the confidence interval into account
                # TODO: x and z consists just of 0s and 1s each. This might gives rise for further
                # optimization of the computation of the mutual correlation
                cov = np.mean(xcen * (z - means[other]))
                c = cov / (sqrtvars[word] * sqrtvars[other])
                c = np.absolute(c)
            elif consts[word] and consts[other]:
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
