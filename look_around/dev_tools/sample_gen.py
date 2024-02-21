from req_gen import ReqGen as RG
from alg_cat import AlgorithmicCategorizer as AC
import town_gen as tg
import pandas as pd
import numpy as np


class SampleGen:

    rg: RG
    ac: AC
    towns: pd.Series
    rand: np.random.Generator

    def __init__(self) -> None:
        self.rg = RG()
        self.ac = AC()
        self.towns = tg.gen_towns(100)
        self.rand = np.random.default_rng()

    def new_req(self, print_req: bool = True, print_ranking: bool = True) -> None:
        town_idx = self.rand.integers(len(self.towns))
        town_name = str(self.towns.index[town_idx])
        town_pop = self.towns[town_name]

        self.rg.redesign(town_name)
        html = self.rg.get_html()

        self.ac.fit(html, town_pop)
        self.ac.predict()

        if print_req:
            self.rg.print()

        if print_ranking:
            self.ac.print()

    def get_req(self) -> str:
        return self.rg.get_html()

    def get_rating(self) -> int:
        return self.ac.get_category()

    def print_towns(self) -> None:
        print(self.towns)
