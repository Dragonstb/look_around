from pathlib import Path
import numpy as np
import numpy.typing as npt
import look_around.dev_tools.utils as utils
from typing import Dict, List
import pandas as pd
from look_around.tools import keys

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
        Index list of sample data for training.
        """
        full_path = Path(self.training_dir, _doc_index)
        file_data = pd.read_csv(full_path, index_col=0)
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

            counter += self._update_training_directory(
                file_data, subdir, self.training_dir)
        if counter > 0:
            print(f'added {counter} files')  # TODO: localize info message
            if write_on_update:
                self.write_training_index(file_data)
        else:
            print('no new files')
        return file_data

    def _update_training_directory(self, file_data: pd.DataFrame, subdir: Path, modedir: Path) -> int:
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
        Number of files added to the index.
        """
        counter = 0
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
                pd.concat([file_data, df])
                counter += 1
        return counter

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
