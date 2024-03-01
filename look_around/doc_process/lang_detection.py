from nltk.corpus import stopwords
from typing import List


def detect_lang(text: str, langs: List[str], threshold: float = 0) -> str:
    """
    Simple language detection. Derives the language of 'text' by computing the fraction of stop words
    in the text for each language.

    text:
    The text of yet unknown language.

    threshold (default 0):
    A number ranging from zero to unity. The fraction of stop words in the assumed language must exceeds
    the given threshold, or 'unkown' is returned.

    returns:
    Assumed language. Returns 'unknown' if the fraction of stop words even for the assumed language does
    not exceeds 'threshold'... or if you show up with no text or no languages in the arguments.
    """
    cur_lang: str = "unknown"
    cur_freq: float = -1
    words = set(text.split())
    if len(words) == 0 or len(langs) == 0:
        return cur_lang

    for lang in langs:
        stops = stopwords.words(lang)
        stopped_words = [word for word in words if word in stops]
        fraction = len(stopped_words) / len(words)
        if fraction > cur_freq:
            cur_freq = fraction
            cur_lang = lang

    if cur_freq < threshold:
        return "unknown"

    return cur_lang
