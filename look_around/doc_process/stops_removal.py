from nltk.corpus import stopwords


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
    shortlist = [word for word in text.split() if word not in sw]
    return ' '.join(shortlist)
