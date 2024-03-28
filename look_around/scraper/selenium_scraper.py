from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from typing import List, Dict
import random
from look_around.scraper.page_handlers.page_handler import PageHandler
from look_around.scraper import config_keys as ck


class SeleniumScraper():

    base_url: str
    browser: str
    handlers: Dict[str, PageHandler]

    def __init__(self, base_url: str, browser: str) -> None:
        self.base_url = base_url
        self.browser = browser
        self.handlers = {}

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

        try:
            driver.get(self.base_url)
            for action in actions:
                self._apply_action_to_driver(driver, action)
        except BaseException as be:
            print(be)
            print('quitting')  # TODO: localize

        driver.quit()

    def register_page_handler(self, name: str, handler: PageHandler) -> None:
        """
        Registers the pahe handler and makes it accessible via the provided name.

        ----
        name:
        Key with that the handler is registered.

        handler:
        The page handler.
        """
        self.handlers[name] = handler

    # _______________  top level action handling  _______________

    def _apply_action_to_driver(self, driver: WebDriver, config: Dict) -> None:
        """
        Actually, applies the action to the html tag.

        ---
        driver:
        The web driver.

        config:
        The json with the configuration for the action.
        """
        elem = driver.find_element(By.TAG_NAME, 'html')
        ancestors = []
        self._apply_action_to_elem(elem, ancestors, config, driver)

    def _apply_action_to_elem(self, parent: WebElement, ancestors: List[str], config: Dict, driver: WebDriver) -> None:
        """
        Applies the action, which is described and configured in 'config', to the given element. The method returns if
        the configuration does not contain a key 'type'. The method call for the action is surrounded by a try/except block
        that react on BaseExceptions.

        ----
        parent:
        Element the action is applied to. If the action demands a search for a child element, the search starts from
        this element here.

        ancestors:
        List of =-separated key value pairs that describe the path from the html element to 'parent'.

        config:
        Json containing the configuration for the action.

        driver:
        The web driver.
        """
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
            elif type == 'handle':
                self._handling_action(config, driver)
            elif type == 'simple cookie dialog':
                self._simple_cookie_dialog(parent, config, driver)
        except BaseException as be:
            print(be)

    # _______________  default actions  _______________

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
        """
        Gets all elements that fullfill the description in the last entry of 'children'. At the same time, for all
        other entries only the first match is taken, though. Consequently, all elements returns have the same parent.

        ----
        parent:
        Element the search starts from.

        children:
        Description how to look for children after children, generation for generation.
        """
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
        """
        Clicks the last descendant in the list of children given in the 'config'. Then, if present, it applies the actions
        listed in 'config' to the driver.

        parent:
        Element to look from in lineage of children.

        config:
        Configuration of the click action.

        driver:
        The web driver.
        """
        children = config["children"]
        repeat = self._get_repeating(config)
        while repeat == ck.AS_LONG_AS_POSSIBLE:
            elem = self._traverse_children(parent, children)
            elem.click()  # may raise exception once it is not possible anymore

            # actions to be called on these elements
            try:
                actions = config['actions']
            except KeyError:
                # no further actions
                return

            for action in actions:
                self._apply_action_to_driver(driver, action)

    def _sleep_action(self, config: Dict, driver: WebDriver) -> None:
        """
        Let the script rest for a few seconds.

        config:
        Action configuration. Should define a number 'min' and a number 'max'. The script sleeps
        a random amount of seconds between min and max.

        driver:
        The web driver.
        """
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
        """
        Go one page back.

        driver:
        The web driver.
        """
        driver.back()

    def _handling_action(self, config: Dict, driver: WebDriver) -> None:
        """
        Invokes a page handler registered with the given name. If no page handler is registerd
        with the name provided, this method simply does nothing and returns. Also simply
        returns if the action configuration does not provide a name.

        ----
        config:
        Json containing the configuration of the action.

        driver:
        The web driver.
        """
        try:
            name = config['name'].strip()
        except KeyError:
            print('Configuration for page handling does not has a name given, aborting')
            return

        try:
            handler = self.handlers[name]
            handler.handle_page(driver)
        except BaseException:
            pass  # just return

    # _______________  fun with cookie banners  _______________

    def _simple_cookie_dialog(self, parent: WebElement, config: Dict, driver: WebDriver) -> None:
        children = config[ck.CHILDREN]

        try:
            wait_for = int(config[ck.WAIT_FOR])
        except:
            wait_for = 10

        elem = self._traverse_children(parent, children)
        wait = WebDriverWait(driver, timeout=wait_for)
        wait.until(lambda _: self._is_interactible(elem))

        elem.click()

    def _is_interactible(self, elem: WebElement) -> bool:
        return elem.is_displayed() and elem.is_enabled()

    # _______________  utilities  _______________

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

        NoSuchElementException if a single child cannot be found.
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

    def _get_repeating(self, config: Dict) -> str:
        """
        Extracts the value of the key 'repeat' from the configuration.

        ----

        config:
        The configuration of the action.

        ----
        returns:
        The repitition. If the key is missing or the value invalid, 'no' is returned.
        """
        try:
            repeat = config[ck.REPEAT]
            if repeat != ck.AS_LONG_AS_POSSIBLE:
                repeat = ck.NO
        except BaseException:
            repeat = ck.NO

        return repeat
