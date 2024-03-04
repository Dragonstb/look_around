from numpy._typing import NDArray
from tensorflow.keras import Model
from tensorflow.keras.utils import to_categorical
from look_around.models.model_wrapper import ModelWrapper
from scipy.sparse import spmatrix
import pandas as pd
from pathlib import Path
import numpy as np
import numpy.typing as npt


class TfKerasModel(ModelWrapper):

    model: Model
    batch_size: int
    epochs: int

    def __init__(self, name: str, model: Model, batch_size: int = None, epochs: int = 1) -> None:
        super().__init__(name)
        self.model = model
        self.batch_size = batch_size
        self.epochs = epochs

    def fit(self, features: spmatrix, labels: pd.Series) -> None:
        cat_labels = to_categorical(labels)
        self.model.fit(features, cat_labels,
                       batch_size=self.batch_size, epochs=self.epochs)
        super().compute_training_scores(features, labels)

    def predict(self, features: spmatrix) -> npt.NDArray:
        cat_pred = self.model.predict(features)
        pred = np.argmax(cat_pred, axis=1)  # inverts to_categorical
        return pred

    def save_model(self, dir: Path) -> None:
        path = Path(dir, f'{self.name}.keras')
        self.model.save(path)
