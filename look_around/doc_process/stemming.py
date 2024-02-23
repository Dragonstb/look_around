import snowballstemmer


def stem(text: str, lang: str = 'english') -> str:
    """
    Returns a stemmed version of 'text' using the snowballstemmer.

    text:
    Text to be stemmed.

    lang (default english):
    Language used for the stemming.

    returns:
    The text with the words stemmed.
    """
    # may cause a key error if 'lang' is not an available language
    # may cause an AttributeError when 'lang' is not valid
    stemmer = snowballstemmer.stemmer(lang)
    stemmed = stemmer.stemWords(text.split())

    return ' '.join(stemmed)
