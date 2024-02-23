from pathlib import Path
import numpy as np
import look_around.dev_tools.utils as utils  # TODO: shift file to higher directory
from typing import Dict

_train_dir = 'training'
_model_dir = 'model'
_data_dir = 'data'
_chars = np.array(
    list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))


class Project():
    """
    Collects the relevant pathes of a project. Each project has an own project directory.
    """
    root_dir: Path
    """project directory"""
    train_dir: Path
    """Directory containing training data"""
    model_dir: Path
    """directory for storing the models"""
    data_dir: Path
    """Directory with the data actually ised for predictions"""
    sample_counter: int
    rand = np.random.Generator

    def __init__(self, name: str, parent: Path) -> None:
        # TODO: check if writable / for already existing
        self.root_dir = Path(parent.absolute(), name)
        self.train_dir = Path(self.root_dir, _train_dir)
        self.model_dir = Path(self.root_dir, _model_dir)
        self.data_dir = Path(self.root_dir, _data_dir)
        self.sample_counter = 0
        rand = np.random.default_rng()

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
