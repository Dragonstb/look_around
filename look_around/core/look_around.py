from pathlib import Path
import json
from typing import Dict, Tuple
from look_around.core.project import Project
import numpy as np
import numpy.typing as npt
import pandas as pd
from look_around.tools import tools
from scipy.sparse import spmatrix
from look_around.run import run_dev
from look_around.run import run_gen


class LookAround():

    _config: Dict
    """The configuration json."""
    home_path: Path
    """Directory the look around projects are stored in."""
    prj: Project
    """Currently loaded project"""
    training_mode: bool
    """True when working with training data. False when analyzing the actual data."""
    vocab: npt.NDArray[np.str_]
    file_data: pd.DataFrame
    train_samples: pd.Series
    test_samples: pd.Series
    train_data: Tuple[spmatrix, pd.Series]
    test_data: Tuple[spmatrix, pd.Series]

    def __init__(self) -> None:
        path = Path(__file__).parent
        path = Path(path, '..',
                    'look_around_config.json').absolute().resolve()

        if path.exists() and path.is_file():
            try:
                with open(path, 'rt') as file:
                    self._config = json.load(file)
                    to_home = self._config['home']
                    self.home_path = Path(
                        path.parent, to_home).absolute().resolve()
            except BaseException as be:
                print('could not load configuration')
                print(be)

            self.training_mode = True

    def create_project(self, name: str) -> Project:
        """
        Creates a new project and its folders and sets it as the active one.

        name:
        Name of the project.

        returns:
        Instance of project
        """
        self.prj = run_gen.create_project_folders(name, self.home_path)
        return self.prj

    def read_project(self, name: str) -> Project:
        """
        Loads the project.

        name:
        Name of the project.

        raises RuntimeError:
        If no project with the given name can be found.
        """
        path = Path(self.home_path, name).absolute().resolve()
        if not path.exists:
            raise RuntimeError('No such project')  # TODO: localize message

        self.prj = Project(name, self.home_path)
        return self.prj

    def read_vocab(self, name: str) -> npt.NDArray[np.str_]:
        """
        Loads a vocabulary.

        name:
        Name of the vocabulary.

        returns:
        The vocabulary.
        """
        self.vocab = self.prj.read_vocab(name)
        return self.vocab

    def read_training_index(self) -> pd.DataFrame:
        self.file_data = self.prj.read_training_index()
        self.training_mode = True
        return self.file_data

    def read_samples(self) -> Tuple[pd.Series, pd.Series]:
        self.train_samples = self.prj.read_train_samples(self.file_data)
        self.test_samples = self.prj.read_test_samples(self.file_data)
        return (self.train_samples, self.test_samples)

    def get_feature_labels(self, ngram_range: Tuple[int, int] = (1, 1)) -> Tuple[spmatrix, pd.Series, spmatrix, pd.Series]:
        self.train_data = tools.get_features_labels(
            self.vocab, self.train_samples, self.file_data, ngram_range=ngram_range)
        self.test_data = tools.get_features_labels(
            self.vocab, self.test_samples, self.file_data, ngram_range=ngram_range)
        return (self.train_data[0], self.train_data[1], self.test_data[0], self.test_data[1])

    def make_dev_project(self, size: int, name: str) -> Project:
        self.prj = run_dev.create_dev_project(size, name, self.home_path)
        return self.prj

    def get_current_project_name(self):
        if self.prj is not None:
            return self.prj.name
        return None

    def is_in_training_mode(self) -> bool:
        return self.training_mode
