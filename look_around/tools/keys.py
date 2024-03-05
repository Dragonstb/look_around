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
ORIGIN = "origin"
"""
Column in the sample file index: holds the origin of the sample.
"""
LABELED_BY = 'labeled by'
"""
Column in the sample file index: holds the entity that labeled the sample.
"""

DESC = 'description'
"""Column in the model index: holds a description of the model"""
TRAIN_ACC = 'train accuracy'
"""Column in the model index: holds the training accuracy score"""
TRAIN_PREC = 'train precission'
"""Column in the model index: holds the training precission score"""
TRAIN_REC = 'train recall'
"""Column in the model index: holds the training recall score"""
TRAIN_F1 = 'train f1'
"""Column in the model index: holds the training f1 score"""
VAL_ACC = 'val accuracy'
"""Column in the model index: holds the validation accuracy score"""
VAL_PREC = 'val precission'
"""Column in the model index: holds the validation precission score"""
VAL_REC = 'val recall'
"""Column in the model index: holds the validation recall score"""
VAL_F1 = 'val f1'
"""Column in the model index: holds the validation f1 score"""

ACCURACY = 'accuracy'
PRECISION = 'precision'
RECALL = 'recall'
F1 = 'F1'
