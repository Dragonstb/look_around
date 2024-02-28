USAGE = 'usage'
"""Column in the sample files index that holds the usage of a sample (train, test, use, ...)."""
TRAIN = 'train'
"""This sample is used as train sample."""
TEST = 'test'
"""This sample is used as test sample."""
RAW_FILE = 'raw file'
"""
Column in the sample files index: holds the names of the rae sample files. These files require some preparation before
they can be analyzed. File names are relative to the index file.
"""
PREP_FILE = 'prepared file'
"""
Column in the sample files index: holds the names of the prepared and ready for use sample files. File names are relative
to the index file.
"""
RATING = 'rating'
"""
Column in the sample file index: holds the label.
"""
LANGUAGE = 'language'
"""
Column in the sample file index: holds the language the raw sample text is written in.
"""
