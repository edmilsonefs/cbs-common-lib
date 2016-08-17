import os
import random
import subprocess
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from testlio.base import TestlioAutomationTest

class CommonIOSHelper(TestlioAutomationTest):
    phone = False
    tablet = False
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
        self.click(id="Search")
        self.send_text_native(show_name)
        self.driver.tap([(50, 150)])