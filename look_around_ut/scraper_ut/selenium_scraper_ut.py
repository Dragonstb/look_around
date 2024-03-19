from selenium.webdriver.common.by import By
import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.scraper.selenium_scraper import SeleniumScraper
# autopep8: on


class TestSeleniumScraper(unittest.TestCase):

    scraper: SeleniumScraper

    def setUp(self) -> None:
        self.scraper = SeleniumScraper('https://www.example.com', 'browser')

    def test_get_by_id(self):
        type = 'id'
        expect = By.ID
        actual = self.scraper._get_by(type)
        self.assertEqual(expect, actual)

    def test_get_by_tag(self):
        type = 'tag'
        expect = By.TAG_NAME
        actual = self.scraper._get_by(type)
        self.assertEqual(expect, actual)

    def test_get_by_class(self):
        type = 'class'
        expect = By.CLASS_NAME
        actual = self.scraper._get_by(type)
        self.assertEqual(expect, actual)

    def test_get_by_css(self):
        type = 'css'
        expect = By.CSS_SELECTOR
        actual = self.scraper._get_by(type)
        self.assertEqual(expect, actual)

    def test_get_by_name(self):
        type = 'name'
        expect = By.NAME
        actual = self.scraper._get_by(type)
        self.assertEqual(expect, actual)

    def test_get_by_invalid(self):
        type = 'invalid'
        self.assertRaises(ValueError, self.scraper._get_by, type)

    # def test_list_action(self):
    #     html = '<!DOCTYPE html><html><head><title>Unit Test</title></head><body><p id="first"><ul><li>no1</li><li>no2</li></ul></p><p id="second"><ul><li>yes1</li><li>yes2</li><li>yes3</li></ul></p></body></html>'


if __name__ == '__main__':
    unittest.main()
