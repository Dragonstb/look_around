import numpy.typing as npt
import numpy as np
import pandas as pd
import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.models.model_wrapper import ModelWrapper as MW
# autopep8: on

_CATS = 3


class TestModelWrapper(unittest.TestCase):

    mw: MW
    labels: pd.Series
    """A constructed set of numbers serving as 'true labels'"""
    predictions: npt.NDArray[np.int_]
    """A constructed set of numbers serving as 'predictions'"""

    def setUp(self) -> None:
        self.mw = MW('unit test')
        self.labels = pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
        self.predictions = np.array([0, 0, 0, 0, 1, 1, 0, 1, 2, 0, 2, 1])

    def test_compute_accuracy(self):
        norm = len(self.labels)
        expect = [-1., -1., -1., -1.]
        expect[0] = (4+6)/norm
        expect[1] = (2+6)/norm
        expect[2] = (1+7)/norm
        expect[3] = 7/norm
        actual = self.mw.compute_accuracy(
            self.labels, self.predictions, categories=_CATS)

        for idx in range(_CATS+1):
            self.assertAlmostEqual(
                expect[idx], actual[idx], delta=.001, msg=f'Wrong accuracy in index {idx}')

    def test_compute_precision(self):
        expect = [-1., -1., -1., -1.]
        expect[0] = 4/len(self.predictions[self.predictions == 0])
        expect[1] = 2/len(self.predictions[self.predictions == 1])
        expect[2] = 1/len(self.predictions[self.predictions == 2])
        expect[3] = (expect[0] + expect[1] + expect[2]) / 3
        actual = self.mw.compute_precision(
            self.labels, self.predictions, categories=_CATS)

        for idx in range(_CATS+1):
            self.assertAlmostEqual(
                expect[idx], actual[idx], delta=.001, msg=f'Wrong precision in index {idx}')

    def test_compute_recall(self):
        expect = [-1., -1., -1., -1.]
        expect[0] = 4/len(self.labels[self.labels == 0])
        expect[1] = 2/len(self.labels[self.labels == 1])
        expect[2] = 1/len(self.labels[self.labels == 2])
        expect[3] = (expect[0] + expect[1] + expect[2]) / 3
        actual = self.mw.compute_recall(
            self.labels, self.predictions, categories=_CATS)

        for idx in range(_CATS+1):
            self.assertAlmostEqual(
                expect[idx], actual[idx], delta=.001, msg=f'Wrong recall in index {idx}')

    def test_compute_f1(self):
        precision = [-1., -1., -1., -1.]
        precision[0] = 4/len(self.predictions[self.predictions == 0])
        precision[1] = 2/len(self.predictions[self.predictions == 1])
        precision[2] = 1/len(self.predictions[self.predictions == 2])

        recall = [-1., -1., -1., -1.]
        recall[0] = 4/len(self.predictions[self.labels == 0])
        recall[1] = 2/len(self.predictions[self.labels == 1])
        recall[2] = 1/len(self.predictions[self.labels == 2])

        expect = [2*precision[idx]*recall[idx] /
                  (precision[idx]+recall[idx]) for idx in range(_CATS)]
        expect.append((expect[0] + expect[1] + expect[2]) / 3)

        actual = self.mw.compute_f1(
            self.labels, self.predictions, categories=_CATS)

        for idx in range(_CATS+1):
            self.assertAlmostEqual(
                expect[idx], actual[idx], delta=.001, msg=f'Wrong f1 in index {idx}')


if __name__ == '__main__':
    unittest.main()
