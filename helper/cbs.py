import os
import random
import re
import subprocess
from email.mime.text import MIMEText
from smtplib import SMTP
from time import sleep, time
from xml.etree import ElementTree

from selenium.common.exceptions import NoSuchElementException, WebDriverException

from testlio.base import TestlioAutomationTest


class CommonHelper(TestlioAutomationTest):
    created_email_from_address = 'jfreight33@gmail.com'
    created_email_from_password = 'testing789'
    created_email_to_address_list = 'valdo@testlio.com'
    phone = False
    tablet = False
    IS_AMAZON = False
    testdroid_device = os.getenv('TESTDROID_DEVICE')
    passed = False
    user_type = 'anonymous'
    anonymous = 'anonymous'
    registered = 'registered'
    subscriber = 'subscriber'
    ex_subscriber = 'ex-subscriber'
    cf_subscriber = 'cf-subscriber'
    trial = 'trial'
    show_name = 'American Gothic'
    com_cbs_app = 'com.cbs.app'

    def setup_method(self, method, caps=False):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi off", shell=True)
        super(CommonHelper, self).setup_method(method, caps)

        self.init_variables()

    def init_variables(self):
        if os.getenv('LOCAL') is None:
            self.testdroid_device = self.get_testdroid_device_from_adb()
        self.activate_standard_keyboard()
        #self.driver.orientation = 'PORTRAIT'
        if 'Nexus 7' in self.testdroid_device \
                or 'KFTBWI' in self.testdroid_device:
            self.tablet = True
            self.phone = False
        else:
            self.tablet = False
            self.phone = True
        if 'KFTBWI' in self.testdroid_device:
            self.com_cbs_app = 'com.cbs.ott'
            self.IS_AMAZON = True

    def teardown_method(self, method):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi on", shell=True)
        if self.passed:
            self.event.start(data='Test completed successfully')
        else:
            self.event.start(data='Test failed. Getting screenshot and page_source.')
            if self.driver:
                self.safe_screenshot()
                try:
                    self.driver.page_source
                except Exception:
                    self.event.start(data='in teardown: page source failed')
        super(CommonHelper, self).teardown_method(method)

    def safe_screenshot(self):
        try:
            self.event.screenshot(self.screenshot())
        except Exception:
            self.event.start(data='in teardown: screenshot failed')

    def get_testdroid_device_from_adb(self):
        """
        Mapping of device model names (as returned by adb getprop) to testdroid device names
        """
        lookup = {}
        lookup['KFTBWI'] = 'KFTBWI'
        lookup['831C'] = 'HTC_M8x'
        lookup['Nexus 5'] = 'LGE Nexus 5'
        lookup['Nexus 5'] = 'LGE Nexus 5 6.0'
        lookup['Nexus 5X'] = 'LGE Nexus 5X'
        lookup['Nexus 6'] = 'motorola Nexus 6'
        lookup['Nexus 7'] = 'asus Nexus 7'
        lookup['?'] = 'samsung GT-N7100'
        lookup['GT-N7100'] = 'samsung GT-N7100'
        lookup['SAMSUNG-SM-N900A'] = 'samsung SAMSUNG-SM-N900A'
        lookup['SM-N920R4'] = 'Samsung Galaxy Note 5'
        lookup['SAMSUNG-SGH-I747'] = 'samsung SAMSUNG-SGH-I747'
        lookup['GT-I9500'] = 'samsung GT-I9500'
        lookup['SAMSUNG-SM-G900A'] = 'samsung SAMSUNG-SM-G900A'
        lookup['SAMSUNG-SM-G930A'] = 'samsung SAMSUNG-SM-G930A'
        lookup['SM-T330NU'] = 'samsung SM-T330NU'

        adb_device_name = subprocess.check_output(['adb', 'shell', 'getprop ro.product.model']).strip()
        return lookup[adb_device_name]

    def click_until_element_is_visible(self, element_to_be_visible, element_to_click):
        self.driver.implicitly_wait(20)

        element = None
        count = 0
        while element is None and count < 10:
            try:
                element = self.driver.find_element_by_name(element_to_be_visible)
            except:
                self.click(name=element_to_click)
                count += 1
        self.driver.implicitly_wait(30)

    def go_to_menu_page_and_select_option(self, menu_option):
        # This is to avoid navigation drawer not being clicked properly
        count = 0
        self.driver.implicitly_wait(10)
        while count < 30:
            try:
                self.driver.find_element_by_name('Open navigation drawer').click()
                self.driver.find_element_by_name(menu_option).click()
                break
            except:
                pass
            count += 1
        self.driver.implicitly_wait(30)

    ################################################
    # HEADER
    def open_drawer(self):
        """
        Opens side drawer if it's not open.  If we're up a level (viewing a show) it will go back, then open the drawer.
        """
        el = self.exists(name='Open navigation drawer', timeout=3)
        if el:
            el.click()
        else:
            # maybe we're a level deeper.  Try going back.
            self.go_back()

            # if the drawer is NOT already open, try again and throw err on failure
            if not self.is_drawer_open():
                self.click(name='Open navigation drawer')

        sleep(1.5)

    def is_drawer_open(self):
        return not self.exists(name='Open navigation drawer', timeout=3)

    def close_drawer(self):
        self.back()

    def navigate_up(self):
        self.click(name='Navigate up')

    def select_search_icon(self):
        self.click(id=self.com_cbs_app + ':id/action_search')
        self.event.screenshot(self.screenshot())

    def click_search_icon(self):
        self.click(id=self.com_cbs_app + ':id/action_search')

    def click_search_text(self):
        self.click(id=self.com_cbs_app + ':id/search_src_text')

    def click_clear_search(self):
        self.click(id=self.com_cbs_app + ':id/search_close_btn')

    def click_search_back(self):
        # self.click(id=self.com_cbs_app + ':id/closeButton')
        self.click(name='Navigate up')  # home->search
        # Todo analyze this, as it's the same as navigate up

    ################################################
    # MENU

    def _go_to(self, menu):
        self.driver.implicitly_wait(8)
        drawer = self._find_element(id=self.com_cbs_app + ':id/navigation_drawer')
        self.click(element=drawer.find_element_by_name(menu), data='Click on menu item %s' % menu)
        self.driver.implicitly_wait(20)

    def goto_sign_in(self):
        self.open_drawer()

        # on some screens (live tv), the text 'Sign In' appears twice, so be sure we get the right one...
        drawer = self.driver.find_element_by_id(self.com_cbs_app + ':id/userInfoHolder')
        sign_in = drawer.find_element_by_name('Sign In')
        self.click(element=sign_in, data='Click on menu item Sign In')
        self._hide_keyboard()

    def goto_signup(self):
        self.goto_sign_in()
        self._hide_keyboard()
        sleep(1)

        if not self.click_safe(name="Don't have an account? Sign Up"):
            self.click(name="Sign Up")

        self.verify_exists(name='Sign up with your email')
        sleep(1)

    def goto_home(self):
        self.open_drawer()
        self._go_to('Home')

    def goto_shows(self):
        self.open_drawer()
        self._go_to('Shows')

    def goto_subscribe(self):
        self.open_drawer()
        self._go_to('Subscribe')

    def goto_live_tv(self):
        self.open_drawer()
        self._go_to('Live TV')
        self.click_allow_popup()
        self.driver.implicitly_wait(120)

    def goto_schedule(self):
        self.open_drawer()
        self._go_to('Schedule')

    def goto_settings(self):
        self.open_drawer()
        self._go_to('Settings')

    def goto_show(self, show_name):
        self.select_search_icon()
        self.wait_for_show_page_to_load()

        self.send_keys_on_search_field(show_name)
        self.click_first_search_result()
        sleep(10)

    # def goto_show(self, show_title):
    #     """
    #     Uses search functionality, goes to show page, verifies it's on a show page
    #     """
    #     self.search_for(show_title)
    #     self.click_first_search_result()
    #     self.wait_for_show_page_to_load()

    ################################################
    # LOGIN

    def sign_in_twitter(self, email, password):
        self.goto_sign_in()
        self.click_twitter_icon()

        if 'SGH-I747' in self.testdroid_device or 'SM-N900A' in self.testdroid_device:
            self.login_through_twitter_by_multi_tap(email, password)
        else:
            self.login_through_twitter(email, password)

        self._complete_reg()
        self._post_login()

    def sign_in_gplus(self):
        self.goto_sign_in()
        self.click_gplus_icon()
        self.login_through_gplus()

        # if we see "CBS would like to: Know your basic profile..."
        for i in range(4):
            e = self.exists(name='Allow', timeout=5)
            if e:
                e.click()
            else:
                break

        self._complete_reg()
        self._post_login()

    def sign_in_facebook(self, email, password):
        self.goto_sign_in()
        self.click_facebook_icon()
        self.choose_and_perform_facebook_scenario(email, password)

        self._complete_reg()
        self._post_login()

    def choose_and_perform_facebook_scenario(self, email, password):
        """
        If device is in the list of devices that has FB installed, login through the app,
        otherwise, login through the webview
        """
        self.login_through_facebook_webview(email, password)

    def login_through_gplus(self):
        sleep(30)
        self.safe_screenshot()
        self.click(id='com.google.android.gms:id/account_name')
        sleep(5)
        self.safe_screenshot()

    def login_through_facebook_webview(self, email_text, password_text):
        """
        Logs in through FB webview after making sure the textfields appear
        """
        sleep(30)

        count = 0
        while count < 5:
            try:
                self.set_implicit_wait(60)
                self.driver.find_element_by_class_name("android.widget.EditText")
                self.driver.find_element_by_class_name("android.widget.Button")
                break
            except:
                self.hw_back()
                self.goto_sign_in()
                self.click_facebook_icon()
                pass
            count += 1

        self.set_implicit_wait()
        sleep(10)

        fields = self.driver.find_elements_by_class_name("android.widget.EditText")
        email = fields[0]
        password = fields[1]

        # start from the bottom up
        self.send_keys(data=email_text, element=email)
        self._hide_keyboard()
        self.send_keys(data=password_text, element=password)
        self._hide_keyboard()
        self.event.screenshot(self.screenshot())  # per spec

        # login_button = self.driver.find_elements_by_class_name('android.widget.Button')[0]
        # self.click(element=login_button)
        self.click(class_name='android.widget.Button')

        sleep(30)
        self.event.screenshot(self.screenshot())  # per spec

        if self.exists(class_name='android.webkit.WebView') or self.exists(name='You have already authorized CBS.com.',
                                                                           timeout=5):
            if self.exists(class_name='android.widget.Button', timeout=5):
                bs = self.driver.find_elements_by_class_name("android.widget.Button")
                bs[1].click()
                sleep(4)

            else:
                # Quite the hack:
                # Try several times, moving down the screen, to tap the "OK" on the webview
                y = .75
                while self.exists(class_name='android.webkit.WebView', timeout=10) and y < .95:
                    self.tap(.65, y)
                    y += .03
                    sleep(3)

        sleep(30)
        self.event.screenshot(self.screenshot())  # per spec

    def login_through_twitter_by_multi_tap(self, email_text, password_text):
        """
        A couple phones are too old (4.3) to have webviews correctly work, so we tap by x,y coords
        """
        self.exists(class_name='android.webkit.WebView', timeout=60)
        sleep(20)

        # What we're doing here is doing lots of taps in a row, trying to find the button.
        # It's actually not that slow.
        y = .35
        for i in range(10):
            self.tap(.4, y)
            sleep(1)
            if self.is_keyboard_displayed():
                self.tap(.4, y)
                break
            y += .01

        sleep(1)
        self.tap_keys_on_keyboard(email_text + '\t')
        sleep(1)
        self.tap_keys_on_keyboard(password_text + '\t')
        sleep(1)
        self.event.screenshot(self.screenshot())  # per spec

        # tap authorize button
        self.tap_keys_on_keyboard('\n')
        sleep(10)

        # popup says "Do you want to save your password?"
        self.click_safe(name='Not now', timeout=10)

        self.event.screenshot(self.screenshot())  # per spec

    def login_through_twitter(self, email_text, password_text):
        """
        Logs in through Twitter webview
        """
        sleep(30)
        self.set_implicit_wait()

        count = 0
        while count < 5:
            try:
                sleep(10)
                self.driver.find_element_by_class_name('android.widget.EditText')
                break
            except:
                self.hw_back()
                self.goto_sign_in()
                self.click_twitter_icon()
            count += 1

        sleep(10)

        fields = self.driver.find_elements_by_class_name('android.widget.EditText')
        email = fields[0]
        password = fields[1]

        # start from the bottom up
        self.send_keys(data=email_text, element=email)
        self._hide_keyboard()
        self.send_keys(data=password_text, element=password)
        self._hide_keyboard()

        self.event.screenshot(self.screenshot())  # per spec

        # e = self._find_element(name='Username or email')
        # self.swipe_element_to_top_of_screen(e)
        # login_button = self.driver.find_elements_by_class_name("android.widget.Button")[0]
        # self.click(element=login_button)
        self.click(class_name="android.widget.Button")

        sleep(20)

        # popup says "Do you want to save your password?"
        self.click_safe(name='Not now', timeout=10)

    def _complete_reg(self):
        """
        Deals with Term & Conditions popup and calls click_submit
        """
        # Complete registration if required
        self.exists(id=self.com_cbs_app + ':id/terms_accept_checkBox', timeout=300)
        self.click(id=self.com_cbs_app + ':id/terms_accept_checkBox')
        self.click_submit()

    def _post_login(self):
        """
        After logging in (regardless of email, facebook, twitter, etc.)
        several things can happen including Upgrade popups, Use Location? popups, etc.
        Verifies that login was successful
        Also closes nav drawer if it's open
        """
        if self.exists(name='CBS All Access', timeout=30) or self.exists(name='Upgrade Account', timeout=5):
            self.hw_back()

        if self.exists(name='Use location?', timeout=5):
            if not self.click_safe(name='Yes', timeout=5):
                self.click(name='YES')

        self.back_while_open_drawer_is_visible()
        self.open_drawer()
        self.assertTrueWithScreenShot(self.not_exists(name='Sign In', timeout=1), screenshot=True,
                                      msg="Verify 'Sign In' not an option in menu after logging in.")
        self.close_drawer()

    def login(self, username, password):
        """
        Does the work - enters email/pwd, then calls some post-login functions
        This assumes you are on the Sign In screen.
        """
        self._hide_keyboard()
        textfields = self.driver.find_elements_by_class_name('android.widget.EditText')
        textfields[0].click()
        self.send_keys(element=textfields[0], data=username)
        self.driver.hide_keyboard('With Email')

        textfields[1].click()
        self.send_keys(element=textfields[1], data=password)
        self._hide_keyboard()
        sleep(1)

        # textview also says Sign In (on phone at least)
        self.click(xpath="//android.widget.Button[@text='Sign In']")

        self._complete_reg()
        self._post_login()

    def wait_for_show_page_to_load(self):
        count = 0
        while count < 10:
            if self.exists(class_name='android.widget.ProgressBar', timeout=5):
                sleep(5)
                count += 1
            else:
                break

    def hw_power(self):
        self.driver.press_keycode(26)

    def hw_back(self):
        self.driver.press_keycode(4)

    def hw_enter(self):
        self.driver.press_keycode(66)

    def hw_home(self):
        self.driver.press_keycode(3)

    def hw_switch_apps(self):
        self.driver.press_keycode(187)

    def send_keys_on_search_field(self, show_name):
        search_field = self.click(id=self.com_cbs_app + ':id/search_src_text')
        self.send_keys(show_name, search_field)
        self._hide_keyboard()
        sleep(5)
        self.event.screenshot(self.screenshot())

    def send_keys_with_retry(self, element, string, retries=4):
        """
        Tries a few times to enter the string and then make sure it's entered correctly.
        The "length" part is because sometimes we send "hello" but then the element will add
        its own text, and say something like "hello is being searched for"
        """
        length = len(string)

        for i in range(retries):
            self.send_keys(string + '\n', element)
            if element.text[0:length] != string:
                element.clear()
            else:
                break

    def activate_standard_keyboard(self):
        """
        Looks through the device's system keyboards and activates the correct one.  Should prevent things like
        the @ symbol in "user@gmail.com" turning into "user2gmail.com" when using send_keys().  Saw this on older
        phones sometimes.
        """
        for kybd in self.driver.available_ime_engines:
            if 'samsungkeypad' in kybd.lower():
                self.driver.activate_ime_engine(kybd)
                return

            if ('latin' in kybd.lower() or
                        'samsung' in kybd.lower() or
                        'htc' in kybd.lower() or
                        'amazon' in kybd.lower()):
                new_kybd = kybd

        try:
            self.driver.activate_ime_engine(new_kybd)
        except:
            pass

    def tap_keys_on_keyboard(self, txt):
        """
        Sometimes send_keys() doesn't work. Sometimes you just have to tap the keys yourself.
        This will currently work for a limited set of keyboard keys.
        See all Android keycodes at http://developer.android.com/reference/android/view/KeyEvent.html

        example: self.tap_keys_on_keyboard('some string')
        """
        dct = {'-': 69, '=': 70, '[': 71, ']': 72, '\\': 73, ';': 74, '\'': 75, '/': 76, ' ': 62, ',': 55, '.': 56,
               '\t': 61, '\r': 66, '\n': 66}
        dct2 = {')': 7, '!': 8, '@': 9, '#': 10, '$': 11, '%': 12, '^': 13, '&': 14, '*': 15, '(': 16, '_': 69, '+': 70,
                '{': 71, '}': 72, '|': 73, ':': 74, '"': 75, '?': 76, '<': 55, '>': 56}

        for char in txt:
            metastate = 0

            if re.search(r'[0-9]', char):
                i = ord(char) - 41
            elif re.search(r'[a-z]', char):
                i = ord(char) - 68
            elif re.search(r'[A-Z]', char):
                i = ord(char) - 36
                metastate = 1
            elif char in dct:
                i = dct[char]
            elif char in dct2:
                i = dct2[char]
                metastate = 1
            else:
                raise RuntimeError("got a char I don't think we can tap: %s" % char)

            self.driver.press_keycode(i, metastate)

    def click_allow_popup(self):
        if self.exists(name='Allow', timeout=10):
            try:
                if self.phone:
                    self.click_until_element_is_visible("Open navigation drawer", "Allow")
                else:
                    self.click_until_element_is_visible("Navigate up", "Allow")
            except:
                pass

    def click_by_location(self, elem, msg=None, **kwargs):
        """
        sometimes elem.click() fails for whatever reason.  get x,y coords and click by that
        """
        if kwargs['side'] is None:
            kwargs['side'] = 'middle'

        loc = elem.location
        size = elem.size
        if self.tablet:
            if kwargs['side'] == 'middle':
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'left':
                x = loc['x'] + size['width'] / 4
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'right':
                x = loc['x'] + size['width'] - 10
                y = loc['y'] + 10

        elif self.phone:
            if kwargs['side'] == 'middle':
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'left':
                x = loc['x'] + size['width'] / 4
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'right':
                x = loc['x'] + size['width'] - size['width'] / 4
                y = loc['y'] + size['height'] / 2

        if not msg:
            msg = elem.text or \
                  elem.get_attribute('name') or \
                  elem.get_attribute('resourceId') or \
                  elem.tag_name

            msg = 'About to click by location...  element info = %s' % msg

        # an array of tuples
        # self.driver.tap([(x, y)])
        self.tap(x=x, y=y, msg=msg)

    def accept_start_popup(self):
        # Allow CBS to see your location?
        if "5 6.0" in self.testdroid_device:
            self.click_safe(name='Allow', timeout=300)
        if 'HTC' in self.testdroid_device:
            name = 'ACCEPT'
            self.click_safe(name=name, timeout=480)
            sleep(3)
            self.click_safe(id='android:id/button1', timeout=5)
        elif 'Nexus' in self.testdroid_device:
            name = 'ACCEPT'
            self.click_safe(name=name, timeout=300)
        else:
            if not self.click_safe(name='ACCEPT', timeout=300):
                self.click_safe(name='Accept', timeout=10)

    def click_safe(self, **kwargs):
        """
        Waits for element to exist before trying to click.  Default wait = current implicit wait
        Does NOT throw an error if element does not exist.
        If true - click and return the element.  If false - return False

        example:
        self.click_safe(id=self.com_cbs_app + ':id/showcase_button', timeout=10)
        """
        element_or_false = self.exists(**kwargs)

        if element_or_false:
            msg = element_or_false.text or \
                  element_or_false.get_attribute('name') or \
                  element_or_false.get_attribute('content-desc') or \
                  element_or_false.get_attribute('resource-id') or \
                  element_or_false.tag_name

            self.event.click('In click_safe(), about to click.  element info = %s' % msg)
            element_or_false.click()
            return element_or_false
        else:
            return False

    def tap(self, x, y, msg=""):
        """
        Converts relative args such as click(.5, .5)
        to actual numbers such as (515, 840) based on current screen size.
        Apparently some versions of appium don't handle this correctly. Surprising.
        """
        if x < 1 or y < 1:
            s = self.driver.get_window_size()
            width = s['width']
            height = s['height']

            if x < 1:
                x = x * width
            if y < 1:
                y = y * height

        # logging
        self.event.click('clicking: %s (%s, %s)' % (msg, int(x), int(y)))
        self.driver.tap([(x, y)])

    def generate_random_string(self, length=8):
        """
        returns random alpha-numeric string
        """
        return str(''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length)))

    def _hide_keyboard(self):
        for x in range(0, 3):
            try:
                self.driver.hide_keyboard()
                sleep(1)
            except:
                pass
        sleep(2)

    def is_keyboard_displayed(self):
        """
        WARNING: Has the side-effect of hiding the keyboard if it's displayed

        Wrapper for driver.hide_keyboard()
        Returns True or False
        """
        try:
            self.driver.hide_keyboard()
            return True
        except WebDriverException:
            return False

    def click_on_first_video(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_name('Free Episodes')
            self._short_swipe_down(duration=3000)
        except:
            self.driver.implicitly_wait(60)
            pass
        if self.exists(name='paid', timeout=5):
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
        else:
            if self.exists(name='Recently Watched', timeout=5):
                self.swipe_element_to_top_of_screen(elem=self.get_element(name='Recently Watched', timeout=10), endy=150)
                prime_container = self._find_element(
                xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Primetime')]]")
            for _ in range(0, 40):
                self._short_swipe_left(prime_container, 500)
            count = 0
            while count < 70:
                self._short_swipe_left(prime_container, 1000)
                if self.exists(name='paid', timeout=5):
                    list_episodes = self.driver.find_elements_by_name('paid')
                    self.click(element=list_episodes[0])
                    break
                else:
                    count += 1

    def click_any_free_video(self):
        if self.exists(xpath="//android.widget.TextView[@text='My CBS']", timeout=5):
            self.swipe_element_to_top_of_screen(elem=self.get_element(xpath="//android.widget.TextView[@text='My CBS']"), endy=100, startx=0)
        if self.exists(name='free', timeout=10):
            list_episodes = self.driver.find_elements_by_name('free')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()

    def click_play_from_beginning(self):
        self.click_safe(name='Play From Beginning', timeout=10)

    def select_first_show_option(self):
        self.click(id=(self.com_cbs_app + ':id/showImage'), data='First show icon')

    def click_any_video(self):
        self.safe_screenshot()
        episode = self.get_elements(id=self.com_cbs_app + ":id/videoImage")
        self.click(element=episode[0])
        # self.click_by_location(list_episodes[0], side='middle')
        self.click_play_from_beginning()

    def click_any_aa_video(self):
        if self.exists(name='paid', timeout=10):
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()
        else:
            self._short_swipe_down(duration=3000)
            self._short_swipe_down(duration=3000)
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()

    def back(self):
        self.log_info("Press Back button")
        self.driver.back()

    def go_back(self):
        # <- icon lost its id on the live tv page :(
        if self.exists(name='Live TV', timeout=3):
            self.hw_back()
        else:
            self.click_safe(name='Navigate up')

    def verify_exists_element_video_page(self, poll_every=5, **kwargs):
        count = 0
        result = False
        while count < kwargs['timeout']:
            if self.exists(element=self.get_element(**kwargs)):
                result = True
                #self.unpause_video()
                break
            else:
                sleep(poll_every)
                #self.pause_video()
                count += poll_every

        self.assertTrueWithScreenShot(result, screenshot=True, msg="Should see element on video page")

    def back_while_open_drawer_is_visible(self):
        counter = 0
        while not self.exists(element=self.get_element(timeout=10, name='Open navigation drawer')):
            self.back()
            counter += 1
            if counter > 10:
                break

    def back_while_navigate_up_is_visible(self):
        counter = 0
        while not self.exists(element=self.get_element(timeout=10, name='Navigate up')):
            self.back()
            counter += 1
            if counter > 10:
                break

    def back_to_home_page(self):
        counter = 0
        self.driver.implicitly_wait(20)
        while counter < 10:
            try:
                self.driver.find_element_by_id(self.com_cbs_app + ":id/homeMarqueeContainer")
                break
            except:
                self.driver.back()
                counter += 1
        self.driver.implicitly_wait(self.default_implicit_wait)

    def back_while_search_icon_is_visible(self):
        counter = 0
        self.driver.implicitly_wait(20)
        while counter < 10:
            try:
                self.driver.find_element_by_id(self.com_cbs_app + ":id/action_search")
                break
            except:
                self.driver.back()
                counter += 1
        self.driver.implicitly_wait(self.default_implicit_wait)

    def back_while_page_is_visible(self, page_title):
        counter = 0
        self.driver.implicitly_wait(20)
        while counter < 10:
            try:
                self.driver.find_element_by_xpath(
                    "//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@text='" + page_title + "']")
                break
            except:
                self.driver.back()
                counter += 1
        self.driver.implicitly_wait(self.default_implicit_wait)

    def exists(self, **kwargs):
        """
        Finds element by name or xpath
        advanced:
            call using an element:
            my_layout = self.driver.find_element_by_class_name('android.widget.LinearLayout')
            self.exists(name='Submit', driver=my_layout)
        """

        if kwargs.has_key('timeout'):
            self.driver.implicitly_wait(kwargs['timeout'])
        else:
            self.driver.implicitly_wait(20)
        if kwargs.has_key('driver'):
            d = kwargs['driver']
        else:
            d = self.driver

        if kwargs.has_key('element'):
            try:
                return kwargs['element']
            except:
                return False
        else:
            try:
                if kwargs.has_key('name'):
                    try:
                        e = d.find_element_by_name(kwargs['name'])
                    except:
                        e = d.find_element_by_xpath('//*[contains(@text,"%s")]' % kwargs['name'])
                elif kwargs.has_key('class_name'):
                    e = d.find_element_by_class_name(kwargs['class_name'])
                elif kwargs.has_key('id'):
                    e = d.find_element_by_id(kwargs['id'])
                elif kwargs.has_key('xpath'):
                    e = d.find_element_by_xpath(kwargs['xpath'])
                else:
                    raise RuntimeError("exists() called with incorrect param. kwargs = %s" % kwargs)

                return e
            except NoSuchElementException:
                return False
            finally:
                self.driver.implicitly_wait(self.default_implicit_wait)

    def not_exists(self, **kwargs):
        """
        Waits until element does not exist.  Waits up to <implicit_wait> seconds.
        Optional parameter: timeout=3 if you only want to wait 3 seconds.  Default=30
        Return: True or False
        """
        if 'timeout' in kwargs:
            timeout = (kwargs['timeout'])
        else:
            timeout = 30

        start_time = time()

        kwargs['timeout'] = 0  # we want exists to return immediately
        while True:
            elem = self.exists(**kwargs)
            if not elem:
                return True

            if time() - start_time > timeout:
                return False

    def exists_one_of(self, *args):
        """
        Pass in a list of elements to search for.  This is very helpful for differences across devices such
        as Submit vs. SUBMIT (or in system settings menus such as Wi-Fi vs Wi Fi).  Also very useful for multi-
        language support.  This is much more efficient than searching for 130s for elementA, then trying elementB
        default timeout is default_implicit_wait

        examples:
        self.exists_one_of('name', 'SUBMIT', 'name', 'Submit')
        self.exists_one_of('name', 'Logout', 'id', self.com_cbs_app + ':id/signOutButton', 'timeout', 10)
        """

        if len(args) % 2 != 0:
            raise RuntimeError('Number of args passed to exists_one_of() must be an even number')

        # will be overwritten later if they passed in a value for timeout
        timeout = self.default_implicit_wait

        # turn list ['a', 'b', 'c', 'd']
        # into dict {'a':'b', 'c':'d'}
        search_list = []
        while args:
            if args[0] in ['name', 'class_name', 'id', 'xpath']:
                d = {args[0]: args[1]}
                search_list.append(d)
            elif args[0] == 'timeout':
                timeout = args[1]
            args = args[2:]

        start_time = time()

        while True:
            # this inner for loop will ensure that we search for all elements at least once.
            for i in range(len(search_list)):
                new_args = {'timeout': 0}
                new_args.update(search_list[i])  # 'timeout'=0 we want exists to return immediately

                elem = self.exists(**new_args)
                if elem:
                    return elem

            if time() - start_time > timeout:
                return False

    def find_on_page(self, find_by, find_key, max_swipes=10, x=.5):
        """
        Scrolls down the page looking for an element.  Call the method like this:
        self.find_on_page('name', 'Settings')
        self.find_on_page('id', self.com_cbs_app + ':id/seasonEpisode')
        """
        for i in range(max_swipes):
            if find_by == 'name':
                e = self.get_element(xpath='//*[contains(@text,"' + find_key + '")]', timeout=10)
            else:
                e = self.get_element(xpath='//*[contains(@resource-id,"' + find_key + '")]', timeout=10)

            if e is False:
                self.swipe(x, .5, x, 10, 1500)
            else:
                return e

        return False
        # raise NoSuchElementException("find_on_page failed looking for '%s'" % elem_id)

    def find_one_of(self, *args):
        """
        Uses exists_one_of() and just throws an error if cannot find any of the elements passed in
        See exists_one_of()

        examples:
        self.find_one_of('name', 'SUBMIT', 'name', 'Submit')
        self.find_one_of('name', 'Logout', 'id', self.com_cbs_app + ':id/signOutButton', 'timeout', 10)
        """

        elem = self.exists_one_of(*args)
        if elem:
            return elem
        else:
            raise NoSuchElementException("Could not find any of %s" % str(args))

    def verify_exists(self, **kwargs):
        screenshot = False
        if kwargs.has_key('screenshot') and kwargs['screenshot']:
            screenshot = True

        if kwargs.has_key('name'):
            selector = kwargs['name']
        elif kwargs.has_key('class_name'):
            selector = kwargs['class_name']
        elif kwargs.has_key('id'):
            selector = kwargs['id']
        elif kwargs.has_key('xpath'):
            selector = kwargs['xpath']
        else:
            selector = ''

        self.assertTrueWithScreenShot(self.exists(**kwargs), screenshot=screenshot,
                                      msg="Should see element with text or selector: '%s'" % selector)

    def verify_not_exists(self, **kwargs):
        screenshot = False
        if kwargs.has_key('screenshot') and kwargs['screenshot']:
            screenshot = True

        if kwargs.has_key('name'):
            selector = kwargs['name']
        elif kwargs.has_key('class_name'):
            selector = kwargs['class_name']
        elif kwargs.has_key('id'):
            selector = kwargs['id']
        elif kwargs.has_key('xpath'):
            selector = kwargs['xpath']
        else:
            selector = ''

        self.assertTrueWithScreenShot(not self.exists(**kwargs), screenshot=screenshot,
                                      msg="Should NOT see element with text or selector: '%s'" % selector)

    def click_try_1_week_month_free(self):
        self.click(xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                         "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")
        self._hide_keyboard()

    def validation_upsell_page(self):
        self.verify_exists(id=self.com_cbs_app + ':id/allAccessLogo', screenshot=True)
        if self.user_type in [self.anonymous, self.registered]:
            self.verify_exists(
                xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
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
        else:
            if self.user_type == self.ex_subscriber:
                self.verify_exists(
                    xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
                self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
                self.verify_exists(xpath="//*[contains(@text,'Only $5.99/month')]")
                self.verify_exists(name='SELECT')
                self.verify_not_exists(xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                             "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]", timeout=10)
                self.verify_not_exists(name='GET STARTED', timeout=10)

    def wait_until_element_is_visible(self, element_css=None, element_name=None, element_id=None, timeout=20):

        count = 0
        while count <= 10:
            self.driver.implicitly_wait(timeout)
            try:
                if element_css:
                    self.driver.find_elements_by_class_name(element_css)
                    break
                if element_name:
                    self.driver.find_element_by_name(element_name)
                    break
                if element_id:
                    self.driver.find_element_by_id(element_id)
                    break
            except:
                pass
            count += 1

    def _login(self, username, password):

        email_field = self.click(id=self.com_cbs_app + ':id/edtEmail')
        self.send_keys(element=email_field, data=username, id=self.com_cbs_app + ':id/edtEmail')
        self._hide_keyboard()
        self.event.screenshot(self.screenshot())

        password_field = self.click(id=self.com_cbs_app + ':id/edtPassword')
        self.send_keys(element=password_field, data=password, id=self.com_cbs_app + ':id/edtPassword')
        self._hide_keyboard()
        self.event.screenshot(self.screenshot())
        self.click(id=self.com_cbs_app + ':id/btnSignIn')

        self.complete_registration()

    def complete_registration(self):
        # Complete registration if required

        try:
            sleep(5)
            self.click(id=self.com_cbs_app + ':id/terms_accept_checkBox')
            self.event.screenshot(self.screenshot())
            self.click(name='SUBMIT')
        except Exception:
            self.event._log_info(self.event._event_data('complete registration not needed'))
        self.event.screenshot(self.screenshot())
        self.driver.implicitly_wait(30)

    def logout(self):
        self.goto_settings()
        if self.phone:
            origin = self.driver.find_element_by_name('Video Services')
            destination = self.driver.find_element_by_name('Send Feedback')
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
        self.click(name='Sign Out', data='Sign Out 1')
        self.click(id=self.com_cbs_app + ':id/signOutButton', data="Sign out 2")
        if "LGE Nexus 5X" == self.testdroid_device:
            self.event._log_info(self.event._event_data('Sign out 2'))
            self.driver.tap([(400, 660)])
        self.event.screenshot(self.screenshot())
        self.navigate_up()
        self.goto_home()

    def click_already_have_account_sign_in(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.driver.find_element_by_name('Already have an account? Sign In')
        self.click_by_location(elem, side='right')

    #### LIVE TV and NIELSEN
    def goto_nielsen_info_page(self):
        self.goto_settings()
        sleep(1)
        if self.phone:
            self.swipe_down_if_element_is_not_visible(name='Nielsen Info & Your Choices')
        self.click(name='Nielsen Info & Your Choices')
        sleep(15)  # waiting for page to load

    def go_to_debug_page(self):
        self.goto_settings()
        if self.phone:
            origin = self.driver.find_element_by_name('Nielsen Info & Your Choices')
            destination = self.driver.find_element_by_name('Send Feedback')
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
            self.click(name='Debug')
            self.screenshot()
        else:
            self.click(name='Debug')

    def choose_location(self, city, swipe_up=False):
        self.go_to_debug_page()

        window_size_y = self.driver.get_window_size()["height"]

        self.click(name='Location Set')

        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_name(name=city)
            self.click(name=city, screenshot=True)
        except:
            if swipe_up:
                for i in range(3):
                    if self.phone:
                        self.driver.swipe(100, 600, 100, window_size_y - 250)
                    elif self.tablet:
                        self.driver.swipe(500, 600, 500, window_size_y - 400)  # Nexus 7
            else:
                if self.phone:
                    origin = self.driver.find_element_by_name('Philadelphia')
                    destination = self.driver.find_element_by_name('Denver KCNC')
                    self.driver.drag_and_drop(origin, destination)
                    self.event.screenshot(self.screenshot())
                    origin = self.driver.find_element_by_name('College Station, TX KBTX')
                    destination = self.driver.find_element_by_name('Boston')
                    self.driver.drag_and_drop(origin, destination)
                    self.event.screenshot(self.screenshot())
                elif self.tablet:
                    for i in range(4):
                        self.driver.swipe(500, window_size_y - 400, 500, 600)
            self.click(name=city, screenshot=True)

            self.driver.implicitly_wait(30)
        self.navigate_up()

    def select_verify_now(self):
        self.swipe_down_and_verify_if_exists(id_element=self.com_cbs_app + ':id/btnVerifyNow')
        self.click(id=self.com_cbs_app + ':id/btnVerifyNow', data='Clicking verify now')
        self.click_allow_popup()

    def mvpd_logout(self):
        self.goto_settings()
        sleep(5)
        self.safe_screenshot()
        try:
            self.click(xpath='//*[contains(@text,"Disconnect from Optimum")]', data='Disconnect From Optimum')
            self.safe_screenshot()
            self.click(id=self.com_cbs_app + ':id/btnMvpdLogoutSettings')
            sleep(4)
            self.click(id='android:id/button1')
            sleep(3)
        except:
            self.event._log_info(self.event._event_data('Optimum was not connected'))
        self.navigate_up()
        if "KFTBWI" in self.testdroid_device:
            try:
                self.navigate_up()
            except:
                pass

    def go_to_providers_page(self):
        self.goto_live_tv()
        if self.phone:
            self.swipe_down_if_element_is_not_visible('Verify Now', short_swipe=True)
        self.select_verify_now()
        self.click_allow_popup()

    def select_optimum_from_provider_page(self):
        self.driver.find_element_by_id(id_=self.com_cbs_app + ':id/ivProviderLogo')
        self.click(id=self.com_cbs_app + ':id/ivProviderLogo')
        self.click_allow_popup()

    def optimun_sign_in(self, user, password):
        sleep(15)
        if self.testdroid_device == 'LGE Nexus 5 6.0':
            sleep(10)
            id_field = self.driver.find_element_by_xpath(xpath="//*[@content-desc='Optimum ID']").click()
            self.send_keys(element=id_field, data=user, xpath="//*[@content-desc='Optimum ID']")
            self._hide_keyboard()
            self.screenshot()

            password_field = self.driver.find_element_by_xpath(xpath="//*[@resource-id='IDToken2']").click()
            self.send_keys(element=password_field, data=password, xpath="//*[@resource-id='IDToken2']")
            self._hide_keyboard()
            self.screenshot()

            self.driver.tap([(200, 1200)])
            self.screenshot()

        else:
            count = 0
            while count <= 5:
                try:
                    self.driver.find_elements_by_class_name('android.widget.EditText')
                    break
                except:
                    count += 1

            if self.testdroid_device == 'LGE Nexus 5':
                self.driver.tap([(200, 830)])
                self.screenshot()
            if self.testdroid_device == 'asus Nexus 7':
                self.driver.tap([(600, 600)])
                self.screenshot()
            if self.testdroid_device == 'samsung SM-T330NU':
                self.driver.tap([(400, 400)])
                self.screenshot()
            fields = self.driver.find_elements_by_class_name('android.widget.EditText')
            email_field = fields[0]
            password_field = fields[1]
            # start from the bottom up
            self.click(email_field)
            self.screenshot()
            self.send_keys(data=user, element=email_field, class_name='android.widget.EditText'[0])
            self.screenshot()
            self._hide_keyboard()
            self.send_keys(data=password, element=password_field, class_name='android.widget.EditText'[1])
            self.screenshot()
            self.driver.back()
            self.event.screenshot(self.screenshot())
            self.driver.press_keycode(66)  # Enter
            sleep(3)
            self.event.screenshot(self.screenshot())

    def log_info(self, info):
        self.event._log_info(self.event._event_data(info))

    def click_take_the_tour(self):
        self.click(id=self.com_cbs_app + ':id/takeTheTourTextView', screenshot=True)

    def click_episode_indicator(self):
        self.click(id=self.com_cbs_app + ':id/allAccessEpisodesContainer')

    def swipe_list_years(self, element):
        loc = element.location
        size = element.size

        startx = loc['x'] + size['width'] / 2
        endx = startx
        starty = loc['y'] + 20
        endy = loc['y'] + size['height']
        duration = 800

        self.swipe(startx, starty, endx, endy, duration)
        sleep(1)

    ####################################################################################
    # CLICK WRAPPERS

    def click_close(self):
        """
        Mainly for the episode info page that looks like a popup.  It appears when you click the (i) icon for an episode
        This page acts weird.  Sometimes page_source() hangs and fails the test, so we click by location.
        """
        e = self.find_on_page('name', 'Close')
        self.click_by_location(e, 'Close')

        sleep(5)
        self.click_safe(name='Close', timeout=5)

    def click_facebook_icon(self):
        self.click(id=self.com_cbs_app + ':id/imgFacebook')
        sleep(5)

    def click_twitter_icon(self):
        self.click(id=self.com_cbs_app + ':id/imgTwitter')
        sleep(5)

    def click_gplus_icon(self):
        self.click(id=self.com_cbs_app + ':id/imgGoogle')
        sleep(5)

    def click_more(self):
        # ellipse in upper-right corner some screens
        e = self.find_one_of('id', 'More options', 'id', 'More Options')
        e.click()

    def click_favorite_icon(self):
        self.click(id=self.com_cbs_app + ':id/mycbsButton')

    def click_episode_information(self):
        """
        on the show page, where you see a list of episodes,
        this clicks the (i) next to an episode
        """
        self.click(id=self.com_cbs_app + ':id/imgInfo')

    def click_watch_episode(self):
        """
        On the episode info page - the page you see by tapping the (i) icon
        Page acts weird, page_source() causes hanging and test failure, so we'll use tap_by_locatin()
        """
        e = self._find_element(name='Watch Episode')
        self.click_by_location(e, 'Watch Episode')

        # # The problem is this might bring up a "Resume Watching" popup but if we keep tapping down the screen it disappears.
        # max_y = self.driver.get_window_size()['height']
        # y = max_y / 4
        # y_increment = (max_y - y) / 25
        #
        # try:
        #     while y < max_y:
        #         self.tap(.5, y)
        #         y += y_increment
        # except WebDriverException:
        #     # the screen turned landscape and we tapped out of bounds
        #     pass

    def click_upgrade(self):
        self.click(xpath="//android.widget.Button[@text='Upgrade']")

    def click_upgrade_in_menu(self):
        es = self.driver.find_elements_by_id(self.com_cbs_app + ':id/userStatusTextView')
        for e in es:
            if e.text == 'Upgrade':
                e.click()
                return

        raise RuntimeError('Could not find "Upgrade" in side menu')

    def click_upgrade_lc(self):
        bs = self.driver.find_elements_by_id(self.com_cbs_app + ':id/button')

        self.event.click('Upgrade Limited Comm button')

        for b in bs:
            if "FREE" in b.text:
                b.click()
                return

        raise RuntimeError('Could not find "FREE..." button')

    def click_upgrade_cf(self):
        bs = self.driver.find_elements_by_id(self.com_cbs_app + ':id/button')

        self.event.click('Upgrade Comm Free button')

        for b in bs:
            if "GET" in b.text:
                b.click()
                return

        raise RuntimeError('Could not find "GET..." button')

    def click_select_lc(self):
        bs = self.driver.find_elements_by_name('SELECT')
        b0 = bs[0]
        b1 = bs[1]

        self.event.click('Select Limited Comm button')

        # click the button on the left
        if b0.location['x'] < b1.location['x']:
            b0.click()
        else:
            b1.click()

    def click_select_cf(self):
        bs = self.driver.find_elements_by_name('SELECT')
        b0 = bs[0]
        b1 = bs[1]

        self.event.click('Select Comm Free button')

        # click the button on the right
        if b0.location['x'] > b1.location['x']:
            b0.click()
        else:
            b1.click()

    def click_subscribe_in_menu(self):
        self.click(element=self.get_element(id=self.com_cbs_app + ':id/userStatusTextView'))
        # for e in es:
        #     if e.text == 'Subscribe':
        #         e.click()
        #         return
        #
        # raise RuntimeError('Could not find "Subscribe" in side menu')

    def click_get_started(self):
        self.click(xpath="//android.widget.Button[@text='Get Started']")

    def click_submit(self):
        self.click(name='SUBMIT')

    def click_price(self):
        # on Google billing screen, clicks the down arrow to show full text of billing agreement
        self.click(id='com.android.vending:id/item_price')

    def click_subscription(self):
        # On settings screen
        self.click(name='Manage Account')

    def click_subscribe(self):
        # On settings screen
        self.click(name='Subscribe')

        ####################################################################################

    # REGISTRATION

    # def enter_registration_form_part_01(self):
    #     ##### PART A: first/last/email/pwd #####
    #
    #     self.fn_str = self.generate_random_string()
    #     self.ln_str = self.generate_random_string()
    #     email_str = "TestA%s@gmail.com" % self.generate_random_string()
    #
    #     first_name = self._find_element(id=self.com_cbs_app + ':id/edtFirstName')
    #     self.send_keys(data=self.fn_str, element=first_name)
    #     self._hide_keyboard()
    #
    #     # while not self._verify_sent_text(first_name, self.fn_str):
    #     #     self.send_keys(data=self.fn_str + "\n", element=first_name)
    #
    #     last_name = self._find_element(id=self.com_cbs_app + ':id/edtLastName')
    #     self.send_keys(data=self.ln_str, element=last_name)
    #     self._hide_keyboard()
    #
    #     # while not self._verify_sent_text(last_name, self.ln_str):
    #     #     self.send_keys(data=self.ln_str + "\n", element=last_name)
    #
    #     email = self._find_element(id=self.com_cbs_app + ':id/edtEmail')
    #     self.send_keys(data=email_str, element=email, screenshot=True)
    #     self._hide_keyboard()
    #
    #     # while not self._verify_sent_text(email, email_str):
    #     #     self.send_keys(data=email_str + "\n", element=email)
    #
    #     email_confirm = self._find_element(id=self.com_cbs_app + ':id/edtConfirmEmail')
    #     self.send_keys(data=email_str, element=email_confirm, screenshot=True)
    #     self._hide_keyboard()
    #
    #     # while not self._verify_sent_text(email_confirm, email_str):
    #     #     self.send_keys(data=email_str + "\n", element=email_confirm)
    #
    #     if self.phone:
    #         self.swipe_element_to_top_of_screen(email_confirm, endy=400)
    #
    #     pwd = self._find_element(id=self.com_cbs_app + ':id/edtPassword')
    #     self.send_keys('abcdef', pwd)
    #     self._hide_keyboard()
    #
    #     pwd_confirm = self._find_element(id=self.com_cbs_app + ':id/editConfirmPassword')
    #     self.send_keys('abcdef', pwd_confirm, screenshot=True)
    #     self._hide_keyboard()
    #
    #     if self.phone:
    #         self.swipe_element_to_top_of_screen(pwd_confirm, endy=300)
    #
    # def enter_registration_form_part_02(self):
    #     self.click(id=self.com_cbs_app + ':id/edtBirthdate', screenshot=True)
    #
    #     if self.exists(id='android:id/date_picker_header_year', timeout=10):
    #         self.click(id='android:id/date_picker_header_year', data='Click on current year')
    #         list_years = self._find_element(id='android:id/animator')
    #
    #         for _ in range(5):
    #             self.swipe_list_years(list_years)
    #
    #         years = self.driver.find_elements_by_class_name("android.widget.TextView")
    #
    #         self.click(element=years[5], data='Choose year from the list')
    #         self.click(name='OK')
    #     elif self.exists(id='android:id/date_picker_year', timeout=10):
    #         self.click(id='android:id/date_picker_year', data='Click on current year')
    #         list_years = self._find_element(id='android:id/animator')
    #
    #         for _ in range(5):
    #             self.swipe_list_years(list_years)
    #
    #         years = self.driver.find_elements_by_class_name("android.widget.TextView")
    #
    #         self.click(element=years[5], data='Choose year from the list')
    #         self.click(name='OK')
    #     else:
    #         pickers = self.driver.find_elements_by_class_name('android.widget.NumberPicker')
    #
    #         year_picker = pickers[2]
    #
    #         year_but = year_picker.find_element_by_class_name('android.widget.Button')
    #
    #         # swipe a bunch of times to make the user 18 years old
    #         # do in two steps to try to speed it up some
    #         for i in range(10):
    #             self.swipe_datepicker_down(year_but)
    #
    #         for i in range(10):
    #             self.swipe_datepicker_down(year_but)
    #             year_picker = self.driver.find_elements_by_class_name('android.widget.NumberPicker')[2]
    #             current_year = year_picker.find_element_by_class_name('android.widget.Button').text
    #
    #             if current_year < '1996':
    #                 break
    #
    #         self.driver.implicitly_wait(10)
    #         try:
    #             elem = self.driver.find_element_by_name('Set')
    #         except:
    #             elem = self.driver.find_element_by_name('Done')
    #
    #         self.click(element=elem, data='Choose the date')
    #
    #         self.driver.implicitly_wait(self.default_implicit_wait)
    #
    #     self.click(name='Male')
    #     try:
    #         self.driver.find_element_by_name('Alaska')
    #         self.click(name='Alaska')
    #     except:
    #         self.click(id=self.com_cbs_app + ':id/spnState')
    #         self.click(name='Alaska')
    #
    # def enter_registration_form_part_03(self):
    #     zip_id = self.com_cbs_app + ":id/edtZipCode"
    #
    #     zip = self.driver.find_element_by_id(zip_id)
    #
    #     zip_text = zip.text
    #
    #     self.send_keys('78704', zip)
    #     sleep(2)
    #
    #     zip = self.driver.find_element_by_id(zip_id)
    #
    #     self.verify_not_equal(zip_text, zip.text, screenshot=True)
    #
    #     if self.phone:
    #         self.swipe_element_to_top_of_screen(zip)
    #
    #     check_box = self._find_element(class_name='android.widget.CheckBox')
    #
    #     self.click(element=check_box, data='Accept Terms and Conditions', screenshot=True)
    #
    # def submit_registration_form(self):
    #     """
    #     Clicks Submit button
    #     Makes sure we signed in correctly and get to homepage
    #     Sends email to a couple people with newly created account
    #     """
    #     self._hide_keyboard()
    #
    #     self.click(id=self.com_cbs_app + ':id/btnSignUp')
    #
    #     # self.send_created_account_email()

    ####################################################################################
    # GET WRAPPERS

    def get_show_title_from_info_page(self):
        """
        Info page is the popup you see after clicking (i) on an episode thumbnail
        This will get the show title
        """
        return self._find_element(id=self.com_cbs_app + ':id/showName').text

    ####################################################################################
    # SWIPE / TAP / CLICK / SEND_KEYS
    def swipe_down_if_element_is_not_visible(self, name=None, id_element=None, class_name=None, long_swipe=False,
                                             short_swipe=False):
        """
        function that search for element, if element is not found swipe the page until element is found on screen
        """
        self.driver.implicitly_wait(0)

        # Gets mobile screen size
        window_size_y = self.driver.get_window_size()["height"]

        element = None
        count = 0
        while element is None and count <= 10:
            try:
                if name:
                    element = self.driver.find_element_by_name(name=name)
                elif id_element:
                    element = self.driver.find_element_by_id(id_=id_element)
                elif class_name:
                    element = self.driver.find_element_by_class_name(class_name=class_name)
            except:
                if self.phone:
                    if long_swipe:
                        self.driver.swipe(35, window_size_y - 500, 35, 200)
                    elif short_swipe:
                        self.driver.swipe(35, window_size_y - 600, 35, 700)
                    else:
                        self.driver.swipe(35, window_size_y - 600, 35, 500)
                else:
                    if long_swipe:
                        self.driver.swipe(500, window_size_y - 600, 500, 200)
                    elif short_swipe:
                        self.driver.swipe(500, window_size_y - 600, 500, 550)
                    else:
                        self.driver.swipe(500, window_size_y - 400, 500, 600)
                count += 1

        self.driver.implicitly_wait(30)

    def swipe_up_until_element_is_visible(self, name=None, id_element=None, short_swipe=False):
        """
        function that search for element, if element is not found swipe the page until element is found on screen
        """
        self.driver.implicitly_wait(0)

        # Gets mobile screen size
        window_size_y = self.driver.get_window_size()["height"]

        element = None
        count = 0
        while element is None and count <= 10:
            try:
                if name:
                    element = self.driver.find_element_by_name(name=name)
                elif id_element:
                    element = self.driver.find_element_by_id(id_=id_element)
            except NoSuchElementException:
                if short_swipe:
                    self.driver.swipe(35, 600, 35, window_size_y - 400)
                else:
                    self.driver.swipe(35, 400, 35, window_size_y - 500)
                count += 1
        self.driver.implicitly_wait(30)
        self.screenshot()

    def swipe(self, startx, starty, endx, endy, swipe_time):
        """
        Takes normal args or relative args such as swipe(.5, .5, .5, .2, 1000)
        """
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

        # try a couple times.  sometimes swipe fails for no clear reason
        try:
            self.driver.swipe(startx, starty, endx, endy, swipe_time)
        except WebDriverException:
            sleep(4)
            self.driver.swipe(startx, starty, endx, endy, swipe_time)

    def swipe_down_and_verify_if_exists(self, name=None, id_element=None, class_name=None, screenshot=False):

        if name:
            self.swipe_down_if_element_is_not_visible(name=name, short_swipe=True)
            self.verify_exists(name=name)
        elif id_element:
            self.swipe_down_if_element_is_not_visible(id_element=id_element, short_swipe=True)
            self.verify_exists(id=id_element)
        elif class_name:
            self.swipe_down_if_element_is_not_visible(class_name=class_name, short_swipe=True)
            self.verify_exists(class_name=class_name)

        if screenshot:
            self.event.screenshot(self.screenshot())
        self.driver.implicitly_wait(30)

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

        try:
            self.driver.swipe(x, start_y, x, end_y, duration)
        except:
            self.event.screenshot(self.screenshot())
        sleep(1)

    def _short_swipe_left(self, element, duration):
        location = element.location
        size = element.size

        start_x = location['x'] + size['width'] - 100
        end_x = 20
        y = location['y'] + size['height'] / 2

        try:
            self.driver.swipe(start_x, y, end_x, y, duration)
        except:
            pass
        sleep(1)

    def swipe_element_to_top_of_screen(self, elem, endy=None, startx=-20):
        """
        Uses element.location
        Default is to swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        loc = elem.location
        startx = loc['x'] + startx
        starty = loc['y']

        # in case it's behind the banner ad at the bottom, swipe up a little
        window_height = self.driver.get_window_size()['height']
        if starty > .8 * window_height:
            self.swipe(.5, .5, .5, .3, 1500)
            starty = starty - window_height * .2
            sleep(1)

        if not endy:
            if self.phone:
                endy = 70
            else:
                endy = 180

        self.swipe(startx, starty, startx, endy, 1500)

    def swipe_element_to_bottom_of_screen(self, elem, endy=None, startx=-20):
        """
        Uses element.location
        Default is to swipe NEXT TO the element, to the bottom of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        startx = elem.location['x'] + startx
        starty = elem.location['y']

        size = self.driver.get_window_size()
        height = size['height']

        if not endy:
            if self.phone:
                endy = height - 70
            else:
                endy = height - 180

        self.swipe(startx, starty, startx, endy, 1500)

    def swipe_datepicker_down(self, element, duration=800):
        """
        Swipes the element a little to change it to a random value
        Used just to see that the value is different than before
        """
        loc = element.location
        size = element.size

        startx = loc['x'] + size['width'] / 2
        endx = startx
        starty = loc['y'] + size['height'] / 2
        endy = starty + 200

        if endy < 5:
            endy = 5
            duration -= 200

        self.swipe(startx, starty, endx, endy, duration)
        sleep(1)

    ####################################################################################
    # SHOWS

    def dummy_search(self):
        """
        a lot of times the initial search after install fails.  let's get that one out of the way
        """
        self.click_search_icon()
        self.enter_search_text('48')
        sleep(5)
        self.click_search_back()

    def enter_search_text(self, what_to_search_for):
        """
        Only sends what_to_search_for to the search text field
        If you really want to do a search, use search_for()
        """
        # hack
        if what_to_search_for.lower() == 'the late show with stephen colbert':
            what_to_search_for = 'Late Show with Stephen Colbert'

        self.not_exists(name='android.widget.ProgressBar')
        sleep(1)
        e = self._find_element(id=self.com_cbs_app + ':id/search_src_text')
        e.click()
        sleep(2)

        # try a few times.  Currently not working well: HTC 8x
        for i in range(4):
            sleep(2)
            self.tap_keys_on_keyboard(what_to_search_for[:1])
            sleep(10)
            self.tap_keys_on_keyboard(what_to_search_for[1:])
            if what_to_search_for in e.text:
                break
            else:
                self.event.screenshot(self.screenshot())
                e.clear()

        self.assertTrueWithScreenShot(what_to_search_for in e.text,
                                      screenshot=False,
                                      msg="Search edit text should == %s" % what_to_search_for)

        sleep(5)

    def search_for(self, what_to_search_for):
        """
        Clicks search icon and enters what_to_search_for
        Results should appear automatically
        """
        self.click_search_icon()
        self.enter_search_text(what_to_search_for)

    def click_first_search_result(self):
        # this is how we did it in 2.9
        self.tap(.25, .25, 'first search result')

    def collect_details_from_show_info_page(self):
        show_dict_found = {}
        show_dict_found['show_title'] = self._find_element(id=self.com_cbs_app + ':id/showName').text
        show_dict_found['episode_title'] = self._find_element(id=self.com_cbs_app + ':id/episodeName').text
        show_dict_found['air_date'] = self._find_element(id=self.com_cbs_app + ':id/airDate').text
        show_dict_found['season_episode'] = self._find_element(id=self.com_cbs_app + ':id/seasonEpisode').text

        return show_dict_found

    def find_show_on_home_page(self, show_dict):
        """
        First scrolls down looking for the show category (Primetime, etc.)
        Then scrolls to the side looking for the season / episode combination
        show_dict should look like
            {'show_title': 'CSI Miami',
            'show_category': 'Primetime'}

        Returns a dict that looks like:
            {'show_title': 'CSI Miami',
            'episode_title': 'Fun in the Sun',
            'air_date': '3/5/16',
            'season': '28',
            'episode': '3'}
        """
        show_category = show_dict['show_category']

        category_elem = self.find_on_page('name', show_category)
        self.assertTrueWithScreenShot(category_elem, screenshot=True, msg="Assert our category exists")
        y_orig = category_elem.location['y']

        self.swipe_element_to_top_of_screen(category_elem, endy=.25, startx=20)

        # For some stupid reason, it over-swipes sometimes.  Make sure it's still on the screen
        self.driver.page_source

        category_elem = self.exists(name=show_dict['show_category'], timeout=2)
        screen_height = self.driver.get_window_size()["height"]
        if not category_elem or category_elem.location['y'] < screen_height * .12:
            self.swipe(.5, .5, .5, .9, 1500)
        sleep(2)
        self.driver.page_source

        # find it again to be sure we get the right positioning
        category_elem = self._find_element(name=show_category)
        y = category_elem.location['y'] + category_elem.size['height'] + 50

        # swipe left to right to reset to the beginning of the list
        for i in range(2):
            self.swipe(.2, y, .9, y, 500)
            sleep(1)

        season_ep = 'S%s Ep%s' % (show_dict['season_number'], show_dict['episode_number'])

        # We have to try multiple times just in case we see a "S3 Ep4" (for example) from a different show.
        # Should be extremely rare.
        for i in range(3):
            season_ep_elem = self.find_on_page_horizontal('name', season_ep, swipe_y=y, max_swipes=20)
            title_elem = self.exists(name=show_dict['show_title'], timeout=0)

            # The rare case that we see an elem with the right season and episode numbers, but it's the wrong show.
            # Swipe it off the screen and try again...
            if season_ep_elem and not title_elem:
                self.event.screenshot(self.screenshot())
                self.swipe(.8, y, .2, y, 1500)
                self.event.screenshot(self.screenshot())
            else:
                break

        self.assertTrueWithScreenShot(season_ep_elem, screenshot=True,
                                      msg="Assert our season/episode exists: %s" % season_ep)

        return season_ep_elem

    def find_episode_on_show_page(self, show_dict, exception_hack=False):
        """
        First scrolls down looking for the show category (Primetime, etc.)
        Then scrolls to the side looking for the episode
        show_dict should look like
            {'episode_title': 'Fun in the Sun',
            'season_episode': 'S28 Ep8''}

        Returns a dict that looks like:
            {'show_title': 'CSI Miami',
            'episode_title': 'Fun in the Sun',
            'air_date': '3/5/16',
            'season_episode': 'S28 Ep8''}
        """
        episode_title = show_dict['episode_title']

        if exception_hack == 'AFTER SHOW':
            # for Big Brother After Show, there is no season, it just says "After Show"
            season_name = 'AFTER SHOW'
        elif exception_hack == 'Specials':
            # for specials, there's only one episode, or only one row of episodes anyway
            show_elem = self._find_element(id=self.com_cbs_app + ":id/showName")
            return show_elem
        else:
            season_name = "Season " + str(show_dict['season_number'])

        season_elem = self.find_on_page('name', season_name)
        self.assertTrueWithScreenShot(season_elem, screenshot=True, msg="Assert our season exists: %s" % season_name)
        self.swipe_element_to_top_of_screen(season_elem, endy=.25, startx=20)

        # may help get the position correctly
        sleep(2)
        self.driver.page_source

        # find it again to be sure we get the right positioning
        season_elem = self._find_element(name=season_name)
        y = season_elem.location['y'] + season_elem.size['height'] + 50

        show_elem = self.find_on_page_horizontal('name', episode_title, swipe_y=y, max_swipes=20)
        self.assertTrueWithScreenShot(show_elem, screenshot=True, msg="Assert our show exists: %s" % episode_title)

        return show_elem

    ####################################################################################
    # FIND / EXISTS

    def find_on_page_horizontal(self, find_by, find_value, max_swipes=10, swipe_y=.5):
        """
        Scrolls to the right the page looking for an element.  Call the method like this:
        self.find_on_page('name', 'Settings')
        self.find_on_page('id', 'com.cbs.app:id/seasonEpisode')

        Used to search for a specific episode in a Category (or in a Season if on show page)
        """
        self.set_implicit_wait(0)

        for i in range(max_swipes):
            self.driver.page_source
            if find_by == 'name':
                elems = self.driver.find_elements_by_xpath('//*[contains(@text,"' + find_value + '")]')
            else:
                elems = self.driver.find_elements_by_xpath('//*[contains(@resource-id,"' + find_value + '")]')

            for elem in elems:
                # if the elem is below the Category marker.  This is necessary in case the episode appears in the
                # "Recently Watched" Category at the top.  We want to ignore recently watched videos.
                if elem.location['y'] > swipe_y:
                    # if it's way off to the side, swipe it into the middle of the screen
                    if elem.location['x'] > self.driver.get_window_size()["height"] * .5:
                        self.swipe(.5, swipe_y, .1, swipe_y, 1500)
                    self.set_implicit_wait()
                    return elem

            self.swipe(.7, swipe_y, 10, swipe_y, 1500)

        self.set_implicit_wait()
        return False
        # raise NoSuchElementException("find_on_page_horizontal failed looking for '%s'" % elem_id)

    def find_app_by_xpath_and_click(self, element_xpath):
        """
        From Android "Apps" view, find an app and launch it
        """
        # finds specific app in device apps page
        window_size_y = self.driver.get_window_size()["height"]
        window_size_x = self.driver.get_window_size()["width"]
        self.set_implicit_wait(5)

        # first reset to the far left...
        count = 0
        while count <= 5:
            self.swipe(.2, .5, .8, .5, 300)
            sleep(.5)
            count += 1

        # then start searching to the right
        count = 0
        while count <= 5:
            element = self.exists(xpath=element_xpath, timeout=4)
            if element:
                self.event.screenshot(self.screenshot())
                element.click()
                # loc = element.location
                # self.tap(loc['x'] + 70, loc['y'] + 70)
                break
            else:
                if self.testdroid_device == "HTC_M8x":
                    self.driver.swipe(window_size_x / 2, window_size_y - 300, window_size_x / 2, 300, 1000)
                else:
                    self.swipe(.8, .5, .2, .5, 300)
                count += 1
        self.set_implicit_wait()

        ####################################################################################
        # XML methods
        # These are for the special case where using normal find methods don't work - specifically for the
        # video player skin.  driver.page_source works, but driver.find_element_by_id() just hangs for some reason.
        # Typical use would be:
        #   root = self.get_page_source_xml(True)
        #   self.verify_exists_using_xml(find_by='resource-id', find_key='com.cbs.app:id/tvCurrentTime', screenshot=True)

    def get_page_source_xml(self):
        """
        Used for dealing with watching videos. See section header (XML Methods) for details.
        Returns root element of xml.  We always want the xml with the controls on screen, so
        this taps to bring up the controls if necessary, returns whichever xml has more information.
        Yes, this is a terrible way to do this, but there are so many variables that we do not know and have
        no control over that this simple way is the most reliable in all situations.
        """
        ps1 = self.driver.page_source

        # yeah, this is fairly hacky, but we need this method to return as quickly as possible
        try:
            self.get_page_source_xml_x_tap
        except AttributeError:
            s = self.driver.get_window_size()
            tap_x = int(s['width'] * .5)
            tap_y = int(s['height'] * .5)

            # we're expecting screen to be horizontal while watching a video
            if tap_x > tap_y:
                self.get_page_source_xml_x_tap = tap_x
                self.get_page_source_xml_y_tap = tap_y
            else:
                self.get_page_source_xml_x_tap = tap_y
                self.get_page_source_xml_y_tap = tap_x

        # use the base driver.tap() because we're going to be doing this A LOT and want to avoid clogging the logs
        self.driver.tap([(self.get_page_source_xml_x_tap, self.get_page_source_xml_y_tap)])
        sleep(.5)
        ps2 = self.driver.page_source

        if len(ps1) > len(ps2):
            return ElementTree.fromstring(ps1)
        else:
            return ElementTree.fromstring(ps2)

    def _exists_element_using_xml(self, root=False, find_by=None, find_key=None, class_name='*'):
        """
        usually you'll use either both find_by and find_key:
            find_by must be an attribute such as "text" or "content-desc"
            find_key would be the corresponding attribute like "Learn More" or "OK"
        or just class_name (will get the first element of that class)
            class_name would be the class_name such as "android.widget.Button"
        """

        # We do this weird comparison becasue you apparently can't test true/false using a xml.etree.ElementTree.Element
        if root == False:
            root = self.get_page_source_xml()

        if find_by:
            for elem in root.iter(class_name):
                if find_by in elem.attrib:
                    if elem.attrib[find_by] == find_key:
                        return elem
        else:
            for elem in root.iter(class_name):
                return elem

        return False

    def _find_element_using_xml(self, root=False, find_by=None, find_key=None, class_name='*'):
        """
        usually you'll use either both find_by and find_key:
            find_by must be an attribute such as "text" or "content-desc"
            find_key would be the corresponding attribute like "Learn More" or "OK"
        or just class_name (will get the first element of that class)
            class_name would be the class_name such as "android.widget.Button"
        """
        elem_or_false = self._exists_element_using_xml(root, find_by=find_by, find_key=find_key, class_name=class_name)

        # this is a weird comparison because you get a warning if you do a
        # simple true/false test using a xml.etree.ElementTree.Element
        if elem_or_false == False:
            raise RuntimeError('_find_using_xml failed with args: find_by=%s find_key=%s class_name=%s' % (
                find_by, find_key, class_name))
        else:
            return elem_or_false

    def _get_dimensions_from_element_using_xml(self, elem):
        """
        Returns dict with dimensions of an element, but using raw xml, not Appium location / size methods.
        Sometimes these methods don't work.  See section header (XML Methods) for details.
        """
        # st will look like '[12,529][756,583]'
        st = elem.attrib['bounds']

        import re
        m = re.search('\[(\d+),(\d+)\]\[(\d+),(\d+)\]', st)
        x1 = int(m.group(1))
        y1 = int(m.group(2))
        x2 = int(m.group(3))
        y2 = int(m.group(4))

        dic = {}
        dic['x'] = x1
        dic['y'] = y1
        dic['width'] = x2 - x1
        dic['height'] = y2 - y1

        return dic

    def verify_exists_using_xml(self, root=False, find_by=None, find_key=None, class_name='*', screenshot=False,
                                timeout=0):
        """
        Verifies an element, but using raw xml, not Appium methods.
        Sometimes these methods don't work.  See section header (XML Methods) for details.
        """
        start_time = time()

        # there's no point in trying multiple times if the root is constant
        if not (root == False):
            timeout = 0

        while True:
            el = self._exists_element_using_xml(root, find_by=find_by, find_key=find_key, class_name=class_name)
            # you apparently can't test true/false using a xml.etree.ElementTree.Element
            if not (el == False):
                el = True
                break

            if time() - start_time > timeout:
                break
            sleep(1)

        self.assertTrueWithScreenShot(el,
                                      screenshot=screenshot,
                                      msg="Should see element with values %s, %s, %s" % (find_by, find_key, class_name))

    def verify_cbs_logo_using_xml(self, root=False, screenshot=False):
        """
        Verifies cbs logo, but using raw xml, not Appium methods.
        Sometimes these methods don't work.  See section header (XML Methods) for details.
        """
        el = self._exists_element_using_xml(root, find_by='resource-id', find_key=self.com_cbs_app + ':id/ibCbsLogo')

        # you apparently can't test true/false using a xml.etree.ElementTree.Element
        if not (el == False):
            el = True

        self.assertTrueWithScreenShot(el, screenshot=screenshot, msg="Should see CBS logo")

    ####################################################################################
    # PLAY / WATCH VIDEOS

    def watch_first_video_on_home(self):
        self.goto_home()
        self.click_first_video()

    def click_first_video(self):
        self.click(id=self.com_cbs_app + ":id/videoImage", data="Click first episode")
        sleep(5)

    def click_info_icon(self):
        """
        Click the little (i) next to an episode description
        """
        e = self.find_one_of('id', self.com_cbs_app + ':id/imgInfo', 'id', self.com_cbs_app + ':id/infoIcon')
        e.click()

    def click_first_aa_info_icon(self):
        """
        Click the little (i) next to the first AA (paid) video in the Primetime section
        """
        y = self.click_first_aa_video()
        if not self.exists(name='Open navigation drawer', timeout=0):
            self.hw_back()

        for elem in self.driver.find_elements_by_id(self.com_cbs_app + ':id/infoIcon'):
            if elem.location['y'] > y:
                elem.click()
                return

        raise RuntimeError('Could not find info icon')

    def wait_for_video_to_start(self, buffer_wait=60):
        """
        Waits for video skin to appear
        This method is problematic because sometimes the loading spinner does not appear at all, and if we wait
        60 seconds, the entire pre-roll ad may finish playing.
        """

        start_time = time()
        self.exists(id=self.com_cbs_app + ':id/loading', timeout=buffer_wait)

        elapsed_time = time() - start_time
        timeout = buffer_wait - elapsed_time

        # make sure we're not still spinning/buffering
        ex = self.not_exists(id=self.com_cbs_app + ':id/loading', timeout=timeout)
        self.assertTrueWithScreenShot(ex, screenshot=False, msg="Assert that video buffer spinner disappears")

    def pause_video(self):
        """
        Taps the pause button by x, y
        """
        # Trying to tap using the com.cbs.app:id\playPause id does not work because we can't scan the page_source
        # while video is up.  Must use x, y
        if self.testdroid_device == 'asus Nexus 7':
            tap_x = 70
            tap_y = 900
        elif self.testdroid_device == 'Amazon KFTBWI':
            tap_x = 26
            tap_y = 730

        # works for Nexus 4,
        else:
            tap_x = 25
            tap_y = self.driver.get_window_size()["height"] - 40

        # First scenario where device navigation control is not up
        self.tap(.25, .25, 'to bring up video player controls')
        sleep(1)
        self.tap(tap_x, tap_y, 'pause button')

    def unpause_video(self):
        """
        Taps the unpause button by x, y
        """
        if self.testdroid_device == 'asus Nexus 7':
            tap_x = 70
            tap_y = 900
        elif self.testdroid_device == 'Amazon KFTBWI':
            tap_x = 26
            tap_y = 730

        # works for Nexus 4,
        else:
            tap_x = 49
            tap_y = self.driver.get_window_size()["height"] - 40

        self.tap(tap_x, tap_y, 'unpause/play button')
        sleep(2)

    def jump_in_video(self, jump_time):
        """
        Tap in the seek bar to jump over.  jump_time is in seconds.
        Find where to tap by dividing jump_time by total_time as found in the screen element
        """
        root = self.get_page_source_xml()

        total_time_elem = self._find_element_using_xml(root, 'resource-id', self.com_cbs_app + ':id/tvTotalTime')
        total_time_text = total_time_elem.attrib['text']

        # total_time = hours*3600 + minutes*60 + seconds
        total_time = float(total_time_text[-2:])
        total_time_text = total_time_text[0:-3]
        total_time += float(total_time_text[-2:]) * 60
        total_time_text = total_time_text[0:-3]
        if total_time_text:
            total_time += float(total_time_text[-2:]) * 3600

        if jump_time > total_time:
            seek_pct = .9
        else:
            seek_pct = jump_time / total_time + .05  # add a little for room for error

        seek_bar = self._find_element_using_xml(root, 'resource-id', self.com_cbs_app + ':id/middleSeekbar')
        seek_bar_dim = self._get_dimensions_from_element_using_xml(seek_bar)

        # width * seek_pct is how far over in the bar to tap
        tap_x = seek_bar_dim['x'] + seek_bar_dim['width'] * seek_pct

        # this is just the vertical middle of the seek bar
        tap_y = seek_bar_dim['y'] + seek_bar_dim['height'] / 2

        sleep(1)
        self.tap(tap_x, tap_y, 'jumping in seek bar')
        sleep(1)
        self.tap(tap_x, tap_y, 'jumping in seek bar')

    def is_ad_playing(self):
        """
        If the seek bar is NOT enabled, an ad must be playing
        Returns True or False
        """
        root = self._get_page_source_xml(True)

        for elem in root.iter('android.widget.SeekBar'):
            if elem.attrib['enabled'] == 'false':
                return True

        return False

    ################################################
    # VALIDATE / VERIFY
    # Some generic validate / verify methods to be used in test-specific validations
    # Some specific validations such as verify_show_card()

    def verify_field_text(self, element, text):
        """
        Takes an element and string, verifies that element.text == text
        """
        elem_text = element.text

        if (type(text) == list and elem_text not in text or
                        type(text) == str and elem_text != text):
            raise RuntimeError("verify_field_text failed: text of element '%s' was '%s' but should have been '%s'" % (
                element.name, elem_text, text))

    def verify_not_equal(self, obj1, obj2, screenshot=False):
        self.assertTrueWithScreenShot(obj1 != obj2, screenshot=screenshot,
                                      msg="'%s' should NOT equal '%s'" % (obj1, obj2))

    def verify_equal(self, obj1, obj2, screenshot=False):
        self.assertTrueWithScreenShot(obj1 == obj2, screenshot=screenshot, msg="'%s' should EQUAL '%s'" % (obj1, obj2))

    def verify_cbs_logo(self, special=None, screenshot=False):
        """
        Verifies that the cbs logo exists using some very hacky means
        """
        sleep(3)
        self.driver.page_source
        # cbs logo in upper left
        logo_exists = False

        win_size = self.driver.get_window_size()
        max_y = .15 * win_size['height']
        max_x = .25 * win_size['width']

        if special == 'video':
            class_name = 'android.widget.ImageButton'
        else:
            class_name = 'android.widget.ImageView'

        # Try this two times.  This is verbose and there are cleaner ways of doing this, but I want the
        # NoSuchElementException to get raised if it's thrown twice, not the assertTrueWithSS exception
        try:
            elems = self.driver.find_elements_by_class_name(class_name)
            for elem in elems:
                size = elem.size
                loc = elem.location
                ratio = float(size['height']) / float(size['width'])
                if (loc['y'] < max_y and loc['x'] < max_x and
                        (0.252 < ratio < 0.258)
                    ):
                    logo_exists = True
                    break
        except NoSuchElementException:
            sleep(60)
            self.driver.page_source
            elems = self.driver.find_elements_by_class_name(class_name)
            for elem in elems:
                size = elem.size
                loc = elem.location
                ratio = float(size['height']) / float(size['width'])
                if (loc['y'] < max_y and loc['x'] < max_x and
                        (0.252 < ratio < 0.258)
                    ):
                    logo_exists = True
                    break

        self.driver.page_source
        self.assertTrueWithScreenShot(logo_exists, screenshot=screenshot, msg='Verifying CBS Logo exists')

    def verify_cbs_logo_square(self, screenshot=False):
        """
        Verifies that the square cbs logo exists using some very hacky means
        """
        # sleep(3)
        # self.driver.page_source
        # # cbs logo in upper left.  this one is square.  this validation sucks
        # logo_exists = False
        #
        # win_size = self.driver.get_window_size()
        # max_y = .15 * win_size['height']
        # max_x = .25 * win_size['width']
        #
        # # Try this two times.  This is verbose and there are cleaner ways of doing this, but I want the
        # # NoSuchElementException to get raised if it's thrown twice, not the assertTrueWithSS exception
        # try:
        #     elems = self.driver.find_elements_by_class_name('android.widget.ImageView')
        #     for elem in elems:
        #         size = elem.size
        #         loc = elem.location
        #         ratio = float(size['height']) / float(size['width'])
        #         if ((ratio == 1.0 or (0.80 < ratio < 0.81)) and
        #                     loc['y'] < max_y and
        #                     loc['x'] < max_x
        #             ):
        #             logo_exists = True
        # except NoSuchElementException:
        #     sleep(45)
        #     self.driver.page_source
        #     sleep(15)
        #     elems = self.driver.find_elements_by_class_name('android.widget.ImageView')
        #     for elem in elems:
        #         size = elem.size
        #         ratio = float(size['height']) / float(size['width'])
        #         if ((ratio == 1.0 or (0.80 < ratio < 0.81)) and
        #                     loc['y'] < max_y and
        #                     loc['x'] < max_x
        #             ):
        #             logo_exists = True
        #
        # self.assertTrueWithScreenShot(logo_exists, screenshot=screenshot, msg='Verifying square CBS Logo exists')
        pass

    def verify_username(self, fn_str=None, ln_str=None):
        """
        Opens the side drawer and verifies username
        Goes to Settings and verifies username
        Needs work
        """
        if not fn_str:
            fn_str = self.fn_str
            ln_str = self.ln_str

        name = fn_str[0] + str(fn_str[1:]).lower() + ' ' + ln_str[0]

        self.open_drawer()

        e = self.exists(id=self.com_cbs_app + ':id/userNameString', timeout=3)
        if e:
            name_str = e.text
        else:
            name_str = self._find_element(id=self.com_cbs_app + ':id/userNameView').text

        self.assertEqualWithScreenShot(name, name_str, screenshot=True,
                                       msg="Expected name in menu: '%s' Actual name in menu: '%s'" % (name, name_str))
        self.close_drawer()

        # todo: fix below
        self.goto_settings()

        name_str = self._find_element(id=self.com_cbs_app + ':id/accountText').get_attribute('text')
        expected_str = 'You are signed in as %s' % name

        self.assertEqualWithScreenShot(expected_str, name_str, screenshot=True,
                                       msg="Expected string in settings: '%s' Actual string in settings: '%s'" % (
                                           expected_str, name_str))

    def verify_live_tv_subscription(self):
        """
        Goes to Live TV and verifies that "Start Watching" buttons appears
        """
        self.goto_live_tv()
        sleep(5)

        self.event.screenshot(self.screenshot())
        if self.exists(name='Start Watching') or self.exists(id=self.com_cbs_app + ":id/showList"):
            return True
        else:
            raise RuntimeError('Live TV is not subscribed to')

    def verify_navigation_drawer_button(self, screenshot=False):
        self.verify_exists(name='Open navigation drawer', screenshot=screenshot)

    verify_menu_icon = verify_navigation_drawer_button

    def verify_share_icon(self, screenshot=False):
        self.click_more()
        self.verify_exists(name='Share', screenshot=screenshot)
        self.hw_back()

    def verify_back_button(self, screenshot=False):
        self.verify_exists(name='Navigate up', screenshot=screenshot)

    def verify_search_text(self, screenshot=False):
        self.verify_exists(id=self.com_cbs_app + ':id/search_src_text', screenshot=screenshot)

    def verify_search_clear_button(self, screenshot=False):
        self.verify_exists(id=self.com_cbs_app + ':id/search_close_btn', screenshot=screenshot)

    def verify_info_icon(self, screenshot=False):
        # (i) image id changed on one screen but not the other
        # imgInfo on individual show page
        # infoIcon on home page
        t_f = self.exists_one_of('id', self.com_cbs_app + ':id/imgInfo', 'id', self.com_cbs_app + ':id/infoIcon')

        self.assertTrueWithScreenShot(t_f, screenshot=screenshot,
                                      msg="Should see element with text or selector: '%s'" % "imgInfo or infoIcon")

    def verify_search_icon(self, screenshot=False):
        self.verify_exists(id=self.com_cbs_app + ':id/action_search', screenshot=screenshot)

    def verify_favorite_icon(self, screenshot=False):
        self.verify_exists(id=self.com_cbs_app + ':id/mycbsButton', screenshot=screenshot)

    def verify_no_shows_found_text(self, screenshot=False):
        self.verify_exists(name="No Shows Found.", screenshot=screenshot)

    def verify_show_card(self, screenshot=False):
        self.verify_exists(id=self.com_cbs_app + ':id/showBrowseCardItem', screenshot=screenshot)

    def verify_show_page_tabs(self, screenshot=False):
        self.verify_exists(class_name='android.widget.HorizontalScrollView', screenshot=screenshot)

    def verify_text_exists(self, txt_or_list, class_name='android.widget.TextView'):
        """
        Verifies that given text exists somewhere (probably as a substring) in an element of class class_name
        For a list of strings, we're checking that ALL the strings in the list are in the SAME ELEMENT

        NOTE: There is NO WAITING for this search!  Make sure the page is fully loaded before performing this.
        """
        ret_val = self._find_element_with_substrings(txt_or_list, class_name)

        self.assertTrueWithScreenShot(ret_val, msg='Should see "%s" on screen' % txt_or_list)
        return ret_val

    def verify_text_not_exists(self, txt_or_list, class_name='android.widget.TextView'):
        """
        Verifies that given text DOES NOT exist (probably as a substring) in an element of class class_name
        For a list of strings, we're checking that ALL the strings in the list are in the SAME ELEMENT

        NOTE: There is NO WAITING for this search!  Make sure the page is fully loaded before performing this.
        """
        ret_val = self._find_element_with_substrings(txt_or_list, class_name)

        self.assertTrueWithScreenShot(not ret_val, msg='Should NOT see "%s" on screen' % txt_or_list)
        return ret_val

    def _find_element_with_substrings(self, txt_or_list, class_name):
        """
        Used by verify_text_exists() and verify_text_not_exists()
        Finds an element whose text contains txt_or_list.  In an element of class class_name
        For a list of strings, we're checking that ALL the strings in the list are in the SAME ELEMENT
        """
        if type(txt_or_list) == str:
            overall_t_f = False
            for elem in self.driver.find_elements_by_class_name(class_name):
                elem_txt = elem.text
                if txt_or_list in elem_txt:
                    overall_t_f = True
                    break
        else:
            overall_t_f = False
            for elem in self.driver.find_elements_by_class_name(class_name):
                # If the first string is in there, make sure all the rest are as well.
                # This logic is complex because there's a slim chance the [0] element may exist in 2 elements,
                # so we may need to check several
                elem_txt = elem.text
                if txt_or_list[0] in elem_txt:
                    t_f = True

                    for txt in txt_or_list:
                        if txt not in elem_txt:
                            t_f = False

                    if t_f:
                        overall_t_f = True
                        break

        if overall_t_f:
            return elem_txt
        else:
            return False

    def send_created_account_email(self):
        """
        Sends an email about the test.  Currently just used for account creation.  To/from
        addresses should be defined in your cbs.py
        Had to update the google account and set "Allow less secure apps: ON"
        """
        try:
            # test if this var exists
            self.created_account
        except AttributeError:
            return

        msg = self.created_account

        MIMEmsg = MIMEText(msg, 'html')
        MIMEmsg["From"] = self.created_email_from_address
        MIMEmsg["To"] = self.created_email_to_address_list
        MIMEmsg["Subject"] = 'automated email: created account'

        try:
            smtp = SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.created_email_from_address, self.created_email_from_password)
            smtp.sendmail(self.created_email_from_address, self.created_email_to_address_list.split(','),
                          MIMEmsg.as_string())
        except Exception as e:
            err = "%s %s" % (type(e), str(e))
            self.event.error(error=err)

        self.created_account = None

    ####################################################################################
    # DEVELOPING / DEBUGGING METHODS
    # Used only in interactive sessions

    def kill_ss(self):
        """
        Can be used in an interactive session.  Turns off screenshot.  Helpful for remote interactive sessions
        because screenshots are really slow.
        """
        klass = type(self)

        # backup our screenshot method in case we want it back later...
        klass.screenshot_bak = klass.screenshot

        def screenshot(self):
            print 'skipping screenshot'

        klass.screenshot = screenshot

    def revive_ss(self):
        """
        For interactive session, turns screenshot back on if you've called kill_ss()
        """
        klass = type(self)

        klass.screenshot = klass.screenshot_bak

    def src(self, elem=None, tab_str='', full=False, recursing=False):
        """
        Quick way to get page source.  In your interactive session, just do a self.src()
        """
        self.src_skip = ['scrollable', 'long-clickable', 'focused', 'checkable', 'password', 'class', 'index',
                         'checked', 'package', 'selected', 'focusable']

        if not recursing:
            self.src_out_str = ''
            source = self.driver.page_source
            try:
                root = ElementTree.fromstring(source.encode('utf-8'))
            except Exception, e:
                print source
                print e.args
                print "\n\nxml.etree.ElementTree failed parsing source.  sorry."
                print e.message
                raise e

            self.src(elem=root, tab_str='', full=full, recursing=True)
            print self.src_out_str
        else:
            self.src_out_str += '\n' + tab_str + elem.tag

            temp_hash = elem.attrib
            for key in temp_hash:
                if not full and key in self.src_skip:
                    continue
                value = temp_hash[key]
                if value == '':
                    value = 'False'

                self.src_out_str += ", " + key + ": " + value

            for child in list(elem):
                self.src(elem=child, tab_str=tab_str + '  ', full=full, recursing=True)

    def qsrc(self, elem=None, tab_str='', full=False, recursing=False):
        """
        # QUICKER way to get page source - shows elements inline for easy comparison
        """
        self.qsrc_skip = ['NAF', 'clickable', 'enabled', 'instance', 'scrollable', 'long-clickable', 'focused',
                          'checkable', 'password', 'class', 'index', 'checked', 'package', 'selected', 'focusable']

        if not recursing:
            self.qsrc_out_str = ''
            source = self.driver.page_source.encode('ascii', 'ignore')
            try:
                root = ElementTree.fromstring(source.encode('utf-8'))
            except Exception, e:
                print source
                print e.args
                print "\n\nxml.etree.ElementTree failed parsing source.  sorry."
                print e.message
                raise e

            self.qsrc(elem=root, tab_str='', full=full, recursing=True)
            print self.qsrc_out_str
        else:
            temp_str = str.ljust(str(elem.tag), 35)

            temp_hash = elem.attrib
            for key in temp_hash:
                if not full and key in self.qsrc_skip:
                    continue
                value = temp_hash[key]
                if value == '':
                    value = 'False'

                if key == 'text':
                    tw = 30
                elif key == 'resource-id':
                    tw = 55
                elif key == 'content-desc':
                    tw = 30
                elif key == 'bounds':
                    tw = 15
                elif key == 'rotation':
                    tw = 30
                else:
                    print "bad key " + key

                temp_str += str.ljust(str(", " + key + ": " + value), tw)

            if len(temp_str) > 180:
                temp_str += "\n"

            self.qsrc_out_str += temp_str + "\n"

            for child in list(elem):
                self.qsrc(elem=child, tab_str=tab_str + '', full=full, recursing=True)
