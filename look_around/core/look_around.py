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
from look_around.tools import keys
from look_around.doc_process import html_cleaning, stops_removal, stemming


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

    def prepare_unclean_samples(self, lang: str = 'english') -> None:
        idx1 = self.file_data[keys.RAW_FILE].notna()
        idx2 = self.file_data[keys.PREP_FILE].isna()
        df = self.file_data[idx1 & idx2]
        if self.training_mode:
            root = self.prj.training_dir
        else:
            root = self.prj.data_dir
        filecount = len(df)
        counter = 1
        for row in df.index:
            print(f'\rpreprocessing file {counter} of {filecount}', end='')
            raw_file = Path(root, df.loc[row, keys.RAW_FILE]).resolve()
            prep_name = raw_file.stem + '-cleaned.txt'
            prep_file = Path(root, raw_file.parent, prep_name)
            self._prepare_unclean_sample(row, raw_file, prep_file, root, lang)
            counter += 1

    def _prepare_unclean_sample(self, row: str, raw_file: Path, prep_file: Path, root: Path, lang: str) -> None:
        try:
            with open(raw_file, 'rt') as raw:
                lines = [line.strip() for line in raw.readlines()]
                # join by space prevents two words merging into one
                text = ' '.join(lines)
        except BaseException as be:
            print(f'cannot read raw sample file {str(raw_file)}:')
            print(be)
            return

        use_lang = lang
        # TODO: automatically determine language of text, or use existing value in
        # column 'language' of self.file_data

        prepared = html_cleaning.clean_html(text)
        prepared = stops_removal.remove_stop_words(prepared, lang=lang)
        prepared = stemming.stem(prepared, lang=lang)

        try:
            with open(prep_file, 'wt') as prep:
                prep.write(prepared)
                self.file_data.loc[row, keys.PREP_FILE] = str(
                    prep_file.relative_to(root))
        except BaseException as be:
            print(f'cannot write {prep_file.name}:')
            print(be)

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
