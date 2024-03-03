import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.doc_process import stops_removal as sr
# autopep8: on


class TestStopsRemoval(unittest.TestCase):

    def test_sentence(self):
        text = 'Harriet walks along the road. she was very happy because of the sunshine.'
        expect = 'Harriet walks along road. happy sunshine.'
        destopped = sr.remove_stop_words(text)
        self.assertEqual(expect, destopped)

    def test_list(self):
        stopwords = list('bce')
        text = 'a b c d e f g'
        expect = 'a d f g'
        destopped = sr.remove_given_stopwords(text, stopwords)
        self.assertEqual(expect, destopped)

    def test_empty_list(self):
        stopwords = []
        text = 'a b c d e f g'
        destopped = sr.remove_given_stopwords(text, stopwords)
        self.assertEqual(text, destopped)


if __name__ == '__main__':
    unittest.main()
