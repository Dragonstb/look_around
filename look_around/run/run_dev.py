from pathlib import Path
import run_gen
import pandas as pd
from dev_tools.sample_gen import SampleGen as SG
from dev_tools import utils
import numpy as np


def create_dev_project(size: int, name: str, parent: Path):
    prj = run_gen.create_project_folders(name, parent)
    sg = SG()
    cols = []
    file_data = []

    for _ in range(size):
        sg.new_req(print_ranking=False, print_req=False)
        html = sg.get_req()
        rating = sg.get_rating()
        id = prj.create_sample_id()
        dic = {
            'raw file': Path(id['path'], 'raw.html'),
            'rating': rating
        }
        df = pd.DataFrame(dic, index=[id['id']])
        file_data.append(df)

    file_data = pd.concat(file_data)
    print(file_data)
