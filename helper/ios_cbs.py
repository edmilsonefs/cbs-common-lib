import os
import random
import subprocess
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from testlio.base import TestlioAutomationTest

class CommonIOSHelper(TestlioAutomationTest):
    phone = False
    tablet = False
    needToAccept = True
    testdroid_device = os.getenv('TESTDROID_DEVICE')
    default_implicit_wait = 120

    def setup_method(self, method, caps = False):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi off", shell=True)
        super(CommonIOSHelper, self).setup_method(method, caps)

        if 'iPad' in self.driver.capabilities['deviceName']:
            self.tablet = True
            self.phone = False
        else:
            self.tablet = False
            self.phone = True

    def teardown_method(self, method):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi on", shell=True)
        super(CommonIOSHelper, self).teardown_method(method)

    def find_by_uiautomation(self, value, hide_keyboard=False):
        return self.driver.find_element(By.IOS_UIAUTOMATION, value)

    def send_text_native(self, value):
        self.driver.execute_script(
            'var vKeyboard = target.frontMostApp().keyboard(); vKeyboard.setInterKeyDelay(0.1); vKeyboard.typeString("%s");' % value)

    def go_to_sign_in(self):
        self.open_drawer()
        elems = self.driver.find_elements_by_xpath("//*[@name='Sign In']")
        self.click(element=elems[0])

    def back(self):
        self.click(xpath=self.UIAWindow_XPATH + '/UIAButton[2]')

    def go_to_home(self):
        self._go_to('Home')

    def go_to_shows(self):
        self._go_to('Shows')

    def go_to_live_tv(self):
        self._go_to('Live TV')
        self._accept_alert(1)

    def go_to_schedule(self):
        self._go_to('Schedule')

    def go_to_my_cbs(self):
        self._go_to('My CBS')

    def _go_to(self, menu):
        self.open_drawer()
        self.click(xpath="//*[@name='%s' or @value='%s']" % (menu, menu))

    def go_to_settings(self):
        self.open_drawer()
        self.click(xpath="//*[@name='Settings']")

    def open_drawer(self):
        self.driver.implicitly_wait(30)
        count = 0
        while count < 10:
            try:
                self.click(id="Main Menu")
                break
            except:
                self.driver.tap([(25, 35)])
                count += 1

    def close_drawer(self):
        self.driver.back()

    def go_to_show(self, show_name):
        self.go_to_shows()
        # self.click(id="Search")
        # self.send_text_native(show_name)
        self.driver.tap([(80, 170)])

    def _accept_alert(self, count):
        for x in range(0, count):
            try:
                # Accepts terms of service & other popups there may be
                self.wait_and_accept_alert()
                sleep(5)
                break
            except:
                pass

    def _short_swipe_up(self, duration=1000, side='middle'):
        size = self.driver.get_window_size()
        if side == 'middle':
            x = size['width'] / 2
        elif side == 'left':
            x = 50
        elif side == 'right':
            x = size['width'] - 50
        start_y = size['height'] / 2
        end_y = size['height'] - 50

        self.driver.swipe(x, start_y, x, end_y, duration)
        sleep(1)

    def _short_swipe_down(self, duration=4000, side='middle'):
        size = self.driver.get_window_size()
        if side == 'middle':
            x = size['width'] / 2
        elif side == 'left':
            x = 50
        elif side == 'right':
            x = size['width'] - 50
        start_y = size['height'] / 2
        end_y = 50

        self.driver.swipe(x, start_y, x, end_y, duration)
        sleep(1)

    def click_on_first_aa_video(self):
        # count = 1
        # if self.phone:
        #     max_count = 2
        # else:
        #     max_count = 3
        # while count <= max_count:
        self.click(
            xpath="//UIATableCell[contains(@name,'Primetime')]//UIACollectionView[1]//UIACollectionCell[1]")
        if self.needToAccept:
            self._accept_alert(1)
            self.needToAccept = False

            # try:
            #     self.event.screenshot(self.screenshot())
            #     self.driver.find_element_by_id('TRY 1 WEEK FREE*')
            # except:
            #     self.event.screenshot(self.screenshot())
            #     try:
            #         self.driver.find_element_by_id('Cancel').click()
            #     except:
            #         self.driver.tap([(100, 100)])
            #         self.driver.find_element_by_id('Done').click()
            #         count += 1