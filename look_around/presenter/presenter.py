from random import randint
from look_around.presenter.rating_window import RatingWindow
from look_around.presenter.rating_controller import RatingController
from pandas import DataFrame
import numpy as np
from look_around.core.project import Project
from look_around.tools import keys
from pathlib import Path
from numpy import isnan


class Presenter(RatingController):
    """
    Presents the samples to the user. The user may browse through the samples and rate any sample.

    This class acts a controller in the sense of an MVC when presenting the samples. The class receives a DataFrame in the constructor.
    The DataFrame is the model. An instance of 'RatingWindow' is created which serves as the view.
    """

    dir: Path
    rat_win: RatingWindow
    data: DataFrame
    cur_idx: int

    def __init__(self, data: DataFrame, dir: Path) -> None:
        self.data = data
        self.dir = dir
        if len(data) > 0:
            self.cur_idx = 0
        else:
            self.cur_idx = -1

    def show(self) -> None:
        self.rat_win = RatingWindow(self)
        self._update_view()
        self.rat_win.mainloop()

    def prev(self) -> None:
        self.cur_idx -= 1
        if self.cur_idx < 0:
            # luckily, this ends up at -1 if there is no data in 'data'
            self.cur_idx = len(self.data) - 1
        self._update_view()

    def next(self) -> None:
        self.cur_idx += 1
        if self.cur_idx >= len(self.data):
            if len(self.data) > 0:
                self.cur_idx = 0
            else:
                self.cur_idx = -1
        self._update_view()

    def rate(self, rating: int) -> None:
        idx = self.data.index[self.cur_idx]
        self.data.loc[idx, keys.RATING] = rating
        self.data.loc[idx, keys.LABELED_BY] = 'me'  # TODO: localize
        self.rat_win.set_rating(rating)

    def _update_view(self) -> None:
        """
        Updates all sample-specific GUI elements: the html panel and the rating.
        """
        rating = self._get_rating()
        self.rat_win.set_rating(rating)
        self._update_html()

    def _update_html(self) -> None:
        """
        Updates the html panel with the current html file. If loading fails or if there
        is no data, a message is displayed instead.
        """
        if self.cur_idx < 0 or self.cur_idx >= len(self.data):
            html = '<html><head></head><body><h1>No data around</h1></body></html>'
            self.rat_win.load_html(html)
            return

        sub_path = self.data[keys.RAW_FILE][self.cur_idx]
        full_path = Path(self.dir, sub_path)
        try:
            self.rat_win.load_file(str(full_path))
        except:
            html = '<html><head></head><body><h1>Exception</h1></body></html>'
            self.rat_win.load_html(html)

    def _get_rating(self) -> int:
        """
        Gets the rating for the current sample.
        -----
        returns:
        Rating of the current sample. if the current sample has not been rated yet, -1 is returned.
        """
        try:
            rating = self.data[keys.RATING][self.cur_idx]
            if isnan(rating):
                rating = -1
        except KeyError:
            # most likely, column does not exist
            self.data[keys.RATING] = -1
            rating = -1
        except BaseException:
            rating = -1
        return rating
