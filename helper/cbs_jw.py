from cbs import *


class CCommonHelperJW(CommonHelper):
    # This is just to sent the email, it's not really part of testing.
    # Don't update this as long as it's working.

    ####################################################################################
    # SETUP/LOGIN METHODS

    def setup_method(self, method):
        super(CCommonHelperJW, self).setup_method(method, {"unicodeKeyboard": True, "resetKeyboard": True})

        self.set_implicit_wait()

        self.activate_standard_keyboard()
        self.driver.orientation = 'PORTRAIT'

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

        self.event.screenshot(self.screenshot())

        # For the Chromecast button:
        self.click_safe(id=self.com_cbs_app + ':id/showcase_button', timeout=10)

        if 'kftbwi' in self.testdroid_device.lower():
            self.IS_AMAZON = True
        else:
            self.IS_AMAZON = False

        if self.is_drawer_open():
            self.close_drawer()

        # For the Chromecast button:
        self.click_safe(id=self.com_cbs_app + ':id/showcase_button', timeout=10)

    def teardown_method(self, method):
        super(CCommonHelperJW, self).teardown_method(method)

    # def logout(self):
    #     self.goto_settings()
    #     sleep(2)
    #     self.swipe(.5, .8, .5, .2, 500)
    #     sleep(1)
    #     self.swipe(.5, .8, .5, .2, 1000)
    #
    #     self.find_on_page('name', "Sign Out").click()
    #
    #     self.click(id=self.com_cbs_app + ':id/signOutButton')



    ####################################################################################
    # RANDOM HELPER METHODS

    ####################################################################################
    # NAVIGATION

    # def close_drawer(self):
    #     self.swipe(.7, .7, .1, .7, 500)
    #     sleep(1.5)

    def goto_sign_up(self):
        self.goto_sign_in()
        self._hide_keyboard()
        sleep(1)

        if not self.click_safe(name="Don't have an account? Sign Up"):
            self.click(name="Sign Up")

        self.verify_exists(name='Sign up with your email')
        sleep(1)

    # def goto_nav_list_item(self, label):
    #     """
    #     Most goto_<nav item>() methods just use click, but sometimes the word (such as My CBS) may appear other
    #     places on the screen, so we have to be smarter (and slower) about it
    #     """
    #     self.open_drawer()
    #     elems = self.driver.find_elements_by_id(self.com_cbs_app + ':id/navigation_list_item_text')
    #     for elem in elems:
    #         if elem.text == label:
    #             elem.click()
    #             return
    #
    #     raise RuntimeError("No such menu item: %s" % label)

    # def goto_home(self):
    #     self.goto_nav_list_item("Home")
    #     page_is_loaded = self.exists(id=self.com_cbs_app + ':id/sectionView')
    #     if not page_is_loaded:
    #         self.event.screenshot(self.screenshot())
    #     self.assertTrueWithScreenShot(page_is_loaded, screenshot=False,
    #                                   msg="Assert show icons are loaded on home page.")
    #
    # def goto_shows(self):
    #     self.open_drawer()
    #     self.click(name="Shows")
    #
    # def goto_live_tv(self):
    #     """
    #     Goes to Live TV page and handles any popups
    #     """
    #     self.open_drawer()
    #     self.click(name="Live TV")
    #     if self.click_safe(id='com.android.packageinstaller:id/permission_allow_button', timeout=60):
    #         self.click_safe(id='com.android.packageinstaller:id/permission_allow_button', timeout=5)
    #
    #     if self.click_safe(name='TRY AGAIN', timeout=10) or self.click_safe(name='Try Again', timeout=1):
    #         sleep(5)
    #
    # def goto_schedule(self):
    #     self.open_drawer()
    #     self.click(name="Schedule")
    #
    # def goto_shop(self):
    #     self.open_drawer()
    #     self.click(name="Shop")
    #
    # def goto_settings(self):
    #     self.goto_nav_list_item("Settings")
    #     sleep(1)

    # def wait_for_show_page_to_load(self):
    #     # # page_is_loaded = self.exists(id=self.com_cbs_app + ':id/imgInfo')
    #     # page_is_loaded = self.exists(id=self.com_cbs_app + ':id/imgHeader')
    #     # if not page_is_loaded:
    #     #     self.event.screenshot(self.screenshot())
    #     # self.assertTrueWithScreenShot(page_is_loaded, screenshot=False, msg="Assert show icons are loaded on show page.")
    #     sleep(10)

    # def click_by_location(self, elem, msg=None):
    #     """
    #     sometimes elem.click() fails for whatever reason.  get x,y coords and click by that
    #     """
    #     if not msg:
    #         msg = elem.text or \
    #               elem.get_attribute('name') or \
    #               elem.get_attribute('resourceId') or \
    #               elem.tag_name
    #
    #         msg = 'About to click by location...  element info = %s' % msg
    #
    #     loc = elem.location
    #     size = elem.size
    #     x = loc['x'] + size['width'] / 2
    #     y = loc['y'] + size['height'] / 2
    #
    #     # an array of tuples
    #     self.tap(x, y, msg)

    # def exists(self, **kwargs):
    #     """
    #     Finds element and returns it (or False).  Waits up to <implicit_wait> seconds.
    #     Optional parameter: timeout=10 if you only want to wait 10 seconds.  Default=default_implicit_wait
    #
    #     advanced:
    #         call using an element:
    #         my_layout = self.driver.find_element_by_class_name('android.widget.LinearLayout')
    #         self.exists(name='Submit', driver=my_layout)
    #     """
    #     if 'timeout' in kwargs:
    #         self.set_implicit_wait(kwargs['timeout'])
    #
    #     if 'driver' in kwargs:
    #         d = kwargs['driver']
    #     else:
    #         d = self.driver
    #
    #     try:
    #         if 'name' in kwargs:
    #             e = d.find_element_by_name(kwargs['name'])
    #         elif 'class_name' in kwargs:
    #             e = d.find_element_by_class_name(kwargs['class_name'])
    #         elif 'id' in kwargs:
    #             e = d.find_element_by_id(kwargs['id'])
    #         elif 'xpath' in kwargs:
    #             e = d.find_element_by_xpath(kwargs['xpath'])
    #         else:
    #             raise RuntimeError("exists() called with incorrect param. kwargs = %s" % kwargs)
    #
    #         return e
    #     except NoSuchElementException:
    #         return False
    #     finally:
    #         self.set_implicit_wait()
    #
    # def click_first_aa_video(self, screenshot=False):
    #     """
    #     Scrolls down to Primetime section, then clicks through the videos until it finds one that is All Access
    #     """
    #
    #     # Leave this sleep here.  App was doing a weird thing were for a
    #     #   split second "Primetime" existed, then it refreshed.
    #     sleep(2)
    #
    #     # In case we've swiped down the page before, swipe to top of the page to reset
    #     self.swipe(.5, .2, .5, .9, 500)
    #     sleep(1)
    #
    #     elem = self.find_on_page('name', 'Primetime Episodes')
    #     if screenshot:
    #         self.event.screenshot(self.screenshot())
    #
    #     if not elem:
    #         raise RuntimeError('Failed finding "Primetime Episodes" on page.')
    #
    #     self.swipe_element_to_top_of_screen(elem, endy=.2, startx=0)
    #     sleep(1)
    #
    #     window_size = self.driver.get_window_size()
    #     window_y = window_size["height"]
    #     window_x = window_size['width']
    #
    #     # banner ad at bottom:
    #     # we'll start our right-to-left swipe just to the right of it, or at .9, whichever is further right
    #     ad_elem = self._find_element(class_name='android.webkit.WebView')
    #     swipe_start_x = ad_elem.location['x'] + ad_elem.size['width'] + 5
    #
    #     if float(swipe_start_x) / float(window_x) < .9:
    #         swipe_start_x = .9
    #
    #     self.set_implicit_wait(1)
    #     for i in range(25):
    #         elem = self.exists(id='paid')
    #         if elem:
    #
    #             # tedious.  If it's too high or too low, we might tap the title bar or the advertisement by accident...
    #             loc = elem.location
    #             correction_swipe_start_y = None
    #             if loc['y'] < window_y * .25:
    #                 correction_swipe_start_y = .5
    #                 correction_swipe_end_y = .8
    #             elif loc['y'] > window_y * .75:
    #                 correction_swipe_start_y = .8
    #                 correction_swipe_end_y = .5
    #
    #             # more tedium.  All we want to do is swipe up a bit and then click, but sometimes after swiping,
    #             # UIAutomator still thinks the element is in the old location, so we'll do a page_source and _find()
    #             # a few times until it reports a new location
    #             if correction_swipe_start_y:
    #                 self.swipe(.5, correction_swipe_start_y, .5, correction_swipe_end_y, 1000)
    #
    #                 for j in range(5):
    #                     sleep(1)
    #                     self.driver.page_source
    #                     elem = self._find_element(id='paid')
    #
    #                     new_loc = elem.location
    #                     if new_loc != loc:
    #                         loc = new_loc
    #                         break
    #
    #             self.event.screenshot(self.screenshot())
    #             self.event.click('About to click first AA video.  element info = %s' % loc)
    #             elem.click()
    #             self.set_implicit_wait()
    #             return
    #
    #         self.event.screenshot(self.screenshot())
    #
    #         # yes we really need to do this many...
    #         for temp_y in [.25, .4, .5, .7, .96]:
    #             self.swipe(swipe_start_x, temp_y, .2, temp_y, 600)
    #
    #         sleep(1)
    #
    #     self.set_implicit_wait()
    #     raise RuntimeError('could not find a paid video in Primetime section')