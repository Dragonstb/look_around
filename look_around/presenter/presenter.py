from tkinterweb import HtmlFrame
from tkinter import Tk
from tkinter.ttk import Frame, Label, Button
from random import randint


class Presenter():

    tk: Tk
    web: HtmlFrame

    def __init__(self) -> None:
        self.tk = Tk()
        self.web = HtmlFrame(self.tk, messages_enabled=False)
        self.web.load_html(self._random_html())

        frm = Frame(self.web)
        frm.grid()
        Button(frm, text="<-",
               command=self._prev).grid(column=0, row=1, rowspan=2)
        Button(frm, text="->",
               command=self._next).grid(column=1, row=1, rowspan=2)
        Label(frm, text="Current rating").grid(
            column=2, row=1)  # TODO: localize
        Label(frm, text="None").grid(column=2, row=2)  # TODO: localize
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
        Button(frm, text="Quit", command=self.tk.destroy).grid(
            column=0, row=3, columnspan=9)
        self.web.pack(fill="both", expand=True)

    def show(self) -> None:
        self.tk.mainloop()

    def _prev(self) -> None:
        print('prev')
        self.web.load_html(self._random_html())

    def _next(self) -> None:
        print('next')
        self.web.load_html(self._random_html())

    def _rate_0(self) -> None:
        self._rate(0)

    def _rate_1(self) -> None:
        self._rate(1)

    def _rate_2(self) -> None:
        self._rate(2)

    def _rate_3(self) -> None:
        self._rate(3)

    def _rate_4(self) -> None:
        self._rate(4)

    def _rate_5(self) -> None:
        self._rate(5)

    def _rate(self, rating: int) -> None:
        print(f'rating as {rating} stars')

    def _random_html(self) -> str:
        words = ['<html>', '<head>', '<title>']
        words.append(self._random_word(5, 12))
        words += ['</title>', '</head>', '<body>', '<h1>']
        for _ in range(randint(1, 2)):
            words.append(self._random_word(4, 8))
        words += ['</h1>']
        for x1 in range(randint(2, 5)):
            words.append('<h4>')
            for _ in range(randint(1, 5)):
                words.append(self._random_word(3, 8))
            words.append('</h4>')
            for _ in range(randint(20, 70)):
                words.append(self._random_word(3, 12))
        words += ['</body>', '</html>']
        return ' '.join(words)

    def _random_word(self, a: int, b: int) -> str:
        chars = list('abcdefghijklmnopqrstuvwxyz')
        roll = randint(a, b)
        word = [chars[randint(0, len(chars)-1)] for _ in range(roll)]
        return ''.join(word)
