from pathlib import Path
import numpy as np
import numpy.typing as npt
import look_around.dev_tools.utils as utils
from typing import Dict, List
import pandas as pd
from look_around.tools import keys, tools
from look_around.models.model_wrapper import ModelWrapper
from tensorflow.keras.models import load_model
from look_around.models.tfkeras_model import TfKerasModel

_train_dir = 'training'
"""Directory for the training data."""
_model_dir = 'model'
"""Directory for the models."""
_data_dir = 'data'
"""Directory for the data that is actually analyzed."""
_doc_index = 'document_index.csv'
"""File name of the list of properties of the samples."""
_chars = np.array(
    list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
_model_index = 'model_index.csv'


class Project():
    """
    Collects the relevant pathes of a project. Each project has an own project directory.
    """
    root_dir: Path
    """project directory"""
    training_dir: Path
    """Directory containing training data"""
    model_dir: Path
    """directory for storing the models"""
    data_dir: Path
    """Directory with the data actually ised for predictions"""
    sample_counter: int
    rand = np.random.Generator
    name: str

    def __init__(self, name: str, parent: Path) -> None:
        # TODO: check if writable / for already existing
        self.name = name
        self.root_dir = Path(parent.absolute(), name)
        self.training_dir = Path(self.root_dir, _train_dir)
        self.model_dir = Path(self.root_dir, _model_dir)
        self.data_dir = Path(self.root_dir, _data_dir)
        self.sample_counter = 0
        self.rand = np.random.default_rng()

    def make_missing_dirs(self) -> None:
        """
        Creates the directories of the project in the file system. Already existing
        directories remain untouched.
        """
        dirs = [self.training_dir, self.model_dir, self.data_dir]
        for dir in dirs:
            if not dir.exists():
                dir.mkdir(exist_ok=False, parents=True)

    def create_sample_id(self) -> Dict:
        """
        Creates an id for the sample and a core path that is included into the
        names of the files associated with that sample.

        returns:
        Dict with entries 'id' and 'path'. The path contains the subdirectory in the
        training/data directory (whichever approbiate) the sample files will
        end in. Appended to that dir name, divided by the path division symbol, is
        the id.
        """
        self.sample_counter += 1

        id = ''.join(utils.pick_several_from_array(_chars, 6))
        id = '_'.join([id, str(self.sample_counter)])
        dir = str(self.sample_counter//300)
        if len(dir) < 4:
            dir = ''.join([str(0) for _ in range(4-len(dir))]) + dir

        return {'id': id, 'path': '/'.join([dir, id]), 'dir': dir}

    def write_vocab(self, vocab: npt.NDArray[np.str_], name: str) -> None:
        """Writes the vocabulary to disk."""
        full_path = Path(self.root_dir, f'{name}.txt')
        try:
            with open(full_path, 'wt') as file:
                for word in vocab:
                    file.write(word+'\n')
        except BaseException as be:
            print(f'could not write vocabulary {name}.txt')
            print(be)
        # vocab.tofile(Path(self.root_dir, name, '.txt'),)

    def read_vocab(self, name: str) -> npt.NDArray[np.str_]:
        """
        Reads a vocabulary from disk. Does not take care of i/o errors!

        name:
        Name of the vocabulary, without the ending txt.

        returns:
        Vocabulary
        """
        full_path = Path(self.root_dir, f'{name}.txt')
        with open(full_path, 'rt') as file:
            lst = [line.strip() for line in file.readlines()]
            return np.array(lst)

    def write_training_index(self, file_data: pd.DataFrame) -> None:
        """
        Writes the training files index as csv to the disk.

        file_data:
        Index list of sample files ffor training.
        """
        full_path = Path(self.training_dir, _doc_index)
        file_data.to_csv(full_path, index=True)

    def read_training_index(self) -> pd.DataFrame:
        """
        Reads the training files index from disk. Does not take care of I/O errors!

        returns:
        Index list of sample data for training. A new, empty one is created if the file
        does not exist.
        """
        full_path = Path(self.training_dir, _doc_index)
        if full_path.exists():
            file_data = pd.read_csv(full_path, index_col=0)
        else:
            file_data = pd.DataFrame(
                [], columns=[keys.RAW_FILE, keys.PREP_FILE, keys.ORIGIN, keys.LANGUAGE, keys.RATING, keys.LABELED_BY, keys.USAGE])
        return file_data

    def update_training_index(self, file_data: pd.DataFrame, write_on_update: bool = True) -> pd.DataFrame:
        """
        Looks for .html and .htm files in the training directory that have not been added to
        the sample file index yet. The files found become listed in the index.

        file_data:
        The sample file index.

        write_on_update:
        If files have been added, write the file index to disc in the end.

        returns:
        The sample file index.
        """
        counter = 0
        for subdir in self.training_dir.iterdir():
            if subdir.is_file():
                continue

            new_files = self._update_training_directory(
                file_data, subdir, self.training_dir)
            counter += len(new_files)
            file_data = pd.concat([file_data]+new_files)
        if counter > 0:
            print(f'added {counter} files')  # TODO: localize info message
            if write_on_update:
                self.write_training_index(file_data)
        else:
            print('no new files')
        return file_data

    def _update_training_directory(self, file_data: pd.DataFrame, subdir: Path, modedir: Path) -> List[pd.DataFrame]:
        """
        Browses the 'subdir' for .htm and .html files. For any file found, it is checked if the
        file is listed in the sample file index. If not, the file is added.

        file_data:
        The sample file index.

        subdir:
        The directory in that new files are looked for.

        modedir:
        The training directory or the data directory.

        returns:
        Single row data frames that can be appended to the file index. One row per new entry.
        """
        new_files = []
        for file in subdir.glob('*.htm*'):
            if not file.is_file():
                continue
            if not file.suffix == '.html' and not file.suffix == '.htm':
                continue

            file_path = str(file.relative_to(modedir))
            idx = file_data[keys.RAW_FILE] == file_path
            if not idx.any():
                df = pd.DataFrame(
                    {keys.RAW_FILE: file_path}, index=[file_path])
                new_files.append(df)
        return new_files

    def read_train_samples(self, file_data: pd.DataFrame) -> pd.Series:
        """
        Reads the training samples. A file is skipped if an I/O error occurs while the
        file is read.

        file_data:
        The data frame indexing the sample files.

        returns:
        List of training samples.
        """
        return self._read_training_samples(keys.TRAIN, file_data)

    def read_test_samples(self, file_data: pd.DataFrame) -> pd.Series:
        """
        Reads the testing samples. A file is skipped if an I/O error occurs while the
        file is read.

        file_data:
        The data frame indexing the sample files.

        returns:
        List of testing samples.
        """
        return self._read_training_samples(keys.TEST, file_data)

    def _read_training_samples(self, usage: str, file_data: pd.DataFrame) -> pd.Series:
        """
        Reads the training samples. A file is skipped if an I/O error occurs while the
        file is read.

        usage:
        Read files of this usage.

        file_data:
        The data frame indexing the sample files.

        returns:
        List of training samples. The indices refers to the index in *file_data*.
        """

        # get training samples with labels
        usage_idx = file_data[keys.USAGE] == usage
        label_idx = file_data[keys.RATING].notna()
        idx = usage_idx & label_idx
        file_names = file_data.loc[idx, keys.PREP_FILE].dropna()

        contents: List[pd.Series] = []
        for idx in file_names.index:
            file_name = file_names.loc[idx]
            full_path = Path(self.training_dir, file_name)
            try:
                with open(full_path, 'rt') as file:
                    content = file.read().strip()
                    data = pd.Series(content, index=[idx])
                    contents.append(data)
            except BaseException as be:
                print(f'SKIPPING FILE {file_name}')
                print(be)

        return pd.concat(contents)

    def write_model_index(self, file_data: pd.DataFrame) -> None:
        """
        Writes the model index as csv to the disk.

        file_data:
        Index list of the models within the project.
        """
        full_path = Path(self.model_dir, _model_index)
        file_data.to_csv(full_path, index=True)

    def read_model_index(self) -> pd.DataFrame:
        """
        Reads the model index from disk. Does not take care of I/O errors!

        returns:
        Index list of models. A new, empty one is created if the file
        does not exist.
        """
        full_path = Path(self.model_dir, _model_index)
        if full_path.exists():
            model_data = pd.read_csv(full_path, index_col=0)
        else:
            model_data = tools.make_model_index()
        return model_data

    def read_model(self, name: str) -> ModelWrapper:
        """
        Loads the model with the given name and wraps it into an approbiate wrapper. The file suffix
        determines which wrapper is approbiate.

        The model is taken from the model directory and only from the model directory.

        ---

        name:
        Name of the model. This is also the file name without suffix.

        returns:
        The wrapped model.

        ---

        raises FileNotFoundException:
        If no file with 'name' as stem is found.

        raises RuntimeError:
        If the found file does not have a supported file suffix.
        """
        files = [file for file in self.model_dir.iterdir(
        ) if file.is_file() and file.stem == name]
        if len(files) == 0:
            raise FileNotFoundError('No model file with the provided name')

        file = files[0]
        if file.suffix == '.keras':
            model = load_model(file)
            wrap = TfKerasModel(name, model)
            return wrap
        else:
            raise RuntimeError('Unsupported suffix')

    def write_model(self, model: ModelWrapper) -> None:
        """
        Stores the model into the model directory. The model name is used as file name.
        The file suffix depends on the actual model.

        model:
        The model that is stored.
        """
        dir = self.model_dir
        model.write_model(dir)
