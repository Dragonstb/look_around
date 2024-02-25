import pandas as pd
import numpy as np
import numpy.typing as npt
from sklearn.feature_extraction.text import TfidfVectorizer as TFV
from look_around.tools import keys
from typing import Tuple
from scipy.sparse import spmatrix


def get_features_labels(vocab: npt.NDArray[np.str_], docs: pd.Series, file_data: pd.DataFrame) -> Tuple[spmatrix, pd.Series]:
    """
    Transforms the input documents into a feature matrix with their associated labels. The indices of 'docs' also
    appear in 'file_data'. This way, a label is linked to a sample.

    vocab:
    Vocabulary taken into account. These are the features.

    docs:
    The texts the features are extracted from. These are the samples.

    file_data:
    The index of sample files. The labels are taken from this data frame by a join in indices with the 'docs'.
    """
    vect = TFV(use_idf=False, binary=True, norm=None, vocabulary=vocab)
    features = vect.fit_transform(docs)
    labels = file_data.loc[docs.index, keys.RATING]
    return (features, labels)
