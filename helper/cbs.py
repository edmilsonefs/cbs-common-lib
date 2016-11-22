import os
import random
import re
import subprocess
from time import sleep, time
from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP
from xml.etree import ElementTree

from selenium.common.exceptions import NoSuchElementException, WebDriverException

from testlio.base import TestlioAutomationTest


class CommonHelper(TestlioAutomationTest):
    phone = False
    tablet = False
    IS_AMAZON = False
    testdroid_device = os.getenv('TESTDROID_DEVICE')
    default_implicit_wait = 120
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

    def setup_method(self, method, caps = False):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi off", shell=True)
        super(CommonHelper, self).setup_method(method, caps)

        self.get_hosting_platform()
        if self.hosting_platform == 'testdroid':
            self.testdroid_device = self.get_testdroid_device_from_adb()

        if 'Tab' in self.testdroid_device \
                or 'Nexus 7' in self.testdroid_device \
                or 'samsung SM-T330NU' == self.testdroid_device \
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
        super(CommonHelper, self).teardown_method(method)

    def get_hosting_platform(self):
        """
        Determine if we're running on testlio platform or testdroid.
        Sets self.hosting_platform
        """
        if 'VIRTUAL_ENV' in os.environ and "ubuntu" in os.environ['VIRTUAL_ENV']:
            self.hosting_platform = 'testdroid'
        else:
            self.hosting_platform = 'testlio'

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

    def set_implicit_wait(self, wait_time=-1):
        """
        Wrapper that sets implicit wait, defaults to self.default_implicit_wait
        """
        if wait_time == -1:
            wait_time = self.default_implicit_wait

        self.driver.implicitly_wait(wait_time)

    def click_until_element_is_visible(self, element_to_be_visible, element_to_click):
        self.driver.implicitly_wait(20)

        element = None
        count = 0
        while element is None and count < 30:
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

    def open_drawer(self):
        self.click(name='Open navigation drawer')

    def close_drawer(self):
        self.driver.back()

    def navigate_up(self):
        self.click(name='Navigate up')

    def go_to(self, menu):
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

    def goto_sign_up(self):
        self.click(name='Sign Up')
        self._hide_keyboard()

    def goto_home(self):
        try:
            self.go_to('Home')
        except:
            self.open_drawer()
            self.go_to('Home')

    def goto_shows(self):
        try:
            self.go_to('Shows')
        except:
            self.open_drawer()
            self.go_to('Shows')

    def goto_subscribe(self):
        try:
            self.go_to('Subscribe')
        except:
            self.open_drawer()
            self.go_to('Subscribe')

    def goto_live_tv(self):
        try:
            self.go_to('Live TV')
            self.click_allow_popup()
            self.driver.implicitly_wait(120)
        except:
            self.open_drawer()
            self.go_to('Live TV')
            self.click_allow_popup()
            self.driver.implicitly_wait(120)

    def goto_schedule(self):
        try:
            self.go_to('Schedule')
        except:
            self.open_drawer()
            self.go_to('Schedule')

    def goto_settings(self):
        try:
            self.go_to('Settings')
        except:
            self.open_drawer()
            self.go_to('Settings')

    def goto_show(self, show_name):
        self.select_search_icon()
        count = 0
        while count < 10:
            if self.exists(class_name='android.widget.ProgressBar', timeout=10):
                sleep(10)
                count += 1
            else:
                break

        self.send_keys_on_search_field(show_name)
        try:
            self.click(id=self.com_cbs_app + ':id/showImage')
        except:
            self.driver.tap([(220, 450)])
            pass
        sleep(5)

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

    def select_search_icon(self):
        self.click(id=self.com_cbs_app + ':id/action_search')
        self.event.screenshot(self.screenshot())

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

        self.driver.activate_ime_engine(new_kybd)

    def tap_keys_on_keyboard(self, txt):
        """
        Sometimes send_keys() doesn't work. Sometimes you just have to tap the keys yourself.
        This will currently work for a limited set of keyboard keys.
        See all Android keycodes at http://developer.android.com/reference/android/view/KeyEvent.html

        example: self.tap_keys_on_keyboard('some string')
        """
        dct = {'-':69, '=':70, '[':71, ']':72, '\\':73, ';':74, '\'':75, '/': 76, ' ':62, ',':55, '.':56, '\t':61, '\r':66, '\n':66}
        dct2 = {')':7, '!':8, '@':9, '#':10, '$':11, '%':12, '^':13, '&':14, '*':15, '(':16, '_':69, '+':70, '{':71, '}':72, '|':73, ':':74, '"':75, '?':76, '<':55, '>':56}

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

    def click_by_location(self, elem, **kwargs):
        """
        sometimes elem.click() fails for whatever reason.  get x,y coords and click by that
        """
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

        # an array of tuples
        self.driver.tap([(x, y)])

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
                  element_or_false.get_attribute('resourceId') or \
                  element_or_false.tag_name

            self.event.click('In click_safe(), about to click.  element info = %s' % msg)
            element_or_false.click()
            return element_or_false
        else:
            return False

    def tap(self, x, y, msg=''):
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

        start_x = location['x'] + size['width'] - 20
        end_x = 20
        y = location['y'] + size['height'] / 2

        try:
            self.driver.swipe(start_x, y, end_x, y, duration)
        except:
            pass
        sleep(1)

    def click_on_first_video(self):
        # all_access_flag = "//android.widget.LinearLayout[./android.widget.TextView[@text='Primetime Episodes']]//*[@resource-id=self.com_cbs_app + ':id/allAccessFlag']";
        #
        # try:
        #     self.driver.implicitly_wait(10)
        #     self.driver.find_element_by_name('Free Episodes')
        #     self._short_swipe_down(duration=5000)
        # except:
        #     self.driver.implicitly_wait(60)
        #     pass
        # if not self.exists(xpath=all_access_flag, timeout=10):
        #     self._short_swipe_down(duration=5000)
        #     if self.phone:
        #         self._short_swipe_down(duration=5000)
        #     sleep(5)
        # list_episodes = self.driver.find_elements_by_xpath(all_access_flag)
        # count = 0
        # while count < len(list_episodes):
        #     list_episodes = self.driver.find_elements_by_xpath(all_access_flag)
        #     self.click(element=list_episodes[count], data='Click on the All Access video on Home Page', screenshot=True)
        #     sleep(5)
        #     if self.exists(id=self.com_cbs_app + ':id/action_search', timeout=10):
        #         self.click(element=list_episodes[count])
        #     try:
        #         self.driver.implicitly_wait(10)
        #         self.driver.find_element_by_name("Already a subscriber? Sign In")
        #         break
        #     except:
        #         self.driver.back()
        #         try:
        #             self.driver.implicitly_wait(10)
        #             self.driver.find_element_by_name("Already a subscriber? Sign In")
        #             break
        #         except:
        #             self.back_while_open_drawer_is_visible()
        #             count += 1
        # sleep(5)
        # self.event.screenshot(self.screenshot())
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_name('Free Episodes')
            self._short_swipe_down(duration=3000)
        except:
            self.driver.implicitly_wait(60)
            pass
        if self.exists(name='paid', timeout=10):
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
        else:
            prime_container = self._find_element(xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Primetime')]]")
            for _ in range(0, 60):
                self._short_swipe_left(prime_container, 1000)
            count = 0
            while count < 70:
                self._short_swipe_left(prime_container, 1000)
                if self.exists(name='paid', timeout=10):
                    list_episodes = self.driver.find_elements_by_name('paid')
                    self.click(element=list_episodes[0])
                    break
                else:
                    count += 1

    def click_any_free_video(self):
        if self.exists(name='free', timeout=10):
            list_episodes = self.driver.find_elements_by_name('free')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()

    def click_play_from_beginning(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_name('Play From Beginning').click()
        except:
            pass
        self.driver.implicitly_wait(30)

    def select_first_show_option(self):
        self.click(id=(self.com_cbs_app + ':id/imgThumbnail'), data='First show icon')

    def click_any_video(self):
        list_episodes = self.driver.find_elements_by_xpath("//android.widget.LinearLayout[./android.widget.TextView[@text='Recently Watched']]//android.widget.ImageView[@resource-id='" + self.com_cbs_app + ":id/videoImage']")
        self.click(element=list_episodes[0])
        self.click_play_from_beginning()
        self.driver.implicitly_wait(30)

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

    def back_while_open_drawer_is_visible(self):
        counter = 0
        self.driver.implicitly_wait(20)
        while counter < 10:
            try:
                self.driver.find_element_by_name("Open navigation drawer")
                break
            except:
                self.driver.back()
                counter += 1
        self.driver.implicitly_wait(self.default_implicit_wait)

    def back_while_navigate_up_is_visible(self):
        counter = 0
        self.driver.implicitly_wait(20)
        while counter < 10:
            try:
                self.driver.find_element_by_name("Navigate up")
                break
            except:
                self.driver.back()
                counter += 1
        self.driver.implicitly_wait(self.default_implicit_wait)

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
                self.driver.find_element_by_xpath("//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@text='" + page_title + "']")
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

        if kwargs.has_key('driver'):
            d = kwargs['driver']
        else:
            d = self.driver

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

        kwargs['timeout'] = 0   # we want exists to return immediately
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
        self.set_implicit_wait(3)

        for i in range(max_swipes):
            try:
                if find_by == 'name':
                    e = self.driver.find_element_by_name(find_key)
                else:
                    e = self.driver.find_element_by_id(find_key)
                self.set_implicit_wait()
                return e
            except NoSuchElementException:
                self.swipe(x, .5, x, 10, 1500)
                pass

        self.set_implicit_wait()
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

    def click_try_1_week_month_free(self):
        self.click(xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                         "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")
        self._hide_keyboard()

    def validation_upsell_page(self):
        self.verify_exists(id=self.com_cbs_app + ':id/allAccessLogo', screenshot=True)
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

    def wait_until_element_is_visible(self, element_css=None, element_name=None, element_id=None, timeout=30):

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
            origin = self.driver.find_element_by_name('Nielsen Info & Your Choices')
            destination = self.driver.find_element_by_name('Send Feedback')
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
        self.click(name='Sign Out', data= 'Sign Out 1')
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

    #### MVPD and NIELSEN
    def goto_nielsen_info_page(self):
        self.goto_settings()
        sleep(1)
        if self.phone:
            self.swipe_down_if_element_is_not_visible(name='Nielsen Info & Your Choices')
        self.click(name='Nielsen Info & Your Choices')
        sleep(15)  # waiting for page to load

    def go_to_debug_page(self):
        window_size_y = self.driver.get_window_size()["height"]
        self.goto_settings()
        if self.phone:
            origin = self.driver.find_element_by_name('Nielsen Info & Your Choices')
            destination = self.driver.find_element_by_name('Send Feedback')
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
            # for i in range(4):
            #     self.driver.swipe(40, window_size_y - 550, 40, 200)
            # self.screenshot()
            self.click(name='Debug')
            self.screenshot()
        else:
            # self.driver.swipe(35, window_size_y - 600, 35, 200)
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
                    # self.driver.swipe(100, window_size_y - 250, 100, 550)
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
        self.event.screenshot(self.screenshot())
        try:
            self.click(xpath='//*[contains(@text,"Disconnect from Optimum")]', data='Disconnect From Optimum')
            self.event.screenshot(self.screenshot())
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

    def swipe_down_if_element_is_not_visible(self, name=None, id_element=None, class_name=None, long_swipe=False, short_swipe=False):
        """
        function that search for element, if element is not found swipe the page until element is found on screen
        """
        self.driver.implicitly_wait(0)

        # Gets mobile screen size
        window_size_y = self.driver.get_window_size()["height"]

        element = None
        count = 0
        while element is None and count <= 20:
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
        while element is None and count <= 20:
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

    def log_info(self, info):
        self.event._log_info(self.event._event_data(info))