import pandas as pd


class ModelWrapper():

    name: str
    """A name for the model."""
    train_scores: pd.DataFrame
    """A spreadsheet with the training scores"""
    val_scores: pd.DataFrame
    """A spreadsheet with the validation scores"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.train_scores = pd.DataFrame([], columns=[
            'accuracy', 'precision', 'recall', 'F1'], index=[0, 1, 2, 3, 4, 5, 'avg'])
        self.val_scores = pd.DataFrame([], columns=[
            'accuracy', 'precision', 'recall', 'F1'], index=[0, 1, 2, 3, 4, 5, 'avg'])
