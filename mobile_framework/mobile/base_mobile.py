import os

import gevent
from allure import step
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from mobile_framework.utilities import Utilities


class BaseMobile:
    implicit_sec = 30
    properties = False

    def __init__(self, driver):
        self.driver = driver
        if not self.properties:
            Utilities.fix_mobile_properties()
            Utilities.create_executor_file()
            self.properties = True

    def wait_until_element_located(self, locator, timeout=implicit_sec, xml=True):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            if xml:
                Utilities.attach_xml_source(self)
            raise Exception(f'Element {locator[1]} was not found during {timeout} seconds')

    def wait_until_element_invisible(self, locator, timeout=implicit_sec):
        if self.is_present(*locator, timeout=1, xml=False):
            try:
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            except TimeoutException:
                pass

    def wait_until_element_to_be_clickable(self, locator, timeout=implicit_sec):
        try:
            WebDriverWait(self.driver, self.implicit_sec).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            Utilities.attach_xml_source(self)
            raise Exception(f'Element {locator[1]} was not clickable during {timeout} seconds')

    def find_element(self, *locator, timeout=implicit_sec, xml=True):
        self.wait_until_element_located(locator, timeout=timeout, xml=xml)
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        self.wait_until_element_located(locator)
        return self.driver.find_elements(*locator)

    def scroll_for_element(self, *locator):
        attempts = 10
        for _ in range(attempts):
            if _ <= 5:
                try:
                    self.wait_until_element_located(locator, timeout=1, xml=False)
                    element = self.driver.find_element(*locator)
                    TouchAction(self.driver).move_to(element)
                    return element
                except:
                    self.swipe_to_the_bottom_of_screen()
            else:
                try:
                    self.wait_until_element_located(locator, timeout=1, xml=False)
                    element = self.driver.find_element(*locator)
                    TouchAction(self.driver).move_to(element)
                    return element
                except:
                    self.swipe_to_the_top_of_screen()
        Utilities.attach_xml_source(self)
        raise Exception(f'Element - "{locator}" not found')

    def tap(self, *locator, timeout=implicit_sec, scroll=True):
        with step(f'Tap element - {locator}'):
            if scroll:
                element = self.scroll_for_element(*locator)
                self.wait_until_element_to_be_clickable(locator, timeout)
                if os.getenv('os_version') == '13':
                    gevent.sleep(0.3)
                element.click()
                return element
            else:
                self.wait_until_element_to_be_clickable(locator, timeout)
                if os.getenv('os_version') == '13':
                    gevent.sleep(0.3)
                element = self.driver.find_element(*locator)
                element.click()
                return element

    # some elements are visible, but not clickable by appium logic...
    def tap_on_visible(self, *locator, timeout=implicit_sec, scroll=True):
        with step(f'Tap element - {locator}'):
            if scroll:
                element = self.scroll_for_element(*locator)
                self.wait_until_element_located(locator, timeout)
                element.click()
            else:
                self.wait_until_element_located(locator, timeout)
                self.driver.find_element(*locator).click()

    def open_menu(self, click_element, wait_element=""):
        if os.getenv('PLATFORM') == 'ios':
            self.open_menu_ios(click_element, wait_element)
        elif os.getenv('PLATFORM') == 'android':
            self.open_menu_android(click_element, wait_element)

    def open_menu_android(self, click_element, wait_element=""):
        self.tap(*click_element)
        if wait_element != "":
            try:
                self.wait_until_element_located(wait_element, timeout=3)
            except:
                gevent.sleep(1)
                self.tap(*click_element)
                self.wait_until_element_located(wait_element, timeout=3)
        else:
            try:
                self.wait_until_element_invisible(click_element, timeout=3)
            except:
                gevent.sleep(1)
                self.tap(*click_element)
                self.wait_until_element_invisible(click_element, timeout=3)

    def open_menu_ios(self, click_element, wait_element=""):
        element = self.tap(*click_element)
        try:
            element_id = element.get_attribute('wdUID')
            for _ in range(5):
                try:
                    element_after = self.find_element(*click_element, timeout=3)
                    element_after_id = element_after.get_attribute('wdUID')
                except:
                    element_after_id = ''
                if element_id == element_after_id:
                    element.click()
                    continue
                if wait_element == "":
                    return True
                if self.is_present(*wait_element, xml=False):
                    return True
                else:
                    gevent.sleep(1)
            self.wait_until_element_located(wait_element, timeout=5)  # Just to throw needed exception
        except StaleElementReferenceException:
            pass

    def tap_by_coordinates(self, x, y, tap_count=1):
        with step(f'Tap by coordinates - x={x} | y={y} | {tap_count} times'):
            TouchAction(self.driver).tap(x=x, y=y, count=tap_count).perform()

    def type(self, text, *locator):
        with step(f'Type text - {text} into locator - {locator}'):
            element = self.scroll_for_element(*locator)
            self.wait_until_element_located(locator)
            TouchAction(self.driver).move_to(element)
            element.click()
            element = self.scroll_for_element(*locator)
            if os.getenv('PLATFORM') == 'ios':
                self.clear_ios(element)
            else:
                element.clear()
            element.send_keys(text)

    def type_without_visible(self, text, *locator):
        with step(f'Type text - {text} into locator - {locator}'):
            element = self.driver.find_element(*locator)
            if os.getenv('PLATFORM') == 'ios':
                self.clear_ios(element)
            else:
                element.clear()
            element.send_keys(text)

    # https://github.com/appium/appium/issues/9752
    def clear_ios(self, element):
        actions = TouchAction(self.driver)
        actions.long_press(element)
        actions.perform()
        gevent.sleep(1)
        try:
            el3 = self.driver.find_element(*(MobileBy.ACCESSIBILITY_ID, 'Select All'))
            el3.click()

            el4 = self.driver.find_element(*(MobileBy.ACCESSIBILITY_ID, 'Cut'))
            el4.click()
        except NoSuchElementException:  # Input is empty
            pass

    def type_to_alert(self, text):
        attempts = 5
        for _ in range(attempts):
            try:
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                self.driver.switch_to.alert.send_keys(text)
                self.driver.switch_to.alert.accept()
                return True
            except:
                gevent.sleep(1)
        self.driver.switch_to.alert.send_keys(text)
        self.driver.switch_to.alert.accept()

    def is_present(self, *locator, timeout=implicit_sec, xml=True):
        try:
            self.find_element(*locator, timeout=timeout, xml=xml)
        except:
            return False
        return True

    def is_enabled(self, *locator, timeout=implicit_sec):
        try:
            element = self.scroll_for_element(*locator)
            element = self.find_element(*locator, timeout=timeout)
        except:
            return False
        return element.is_enabled()

    def get_text(self, *locator):
        return self.find_element(*locator).text

    def swipe_to_the_bottom_of_screen(self):
        dimensions = self.driver.get_window_size()
        start_point = int((dimensions['height'] * 0.5))
        scroll_end = int((dimensions['height'] * 0.2))
        try:
            self.driver.swipe(0, start_point, 0, scroll_end, 300)
            gevent.sleep(0.5)
        except WebDriverException:
            pass

    def swipe_to_the_top_of_screen(self, **kwargs):
        dimensions = self.driver.get_window_size()
        start_point = int((dimensions['height'] * 0.5))
        scroll_end = int((dimensions['height'] * 0.7))
        try:
            self.driver.swipe(0, start_point, 0, scroll_end, kwargs.get('scroll_speed', 300))
            gevent.sleep(kwargs.get('sleep', 0.2))
        except WebDriverException:
            pass

    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except:  # No alert present
            pass
        if os.getenv('PLATFORM') == 'android':
            try:
                self.tap(*(MobileBy.ID, 'android:id/button1'))
            except:
                pass

    def get_attribute(self, attribute, *locator):
        return self.driver.find_element(*locator).get_attribute(attribute)

    def submit_request_form(self, submit_btn, success_msg, close_btn):
        gevent.sleep(1)
        self.tap(*submit_btn)
        try:
            self.wait_until_element_located(success_msg, timeout=5)
        except:
            self.accept_alert()
            if not self.is_present(*success_msg, timeout=5):
                try:
                    self.tap(*submit_btn, timeout=5)
                except:
                    pass
                self.wait_until_element_located(success_msg)
        self.tap(*close_btn)

    def drag_and_drop_element_by_coord(self, element, x, y):
        actions = TouchAction(self.driver)
        actions.long_press(element).wait(1000).move_to(x=x, y=y).perform().release()
        gevent.sleep(1)

    def swipe_by_coord(self, x_start, y_start, x_end, y_end):
        TouchAction(self.driver).long_press(x=x_start, y=y_start).wait(1000).move_to(x=x_end,
                                                                                     y=y_end).release().perform()
