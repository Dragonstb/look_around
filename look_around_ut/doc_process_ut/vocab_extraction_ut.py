import numpy as np
import numpy.typing as npt
from functools import reduce
import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.doc_process import vocab_extraction as ve
# autopep8: on


class TestVocabExtraction(unittest.TestCase):

    def test_uncorrelated4(self):
        docs = [
            'although',
            'bart',
            'coughed',
            'dramatically'
        ]
        expect = ['although', 'bart', 'coughed', 'dramatically']
        vocab: npt.NDArray = ve.extract_vocab(docs, verbose=False)
        self.assertEqual(len(expect), len(vocab), 'varying length, expected [' +
                         self.print_list(expect)+'] but got ['+self.print_list(vocab)+']')

        for c in expect:
            self.assertTrue(np.equal(vocab, c).any(), f'missing word {c}')

    def test_uncorrelated(self):
        # 'although' leads to vector (1, 0), while 'bart' yields (1, 1)
        docs = [
            'although bart',
            'bart'
        ]
        expect = ['although', 'bart']
        vocab: npt.NDArray = ve.extract_vocab(docs, verbose=False)
        self.assertEqual(len(expect), len(vocab), 'varying length, expected [' +
                         self.print_list(expect)+'] but got ['+self.print_list(vocab)+']')

        for c in expect:
            self.assertTrue(np.equal(vocab, c).any(), f'missing word {c}')

    def test_correlated(self):
        # 'although' is present when 'coughed' is not and vice versa.
        # This strong (anti)correlation should one of them being dropped
        docs = [
            'although bart',
            'bart coughed'
        ]
        expect = ['bart', 'coughed']
        vocab: npt.NDArray = ve.extract_vocab(docs, verbose=False)
        self.assertEqual(len(expect), len(vocab), 'varying length, expected [' +
                         self.print_list(expect)+'] but got ['+self.print_list(vocab)+']')

        self.assertTrue(np.equal(vocab, 'bart').any(), 'missing word bart')
        self.assertTrue(np.equal(vocab, 'although').any() or
                        np.equal(vocab, 'coughed').any(), 'both words were dropped')
        self.assertFalse(np.equal(vocab, 'although').any() and
                         np.equal(vocab, 'coughed').any(), 'both words still present')

    def print_list(self, lst):
        if len(lst) > 1:
            return reduce(lambda a, b: str(a)+', '+str(b), lst)
        elif len(lst) == 1:
            return str(lst)
        else:
            return '><'


if __name__ == '__main__':
    unittest.main()
