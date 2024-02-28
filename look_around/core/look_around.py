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
    """The currently active vocabulary."""
    file_data: pd.DataFrame
    """The sample file index that lists all the sample files together with their meta data."""
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
        self.prj = Project(name, self.home_path)
        self.prj.make_missing_dirs()
        return self.prj

    def update_project(self) -> pd.DataFrame:
        """
        Scans for new, raw sample files and adds them to the sample file index
        """
        if (self.training_mode):
            self.file_data = self.prj.update_training_index(self.file_data)
        return self.file_data

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

    def prepare_unclean_samples(self, lang: str = 'english', write_on_update: bool = True) -> None:
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
            print(f'\rpreprocessing file {counter} of {filecount}:', end='')
            raw_file = Path(root, str(df.loc[row, keys.RAW_FILE])).resolve()
            print(f' {str(raw_file.name)} ', end='')
            prep_name = raw_file.stem + '-cleaned.txt'
            prep_file = Path(root, raw_file.parent, prep_name)
            self._prepare_unclean_sample(row, raw_file, prep_file, root, lang)
            counter += 1

        self.prj.write_training_index(self.file_data)
        print('\r')
        print(f'Preprocessed and wrote {counter-1} files')

    def _prepare_unclean_sample(self, row: str, raw_file: Path, prep_file: Path, root: Path, lang: str) -> None:
        print('reading file', end='')
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

        [print('\b', end='') for _ in range(len('reading file'))]
        print('cleaning html', end='')
        text = html_cleaning.clean_html(text)
        [print('\b', end='') for _ in range(len('cleaning html'))]
        print('removing stop words', end='')
        text = stops_removal.remove_stop_words(text, lang=lang)
        [print('\b', end='') for _ in range(len('removing stop words'))]
        print('stemming', end='')
        text = stemming.stem(text, lang=lang)
        [print('\b', end='') for _ in range(len('stemming'))]

        print('writing file', end='')
        try:
            with open(prep_file, 'wt') as prep:
                prep.write(text)
                self.file_data.loc[row, keys.PREP_FILE] = str(
                    prep_file.relative_to(root))
        except BaseException as be:
            print(f'cannot write {prep_file.name}:')
            print(be)
        [print('\b', end='') for _ in range(len('writing file'))]

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

    def load_training_project(self, name: str) -> pd.DataFrame:
        """
        Shortcut for 'read_project(name)' and 'read_training_index()'.

        returns:
        The sample file index.
        """
        self.read_project(name)
        self.read_training_index()
        return self.file_data
