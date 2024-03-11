from tkinterweb import HtmlFrame
from tkinter import Tk
from tkinter.ttk import Frame, Label, Button
from random import randint
from look_around.presenter.rating_controller import RatingController
from numpy import isnan


class RatingWindow(Tk):
    """
    A GUI window which shows the samples to the user. Alongside, some control elements exists
    in the window for browsing and rating the samples.

    This class references a 'RatingController'. Clicking on buttons in this window invokes the methods
    of the rating controller.
    """

    controller: RatingController
    """The controller that handles the commands."""
    web: HtmlFrame
    """The general frame."""
    rating: Label
    """The label that informs abput the current rating of the current sample."""

    def __init__(self, controller: RatingController, screenName: str = None, baseName: str = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.controller = controller
        self.web = HtmlFrame(self, messages_enabled=False)
        self.web.enable_images(False)
        self.web.load_html(
            '<html><head></head><body><h1>No page</h1></body></html>')

        frm = Frame(self.web)
        frm.grid()
        Button(frm, text="<-",
               command=self._prev).grid(column=0, row=1, rowspan=2)
        Button(frm, text="->",
               command=self._next).grid(column=1, row=1, rowspan=2)
        Label(frm, text="Current rating").grid(
            column=2, row=1)  # TODO: localize
        self.rating = Label(frm, text="None")  # TODO: localize
        self.rating.grid(column=2, row=2)
        Button(frm, text="0", command=self._rate_0).grid(
            column=3, row=1, rowspan=2)
        Button(frm, text="1", command=self._rate_1).grid(
            column=4, row=1, rowspan=2)
        Button(frm, text="2", command=self._rate_2).grid(
            column=5, row=1, rowspan=2)
        Button(frm, text="3", command=self._rate_3).grid(
            column=6, row=1, rowspan=2)
        Button(frm, text="4", command=self._rate_4).grid(
            column=7, row=1, rowspan=2)
        Button(frm, text="5", command=self._rate_5).grid(
            column=8, row=1, rowspan=2)
        Button(frm, text="Quit", command=self.destroy).grid(
            column=0, row=3, columnspan=9)
        self.web.pack(fill="both", expand=True)

    def _prev(self) -> None:
        self.controller.prev()

    def _next(self) -> None:
        self.controller.next()

    def _rate_0(self) -> None:
        self.controller.rate(0)

    def _rate_1(self) -> None:
        self.controller.rate(1)

    def _rate_2(self) -> None:
        self.controller.rate(2)

    def _rate_3(self) -> None:
        self.controller.rate(3)

    def _rate_4(self) -> None:
        self.controller.rate(4)

    def _rate_5(self) -> None:
        self.controller.rate(5)

    def set_rating(self, rating: int) -> None:
        """
        Updates the text in the label with the current rating.
        -----
        rating:
        The rating that becomes displayed. If NaN or negative, the text 'None'
        is written in the label.
        """
        # TODO: localize
        if isnan(rating) or rating < 0:
            self.rating.config(text='None')
        elif self.rating == 1:
            self.rating.config(text='1 star')
        else:
            self.rating.config(text=f'{rating} stars')

    # _______________  passing calls to the HtmlFrame within  _______________

    def load_html(self, html: str) -> None:
        """
        Loads the given *html* into the frame.
        -----
        The html string.
        """
        self.web.load_html(html)

    def load_file(self, path: str) -> None:
        """
        Loads the given *file* into the frame. Note that spooky things like 'file not found' or
        'file is not a html file' may happen. They are not dealt with here.
        -----
        path:
        The path to the file of interest, as string.
        """
        self.web.load_file(path)
