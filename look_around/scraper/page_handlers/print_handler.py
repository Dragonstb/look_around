from selenium.webdriver.remote.webdriver import WebDriver
from look_around.scraper.page_handlers.page_handler import PageHandler


class PrintHandler(PageHandler):

    chars: int

    def __init__(self, chars: int = 100) -> None:
        self.chars = chars

    def handle_page(self, driver: WebDriver) -> None:
        src = driver.page_source
        if len(src) > self.chars:
            src = src[:self.chars] + '...'

        print()
        print(src)
