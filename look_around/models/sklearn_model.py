from sklearn.base import BaseEstimator
from look_around.models.model_wrapper import ModelWrapper
from scipy.sparse import spmatrix
import pandas as pd
from pathlib import Path
import numpy as np
import numpy.typing as npt
from joblib import dump


class SklearnModel(ModelWrapper):

    model: BaseEstimator

    def __init__(self, name: str, model: BaseEstimator) -> None:
        super().__init__(name)
        self.model = model

    def fit(self, features: spmatrix, labels: pd.Series) -> None:
        self.model.fit(features, labels)
        super().compute_training_scores(features, labels)

    def predict(self, features: spmatrix) -> npt.NDArray:
        pred = self.model.predict(features)
        return pred

    def write_model(self, dir: Path) -> None:
        path = Path(dir, f'{self.name}.sklearn')
        dump(self.model, path)
