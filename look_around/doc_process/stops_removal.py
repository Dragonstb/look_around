from nltk.corpus import stopwords
from typing import List


def remove_stop_words(text: str, lang: str = 'english') -> str:
    """
    Destopping the text.

    text:
    Text from which the stop words are to be removed.

    lang (default english):
    Language from which the stop words are taken.

    returns:
    Text without the stop words.
    """
    sw = stopwords.words(lang)
    # shortlist = [word for word in text.split() if word not in sw]
    shortened_text = remove_given_stopwords(text, sw)
    return shortened_text


def remove_given_stopwords(text: str, stopwords: List[str] = []) -> str:
    shortlist = [word for word in text.split() if word not in stopwords]
    return ' '.join(shortlist)
