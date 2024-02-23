import re


def clean_html(html: str) -> str:
    """
    Strips an html source text from the html tags. Tags that come with an
    opening and a closing tag are detected even when the text contains
    custom tags. For custom singular tags, similar to <br>, this is
    not the case. Also sets the text to LOWER CASE.

    html:
    Text that may or may not contain html tags.

    return:
    Processed lower case text without the html tags.
    """
    text = html.lower()  # do not mess with upper case or lower case tags

    # remove tags that do not come in pairs
    list = [r'<!doctype.*?>', r'<[/]{0,1}br.*?>',
            r'<[/]{0,1}hr.*?>', r'<[/]{0,1}wbr.*?>', r'<[/]{0,1}meta.*?>']
    for ex in list:
        while re.search(ex, text) is not None:
            text = re.sub(ex, ' ', text)

    # remove tags that come in a pair, while keeping what is between the opening
    # and the closing tag
    pattern = r'<(\w+)[^>]*>((.|\n)*?)</\1>'
    while re.search(pattern, text) is not None:
        text = re.sub(pattern, r' \2 ', text)

    # remove punctuation, replace by space for ensuring the separation of words
    text = re.sub(r'[^ \w]', ' ', text)

    # clean multiple white spaces that were introduced when they replaced the html tags
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()
