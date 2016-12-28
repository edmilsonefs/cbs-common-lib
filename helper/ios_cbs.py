import os
from time import sleep, time
import random

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

from testlio.base import TestlioAutomationTest


class CommonIOSHelper(TestlioAutomationTest):
    phone = False
    tablet = False
    needToAccept = True
    UIAWindow_XPATH = '//UIAApplication[1]/UIAWindow[1]'
    testdroid_device = os.getenv('TESTDROID_DEVICE')
    default_implicit_wait = 120
    show_name = 'American Gothic'
    user_type = 'anonymous'
    anonymous = 'anonymous'
    registered = 'registered'
    subscriber = 'subscriber'
    ex_subscriber = 'ex-subscriber'
    cf_subscriber = 'cf-subscriber'
    trial = 'trial'

    def setup_method(self, method, caps=False):
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
        self.event.stop()
        sleep(60)
        try:
            self.driver.quit()
            self.event.screenshot(self.screenshot())
        except:
            pass
        sleep(80)

    def find_by_uiautomation(self, value, hide_keyboard=False):
        return self.driver.find_element(By.IOS_UIAUTOMATION, value)

    def set_implicit_wait(self, wait_time=-1):
        """
        wrapper that sets implicit wait, defualts to self.default_implicit_wait
        """
        if wait_time == -1:
            wait_time = self.default_implicit_wait

        self.driver.implicitly_wait(wait_time)

    def find_on_page(self, find_by, find_key, max_swipes=10, x=.5):
        """
        Scrolls down the page looking for an element.  Call the method like this:
        self.find_on_page('name', 'Settings')
        self.find_on_page('id', 'com.cbs.app:id/seasonEpisode')
        """
        self.set_implicit_wait(3)

        for i in range(max_swipes):
            try:
                if find_by == 'accessibility_id':
                    e = self.driver.find_element_by_accessibility_id(find_key)
                elif find_by == 'id':
                    e = self.driver.find_element_by_id(find_key)
                elif find_by == 'xpath':
                    e = self.driver.find_element_by_xpath(find_key)
                else:
                    raise RuntimeError("invalid 'find_by'")

                if e.is_displayed():
                    self.set_implicit_wait()
                    return e
                else:
                    raise NoSuchElementException('pass')
            except NoSuchElementException:
                if self.is_simulator():
                    self.swipe(x, .5, x, 10, 1500)
                else:
                    self.swipe(x, .7, x, .8, 1000)
                pass

        self.set_implicit_wait()
        return False

    def send_text_native(self, value):
        self.driver.execute_script(
            'var vKeyboard = target.frontMostApp().keyboard(); vKeyboard.setInterKeyDelay(0.1); vKeyboard.typeString("%s");' % value)

    def go_to_sign_in(self):
        self.open_drawer()
        elems = self.driver.find_elements_by_xpath("//*[@name='Sign In']")
        self.click(element=elems[0])

    def click_already_have_cbs_account_sign_in(self):
        elem = self.driver.find_element_by_name('Already Have a CBS Account?').find_element_by_name('Sign In')
        self.click(element=elem, screenshot=True)

    def back(self):
        try:
            ta = TouchAction(self.driver)
            ta.press(x=25, y=25).release().perform()
            self.log_info("Press back")
        except:
            self.log_info("Fail to press back")

    def go_to_home(self):
        self._go_to('Home')

    def go_to_shows(self):
        self._go_to('Shows')

    def go_to_live_tv(self):
        self._go_to('Live TV')
        self._accept_alert(2)

    def go_to_schedule(self):
        self._go_to('Schedule')

    def go_to_my_cbs(self):
        self._go_to('My CBS')

    def _go_to(self, menu):
        self.safe_screenshot()
        try:
            self.click(element=self.get_element(xpath="//UIATableCell[@name='%s']" % menu))
        except:
            self.open_drawer()
            sleep(3)
            self.click(element=self.get_element(xpath="//UIATableCell[@name='%s']" % menu))

    def go_to_settings(self):
        self._go_to('Settings')

    def sign_out(self):
        self.click(element=self.get_clickable_element(id='Sign Out'))

    def go_to_sign_out(self):
        self.go_to_settings()
        self.sign_out()
        self.go_to_home()

    def open_drawer(self):
        count = 0
        while count < 10:
            try:
                self.click(element=self.get_clickable_element(id="Main Menu", timeout=30))
                break
            except:
                self.driver.tap([(25, 35)])
                count += 1

    def close_drawer(self):
        count = 0
        while count < 10:
            try:
                self.click(element=self.get_element(id="Main Menu"))
                break
            except:
                self.tap_by_touchaction(0.9, 0.01)
                count += 1

    def go_to_show(self, show_name):
        self.go_to_shows()
        self.click(element=self.get_clickable_element(id="Search", timeout=30))
        sleep(3)
        self.send_text_native(show_name)
        self.driver.tap([(80, 170)])
        # self.close_big_advertisement()

    def exists(self, **kwargs):
        """
        Finds element by name or xpath
        advanced:
            call using an element:
            my_layout = self.driver.find_element_by_class_name('android.widget.LinearLayout')
            self.exists(xpath="//*[@name='Submit']", driver=my_layout)
        """
        timeout = 30
        if kwargs.has_key('timeout'):
            timeout = kwargs['timeout']
        try:
            if kwargs.has_key('name'):
                try:
                    return self.get_element(xpath=
                        "//*[@name='" + kwargs['name'] + "' or @value='" + kwargs['name'] + "']", timeout=timeout)
                except:
                    e = self.get_element(xpath='//*[contains(@name,"%s")]' % kwargs['name'], timeout=timeout)
            elif kwargs.has_key('class_name'):
                e = self.get_element(class_name=kwargs['class_name'], timeout=timeout)
            elif kwargs.has_key('id'):
                e = self.get_element(id=kwargs['id'], timeout=timeout)
            elif kwargs.has_key('xpath'):
                e = self.get_element(xpath=kwargs['xpath'], timeout=timeout)
            else:
                raise RuntimeError("exists() called with incorrect param. kwargs = %s" % kwargs)

            return e
        except:
            return False

    def verify_exists(self, **kwargs):
        screenshot = False
        if kwargs.has_key('screenshot') and kwargs['screenshot']:
            screenshot = True

        selector = ""
        if kwargs.has_key('name'):
            selector = kwargs['name']
        elif kwargs.has_key('class_name'):
            selector = kwargs['class_name']
        elif kwargs.has_key('id'):
            selector = kwargs['id']
        elif kwargs.has_key('xpath'):
            selector = kwargs['xpath']

        self.assertTrueWithScreenShot(self.exists(**kwargs), screenshot=screenshot,
                                      msg="Should see element with text or selector: '%s'" % selector)

    def verify_not_exists(self, **kwargs):
        screenshot = False
        if kwargs.has_key('screenshot') and kwargs['screenshot']:
            screenshot = True

        selector = ""
        if kwargs.has_key('name'):
            selector = kwargs['name']
        elif kwargs.has_key('class_name'):
            selector = kwargs['class_name']
        elif kwargs.has_key('id'):
            selector = kwargs['id']
        elif kwargs.has_key('xpath'):
            selector = kwargs['xpath']

        self.assertTrueWithScreenShot(not self.exists(**kwargs), screenshot=screenshot,
                                      msg="Should NOT see element with text or selector: '%s'" % selector)

    def _accept_alert(self, count):
        for x in range(0, count):
            try:
                # Accepts terms of service & other popups there may be
                self.wait_and_accept_alert()
                sleep(5)
                break
            except:
                pass

    def swipe(self, startx, starty, endx, endy, swipe_time=None):
        # Converts relative args such as swipe(.5, .5, .5, .2, 1000)
        # to actual numbers such as (500, 500, 500, 200, 1000) based on current screen size.
        # Apparently some versions of appium don't handle this correctly. Surprising.

        if startx < 1 or starty < 1 or endx < 1 or endy < 1:
            s = self.driver.get_window_size()
            width = s['width']
            height = s['height']

            if startx < 1:
                startx = startx * width
            if endx < 1:
                endx = endx * width
            if starty < 1:
                starty = starty * height
            if endy < 1:
                endy = endy * height

        endx = endx - startx
        endy = endy - starty

        self.driver.swipe(startx, starty, endx, endy, swipe_time)

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
        start_y = size['height'] / 4
        end_y = -100

        self.driver.swipe(x, start_y, x, end_y, duration)
        sleep(1)

    def click_safe(self, **kwargs):
        """
        Waits for element to exist before trying to click.  Default wait = current implicit wait
        Does NOT throw an error if element does not exist.
        If true - click and return the element.  If false - return False

        example:
        self.click_safe(id='com.cbs.app:id/showcase_button', timeout=10)
        """
        element_or_false = self.exists(**kwargs)

        if element_or_false:
            element_or_false.click()
            return True
        else:
            return False

    def click_by_location(self, elem, **kwargs):
        """
        sometimes elem.click() fails for whatever reason.  get x,y coords and click by that
        """
        loc = elem.location
        size = elem.size
        x = loc['x'] + size['width'] / 2
        y = loc['y'] + size['height'] / 2

        # an array of tuples
        self.tap(x, y)

    def click_on_first_aa_video(self):
        # elFrom = self._find_element(id='Free Episodes')
        # elTo = self._find_element(id='Main Menu')
        # self.driver.scroll(elFrom, elTo)
        aa_xpath = "//UIATableCell[contains(@name,'Primetime')]//UIACollectionView[1]//UIACollectionCell[2]"
        if not self.exists(xpath=aa_xpath, timeout=10):
            self._short_swipe_down(duration=5000)
        # count = 1
        # if self.phone:
        #     max_count = 2
        # else:
        #     max_count = 3
        # while count <= max_count:
        self.safe_screenshot()
        self.click(xpath=aa_xpath)
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

    def click_return(self):
        size = self.driver.get_window_size()
        self.driver.tap([(size['width'] - 30, size['height'] - 30)])
        # try:
        #     self.driver.hide_keyboard('Return')
        # except:
        #     pass

    def hide_keyboard(self):
        if self.phone:
            size = self.driver.get_window_size()

            x = size['width'] / 2
            start_y = size['height'] / 2
            end_y = size['height']

            self.driver.swipe(x, start_y, x, end_y, 500)
        elif self.tablet:
            size = self.driver.get_window_size()
            self.driver.tap([(size['width'] - 30, size['height'] - 30)])

    def close_big_advertisement(self):
        if self.exists(id='Close Advertisement', timeout=10):
            self.click(id='Close Advertisement')

    def back_while_open_drawer_is_visible(self):
        counter = 0
        try:
            self.driver.implicitly_wait(10)
        except:
            pass
        while counter < 10:
            try:
                if self.user_type in [self.subscriber, self.cf_subscriber, self.trial]:
                    self.driver.find_element_by_id("CBSLogo_AllAccess_white").is_displayed()
                    break
                else:
                    self.driver.find_element_by_id("CBSLogo_white").is_displayed()
                    break
            except:
                self.back()
                counter += 1
        try:
            self.driver.implicitly_wait(30)
        except:
            pass

    def validation_upsell_page(self):
        self.verify_exists(id='com.cbs.app:id/allAccessLogo', screenshot=True)
        if self.user_type in [self.anonymous, self.registered]:
            self.verify_exists(xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
            self.verify_exists(xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                     "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
            self.verify_exists(name='GET STARTED')
            if self.user_type == self.registered:
                self.verify_not_exists(name='SELECT', timeout=10)
        elif self.user_type in [self.subscriber, self.trial]:
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
            self.verify_exists(xpath="//*[contains(@text,'UPGRADE')]")
        elif self.user_type == self.cf_subscriber:
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
            self.verify_exists(xpath="//*[contains(@text,'READ OUR FAQ')]")
        else:
            if self.user_type == self.ex_subscriber:
                self.verify_exists(xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
                self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
                self.verify_exists(xpath="//*[contains(@text,'Only $ 5.99/month')]")
                self.verify_exists(name='SELECT')
                self.verify_not_exists(xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                             "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]", timeout=10)
                self.verify_not_exists(name='GET STARTED', timeout=10)

    def tap_by_touchaction(self, x, y):
        x, y = self._convert_relative_x_y(x, y)

        ta = TouchAction(self.driver)
        ta.press(x=x, y=y).release().perform()

    def tap(self, x, y):
        # Converts relative args such as click(.5, .5)
        # to actual numbers such as (515, 840) based on current screen size.
        # Apparently some versions of appium don't handle this correctly. Surprising.

        x, y = self._convert_relative_x_y(x, y)
        self.driver.tap([(x, y)])

    def tap_element(self, **kwargs):
        elem = self._find_element(**kwargs)
        action = TouchAction(self.driver)
        action.long_press(elem).perform()

    def _convert_relative_x_y(self, x, y):
        if x < 1 or y < 1:
            s = self.driver.get_window_size()
            width = s['width']
            height = s['height']

            if x < 1:
                x = x * width
            if y < 1:
                y = y * height

        return x, y

    def video_done_button(self):
        self.safe_screenshot()
        # try:
        try:
            ta = TouchAction(self.driver)
            ta.press(x=100, y=100).release().perform()
        except:
            pass
        self.safe_screenshot()
        try:
            self.click(id="Done", timeout=2)
        except:
            try:
                ta = TouchAction(self.driver)
                ta.press(x=100, y=100).release().perform()
            except:
                pass
            self.click(id="Done", timeout=5)
        self.log_info("End of stream")
        self.safe_screenshot()

    def safe_screenshot(self):
        try:
            self.event.screenshot(self.screenshot())
        except:
            pass

    def close_video(self):
        count = 0
        while count < 10:
            if self.verify_exists(id="Search", timeout=5):
                break
            else:
                self.video_done_button()
                count += 1

    def log_info(self, info):
        self.event._log_info(self.event._event_data(info))

    def click_facebook_icon(self):
        self.click(id='FacebookLogo')

    ####################################################################################
    # LOGIN
    def set_sign_in_email(self, email):
        elem = self._find_element(xpath=self.UIAWindow_XPATH + "/UIATextField[@value='Email']")
        self.send_text(element=elem, data=email)

    def set_sign_in_password(self, password):
        elem = self._find_element(xpath=self.UIAWindow_XPATH + '/UIASecureTextField[1]')
        self.send_text(element=elem, data=password)

    def login(self, email, password):
        self.set_sign_in_email(email)
        self.set_sign_in_password(password)

        self.click(xpath='(//UIAButton[@name="SIGN IN"])')

        self.finish_login()

    def finish_login(self):
        # Complete registration if required

        self.driver.implicitly_wait(10)
        try:
            self.tap_element(xpath=self.UIAWindow_XPATH + "//UIAScrollView[./UIAButton[@name='CONTINUE']]//UIAButton[1]")
            self.click(accessibility_id='CONTINUE')
            sleep(3)
            self.event.screenshot(self.screenshot())
        except:
            try:
                self.driver.find_element_by_id(accessibility_id='CONTINUE', timeout=5)
            except:
                self.tap_element(xpath=self.UIAWindow_XPATH + "//UIAScrollView[./UIAButton[@name='CONTINUE']]//UIAButton[1]")
                self.click(accessibility_id='CONTINUE')
                sleep(3)
                self.event.screenshot(self.screenshot())
            self.event.screenshot(self.screenshot())
        self.driver.implicitly_wait(30)

    def login_optimum(self, username, password):
        email_field = self.driver.find_element_by_class_name('UIATextField').click()
        self.send_keys(element=email_field, data=username, class_name='UIATextField')

        password_field_element = self.driver.find_element_by_xpath(
            '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIASecureTextField[1]')
        self.click(password_field_element)
        self.send_keys(element=password_field_element, data=password)


        if self.tablet:
            self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAImage[3]')
        else:
            self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAImage[2]')
        self.event.screenshot(self.screenshot())
        sleep(5)

    ####################################################################################
    # SEARCH

    def enter_search_text(self, what_to_search_for):
        e = self.find_search_text()
        self.send_keys(element=e, data=what_to_search_for)

    def search_for(self, what_to_search_for):
        self.click_search_icon()
        self.enter_search_text(what_to_search_for)

    def click_first_search_result(self):
        element = self.get_search_result_episode_count_element()
        element.click()

    def find_search_text(self):
        if self.exists(id='Search for a Show', timeout=2):
            return self._find_element(id='Search for a Show')
        else:
            return self.driver.find_elements_by_class_name('UIATextField')[-1]

    def click_search_icon(self):
        self.click(xpath="//UIAButton[@name='Search']")
        self.event.screenshot(self.screenshot())

    def get_search_result_episode_count_element(self):
        collection_views = self.driver.find_elements_by_xpath("//*[@value='page 1 of 1']")

        for cell in collection_views:
            static_texts = cell.find_elements_by_class_name('UIAStaticText')
            for static_text in static_texts:
                if ' Episode' in static_text.text:
                    return static_text
    ####################################################################################
    # SWIPE
    def swipe_element_to_top_of_screen(self):
        """
        Swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        window_size_y = self.driver.get_window_size()["height"]
        self.swipe(30, window_size_y - 400, 30, window_size_y - 20)

    def swipe_element_to_bottom_of_screen(self):
        """
        Swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        window_size_y = self.driver.get_window_size()["height"]
        self.swipe(30, window_size_y - 80, 30, window_size_y - 500)

    def short_swipe_down(self):
        window_size_y = self.driver.get_window_size()["height"]
        self.swipe(30, window_size_y - 100, 30, window_size_y - 150)

    def short_swipe_down_if_element_is_not_visible(self, id=None, class_name=None):
        """
        function that search for element, if element is not found swipe the page until element is found on screen
        """
        self.driver.implicitly_wait(0)

        element = None
        count = 0
        while element is None and count <= 20:
            try:
                if id:
                    element = self.driver.find_element_by_id(id_=id)
                if class_name:
                    element = self.driver.find_element_by_class_name(class_name)
            except:
                self.short_swipe_down()
                count += 1

        self.driver.implicitly_wait(30)

    def header_back_button(self):
        self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
        sleep(2)


    def click_first_show_page_episode(self):
        self.tap_element(xpath=self.UIAWindow_XPATH + '/UIAScrollView[1]/UIATableView[1]/UIATableCell[1]/UIACollectionView[1]/UIACollectionCell[1]')

    def select_optimum_from_provider_page(self):
        self.click(xpath='//UIACollectionCell[2]')

    def go_to_optimum_page(self):
        self.go_to_providers_page()
        self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')

    def go_to_providers_page(self):
        self.go_to_live_tv()
        self.select_verify_now()

    def select_verify_now(self):
        self.click(id='VERIFY NOW')

    def start_watching_button(self):
        self.click(id='Start Watching')

