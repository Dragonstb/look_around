from selenium.webdriver.remote.webdriver import WebDriver


class PageHandler():
    """
    Interface for classes that handle page actions.
    """

    def handle_page(self, driver: WebDriver) -> None:
        pass
