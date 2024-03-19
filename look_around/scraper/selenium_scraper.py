from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time
from typing import List, Dict
import random


class SeleniumScraper():

    base_url: str
    browser: str

    def __init__(self, base_url: str, browser: str) -> None:
        self.base_url = base_url
        self.browser = browser

    def run(self, actions: List):
        if self.browser == 'chrome':
            driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            driver = webdriver.Firefox()
        elif self.browser == 'edge':
            driver = webdriver.Edge()
        elif self.browser == 'safari':
            driver = webdriver.Safari()
        else:
            print('Unsupported browser for now')
            return

        driver.implicitly_wait(2)

        try:
            driver.get(self.base_url)
            for action in actions:
                self._apply_action_to_driver(driver, action)
        except BaseException as be:
            print(be)
            print('quitting')  # TODO: localize

        driver.quit()

    def _apply_action_to_driver(self, driver: WebDriver, config: Dict) -> None:
        elem = driver.find_element(By.TAG_NAME, 'html')
        ancestors = []
        self._apply_action_to_elem(elem, ancestors, config, driver)

    def _apply_action_to_elem(self, parent: WebElement, ancestors: List[str], config: Dict, driver: WebDriver) -> None:
        try:
            type = config['type'].strip()
        except KeyError:
            print('Action config does not have a type, aborting')
            return

        try:
            if type == 'list':
                self._list_action(parent, ancestors, config, driver)
            elif type == 'click':
                self._click_action(parent, config, driver)
            elif type == 'sleep':
                self._sleep_action(config, driver)
            elif type == 'back':
                self._back_action(driver)
        except BaseException as be:
            print(be)

    def _list_action(self, parent: WebElement, ancestors: List[str], config: Dict, driver: WebDriver) -> None:
        """
        The 'list elements' action. Finds a list of elements and applies the actions as defined in config['actions'] to
        each. The search for the elements is started at the 'parent'. It descends in the steps
        given in config['children'].

        parent:
        Parent element where the quest for the list of elements starts.

        config:
        Configuration of this action. It must be a dict. Needs an array 'children' with =-separated key value pairs
        like 'class=highlighted'. Also may have an array 'actions'. These continuation actions, if present, are
        applied to each element listed by this actions.

        raises:
        Value error for invalid entries in 'children'
        KeyError for missing 'children'
        """
        children = config["children"]
        elems = self._build_element_list(parent, children)
        num_elems = len(elems)

        # actions to be called on these elements
        try:
            actions = config['actions']
        except KeyError:
            # no further actions
            return

        for idx in range(num_elems):
            lineage = ancestors + children[:-1]
            lineage.append(children[-1]+f'[{idx}]')
            for action in actions:
                elem = elems[idx]
                try:
                    # just checking if elem has been rendered stale
                    elem.is_enabled()
                except StaleElementReferenceException:
                    elem = self._traverse_children(
                        driver.find_element(By.TAG_NAME, 'html'), lineage)
                self._apply_action_to_elem(elem, lineage, action, driver)

    def _build_element_list(self, parent: WebElement, children: List[str]) -> List[WebElement]:
        # descent the lineage of descendants
        elem = self._traverse_children(parent, children[:-1])

        # from final descendant, we want all elements
        child = children[-1].strip()
        kvp = child.strip().split('=')
        if len(kvp) != 2 or len(kvp[0].strip()) == 0 or len(kvp[1].strip()) == 1:
            raise ValueError(
                f'key value pair {child} does not have exactly one non-empty key and one non-empty value separated by an equal sign (=), aborting.')
        by = self._get_by(kvp[0].strip())
        elems = elem.find_elements(by, kvp[1].strip())

        return elems

    def _click_action(self, parent: WebElement, config: Dict, driver: WebDriver) -> None:
        children = config["children"]
        elem = self._traverse_children(parent, children)
        ActionChains(driver).scroll_to_element(elem).perform()
        elem.click()

        # actions to be called on these elements
        try:
            actions = config['actions']
        except KeyError:
            # no further actions
            return

        for action in actions:
            self._apply_action_to_driver(driver, action)

    def _sleep_action(self, config: Dict, driver: WebDriver) -> None:
        try:
            min_time = config['min']
        except KeyError:
            min_time = 0

        try:
            max_time = config['max']
        except KeyError:
            max_time = 0

        max_time = max(max_time, min_time + 1)
        diff = max_time - min_time
        sleep_time = min_time + random.random() * diff
        sleep_time = max(sleep_time, 0)
        time.sleep(sleep_time)

    def _back_action(self, driver: WebDriver) -> None:
        driver.back()

    def _get_by(self, type: str) -> str:
        """
        Gets the literal of the instance of 'By' that relates to the type given in the argument.
        The 'type' originates from your 'look_around_config.json' and is part of an entry in a
        'children' array.

        type:
        The type. This is not stripped. So make sure there are no blanks around.

        returns:
        The By depending on the type. Values allowed for 'type' are id, tag, class, css, and name. These relate to
        By.ID, By.TAG_NAME, By.CLASS_NAME, By.CSS_SELECTOR, and By.NAME, respectively.

        raises:
        ValueError if passing an invalid argument.
        """
        if type == 'id':
            return By.ID
        elif type == 'tag':
            return By.TAG_NAME
        elif type == 'class':
            return By.CLASS_NAME
        elif type == 'css':
            return By.CSS_SELECTOR
        elif type == 'name':
            return By.NAME
        else:
            raise ValueError('Invalid By Finder provided')

    def _traverse_children(self, parent: WebElement, children: List[str]) -> WebElement:
        """
        Traverse the children as described in 'children', starting from 'parent'. The list 'children'
        contains of =-separated key value pairs. The entries describe which element finder is used alongside
        which value. Always the first child is returned each step, including the final one.

        parent:
        Element to start from.

        children:
        Describes how to find the next child each step.

        returns:
        The final element that follows from the arguments.

        raises:
        ValueError if an antry in 'children' is badly formatted.
        """
        elem = parent
        # descent the lineage of descendants
        for child in children:
            kvp = child.strip().split('=')
            if len(kvp) != 2 or len(kvp[0].strip()) == 0 or len(kvp[1].strip()) == 0:
                raise ValueError(
                    f'key value pair {child.strip()} does not have exactly one non-empty key and one non-empty value separated by an equal sign (=), aborting.')
            key = kvp[0].strip()
            val = kvp[1].strip()
            by = self._get_by(key)
            if not val.endswith(']'):
                # get first element
                elem = elem.find_element(by, val)
            else:
                # the [x], x a number, is the index in an array and must be stripped from val and parsed
                opn = val.rfind('[') + 1
                cls = len(val) - 1
                idx = int(val[opn:cls])
                val = val[:opn-1].strip()
                elems = elem.find_elements(by, val)
                elem = elems[idx]
        return elem