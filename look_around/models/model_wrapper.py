import pandas as pd
import numpy as np
import numpy.typing as npt
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score
from scipy.sparse import spmatrix
from pathlib import Path

_ACCURACY = 'accuracy'
_PRECISION = 'precision'
_RECALL = 'recall'
_F1 = 'F1'


class ModelWrapper():

    name: str
    """A name for the model."""
    train_scores: pd.DataFrame
    """A spreadsheet with the training scores"""
    val_scores: pd.DataFrame
    """A spreadsheet with the validation scores"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.train_scores = pd.DataFrame([], columns=[
            _ACCURACY, _PRECISION, _RECALL, _F1], index=[0, 1, 2, 3, 4, 5, 'avg'])
        self.val_scores = pd.DataFrame([], columns=[
            _ACCURACY, _PRECISION, _RECALL, _F1], index=[0, 1, 2, 3, 4, 5, 'avg'])

    def fit(self, features: spmatrix, labels: pd.Series) -> None:
        pass

    def compute_training_scores(self, features: spmatrix, labels: pd.Series) -> None:
        """
        Computes the accuracies, precisions, recalls, and f1 scores for the training data.

        labels:
        The true labels.

        pred:
        The predicted labels.
        """
        pred = self.predict(features)
        acc = self.compute_accuracy(labels, pred)
        self.train_scores[_ACCURACY] = acc
        prec = self.compute_precision(labels, pred)
        self.train_scores[_PRECISION] = prec
        rec = self.compute_recall(labels, pred)
        self.train_scores[_RECALL] = rec
        f1 = self.compute_f1(labels, pred)
        self.train_scores[_F1] = f1

    def predict(self, features: spmatrix) -> npt.NDArray:
        return np.array([])

    def validate(self, features: spmatrix, labels: pd.Series) -> None:
        """
        Applies the validation data. The predictions are computed for the validation samples
        and compared against the validation labels. Also writes the accuracy, precision,
        recall, and f1 scores into a data frame.

        features:
        The feature matrix.

        labels:
        The correct labels.
        """
        pred = self.predict(features)
        acc = self.compute_accuracy(labels, pred)
        self.val_scores[_ACCURACY] = acc
        prec = self.compute_precision(labels, pred)
        self.val_scores[_PRECISION] = prec
        rec = self.compute_recall(labels, pred)
        self.val_scores[_RECALL] = rec
        f1 = self.compute_f1(labels, pred)
        self.val_scores[_F1] = f1

    def compute_precision(self, labels: pd.Series, pred: npt.NDArray) -> npt.NDArray[np.float_]:
        """
        Computes the precision (true positives over all positive classifications) for each label.
        Also computes the, unweighted, average of the precisions.

        labels:
        The true labels.

        pred:
        The predicted samples.

        returns:
        The label-specific precisions, with the precision of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average precision at index 6.
        """
        label_prec = precision_score(
            labels, pred, labels=np.arange(6), average=None)
        avg = np.mean(label_prec)
        return np.concatenate([label_prec, [avg]])

    def compute_accuracy(self, labels: pd.Series, pred: npt.NDArray) -> npt.NDArray[np.float_]:
        """
        Computes the accuracy (fraction of correct classifications) for each label as well as for
        all samples.

        labels:
        The true labels.

        pred:
        The predicted samples.

        returns:
        The label-specific accuracies, with the accuracy of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the overall accuracy at index 6.

        """
        acc = []
        for label in range(6):
            idx1 = labels == label
            idx2 = pred == label
            idxTP = idx1 & idx2
            idxTN = np.logical_not(idx1) & np.logical_not(idx2)
            acc_label = (len(pred[idxTP]) + len(pred[idxTN])) / len(pred)
            acc.append(acc_label)
        acc_mean = accuracy_score(labels, pred)
        acc.append(acc_mean)
        return np.array(acc)

    def compute_recall(self, labels: pd.Series, pred: npt.NDArray) -> npt.NDArray[np.float_]:
        """
        Computes the recall (true positives over all positive samples) for each label.
        Also computes the, unweighted, average of the recalls.

        labels:
        The true labels.

        pred:
        The predicted samples.

        returns:
        The label-specific recalls, with the recall of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average recall at index 6.
        """
        label_rec = recall_score(
            labels, pred, labels=np.arange(6), average=None)
        avg = np.mean(label_rec)
        return np.concatenate([label_rec, [avg]])

    def compute_f1(self, labels: pd.Series, pred: npt.NDArray) -> npt.NDArray[np.float_]:
        """
        Computes the f1 (true positives over all positive samples) for each label.
        Also computes the, unweighted, average of the f1s.

        labels:
        The true labels.

        pred:
        The predicted samples.

        returns:
        The label-specific f1s, with the f1 of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average f1 at index 6.
        """
        label_f1 = f1_score(labels, pred, labels=np.arange(6), average=None)
        avg = np.mean(label_f1)
        return np.concatenate([label_f1, [avg]])

    def save_model(self, dir: Path) -> None:
        """
        Save the model under its name in the given directory.

        dir:
        The directory in which the model is saved.
        """
        pass
