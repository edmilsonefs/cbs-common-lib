from ios_cbs import *


class CommonIOSHelperJW(CommonIOSHelper):

    # You only have to click the Accept Terms box and CONTINUE button the very first time you log in
    # Kind of an edge case, but very necessary in case you log in and log out repeatedly
    already_accepted_terms = False

    passed = False

    def setup_method(self, method):
        super(CommonIOSHelperJW, self).setup_method(method,
                                          {'waitForAppScript': '$.delay(5000); $.acceptAlert();'})

        self.set_implicit_wait()

        # wait for the splash screen to disappear
        self.not_exists(accessibility_id='SplashEyeLogo', timeout=180)
        self.goto_home()

    def teardown_method(self, method):
        if self.passed:
            self.event.start(data='Test completed successfully')
        else:
            self.event.start(data='Test failed. Getting screenshot and page_source.')
            if self.driver:
                try:
                    self.event.screenshot(self.screenshot())
                except Exception:
                    self.event.start(data='in teardown: screenshot failed')
                try:
                    self.driver.page_source
                except Exception:
                    self.event.start(data='in teardown: page source failed')

        self.event.stop()
        sleep(60)

        try:
            self.driver.quit()
        except Exception:
            self.event.start(data='in teardown: driver.quit() failed')

        sleep(80)


####################################################################################
# SETUP/LOGIN METHODS

    def login(self, username, password):
        """
        This assumes you are on the Sign In screen.
        """

        # username
        if self.phone:
            user_elem = self._find_element(class_name='UIATextField')
        else:
            for e in self.driver.find_elements_by_xpath("//UIATextField[@value='Email']"):
                if e.is_displayed():
                    user_elem = e
                    break

        user_elem.click()
        self.send_keys(element=user_elem, data=username)

        # password
        if self.phone:
            pwd_elem = self._find_element(class_name='UIASecureTextField')
        else:
            for e in self.driver.find_elements_by_xpath("//UIASecureTextField[@value='Password']"):
                if e.is_displayed():
                    pwd_elem = e
                    break

        pwd_elem.click()
        self.send_keys(element=pwd_elem, data=password)

        # sign in button
        if self.phone:
            sign_in_button = self._find_element(xpath="//UIAButton[@name='SIGN IN']")
        else:
            for e in self.driver.find_elements_by_xpath("//UIAButton[@name='SIGN IN']"):
                if e.is_displayed():
                    sign_in_button = e
                    break

        sleep(3)
        sign_in_button.click()

        # continue_button = self.exists(accessibility_id='CONTINUE', timeout=300)
        # agreement = "By registering you become a member of the CBS Interactive family of sites and you have read and agree to the Terms of Use, Privacy Policy, and Video Services Policy. You agree to receive updates, alerts and promotions from CBS and that CBS may share information about you with our marketing partners so that they may contact you by email or otherwise about their products or services."
        # agreement_elem = self._find_element(accessibility_id=agreement)
        # loc = agreement_elem.location
        #
        # for button in self.driver.find_elements_by_xpath("//UIAButton[@name='']"):
        #     button_loc = button.location
        #     loc_y_above = loc['y'] - 15
        #     loc_y_below = loc['y'] + 15
        #     if (button_loc['x'] < loc['x'] and
        #         loc_y_above < button_loc['y'] < loc_y_below):
        #         self.click_by_location(button)
        #         break

        # continue_button = self.exists(accessibility_id='CONTINUE', timeout=300)
        # loc = continue_button.location
        #
        # for button in self.driver.find_elements_by_xpath("//UIAButton[@name='']"):
        #     button_loc = button.location
        #     if (button_loc['x'] < loc['x'] and
        #         button_loc['y'] < loc['y']):
        #         self.click_by_location(button)
        #         sleep(1)
        #         break

        if not self.already_accepted_terms:
            continue_button = self.exists(accessibility_id='CONTINUE', timeout=300)

            for button in self.driver.find_elements_by_xpath("//UIAButton[@name='']"):
                try:
                    button.click()
                except Exception:
                    pass

            self.event.screenshot(self.screenshot())
            continue_button.click()

            # wait for the login to happen
            self.not_exists(accessibility_id='CONTINUE', timeout=300)
            self.already_accepted_terms = True

        self.goto_settings()
        self.assertTrueWithScreenShot(self.exists(accessibility_id='Sign Out', timeout=0),
                                      screenshot=True,
                                      msg="Verify 'Sign Out' button on Settings page.")

    def logout(self, safe=False):
        self.goto_settings()
        if safe:
            self.click_safe(id='Sign Out', timeout=3)
        else:
            self.click(id='Sign Out')

    def mvpd_logout(self):
        pass

        # this is the android 2.9 version:
        # self.goto_settings()
        # self.find_on_page('accessibility_id', "Rate This App", 5)
        # self.screenshot()
        #
        # element = self.exists(id='Disconnect from Optimum', timeout=2)
        # if (element):
        #     self.click_by_location(element)
        #
        # element = self.exists(id='com.cbs.app:id/btnMvpdLogoutSettings', timeout=2)
        # if (element):
        #     self.click_by_location(element)
        #     self.screenshot()
        #     sleep(4)
        #     self.screenshot()
        #
        # element = self.exists(id='android:id/button1', timeout=2)
        # if (element):
        #     self.click_by_location(element)
        #     sleep(3)
        #     self.screenshot()

####################################################################################
# LOW LEVEL METHODS

    def execute_script(self, script):
        """
        send javascript directly, for example see _accept_terms_popup()
        """
        sleep(5)
        self.driver.execute_script('var target = UIATarget.localTarget();')
        self.driver.execute_script(script)

####################################################################################
# RANDOM HELPER METHODS

    def is_simulator(self):
        # if it's hardware, we will instead find '.ipa' in this capability
        return '.app' in self.driver.capabilities['app']

    def clear_text_field(self, text_field, default_text=''):
        # text_field.click()
        # text = text_field.text
        #
        # del_key = self._find_element(xpath="//UIAKey[@name='delete']")
        # for i in range(len(text)):
        #     del_key.click()
        t_f = self.clear_text_field_01(text_field, default_text)

        if not t_f:
            t_f = self.clear_text_field_02(text_field, default_text)

        if not t_f:
            t_f = self.clear_text_field_03(text_field, default_text)

        self.assertTrueWithScreenShot(t_f, screenshot=True, msg="Textfield should be blank or equal some default text")

    def clear_text_field_01(self, text_field, default_text=''):

        for i in range(3):
            text_field.click()

            sleep(1.5)
            try:
                self.click(id='Select All')
                break
            except:
                pass

        sleep(3)
        del_key = self.exists(xpath="//UIAKey[@name='delete']")
        if del_key:
            del_key.click()
        else:
            self.click(id="Cut")

        if default_text == '':
            t_f = text_field.text == ''
        else:
            t_f = default_text in text_field.text

        return t_f

    def clear_text_field_02(self, text_field, default_text=''):
        size = text_field.size
        loc = text_field.location

        x = loc['x'] + size['width'] - 15
        y = loc['x'] + size['height']/2
        self.tap(x, y)

        del_key = self.exists(xpath="//UIAKey[@name='delete']")

        for i in range(len(text_field.text)):
            del_key.click()

        if default_text == '':
            t_f = text_field.text == ''
        else:
            t_f = default_text in text_field.text

        return t_f

    def clear_text_field_03(self, text_field, default_text=''):
        del_key = self.exists(xpath="//UIAKey[@name='delete']")

        for i in range(len(text_field.text)):
            del_key.click()

        if default_text == '':
            t_f = text_field.text == ''
        else:
            t_f = default_text in text_field.text

        return t_f

    def _accept_alert(self):
        for x in range(0, 5):
            try:
                # Accepts terms of service & other popups there may be
                self.wait_and_accept_alert()
                sleep(5)
                break
            except:
                pass

    def _accept_notification_popup(self):
        self.execute_script('target.frontMostApp().alert().cancelButton().tap();')

    def _accept_terms_popup(self):
        self.execute_script('target.frontMostApp().alert().cancelButton().tap();')

    def generate_random_alfa_num_string(self, length=8):
        return str(''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length)))

    def generate_random_string(self, length=8):
        return str(''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length)))

    def _hide_keyboard(self):
        if self.is_keyboard_displayed():
            if self.phone:
                size = self.driver.get_window_size()

                x = size['width']/2
                start_y = size['height']/2
                end_y = size['height']

                self.driver.swipe(x, start_y, x, end_y, 500)
            elif self.tablet:
                size = self.driver.get_window_size()
                self.tap(size['width'] - 30, size['height'] - 30)

    def is_keyboard_displayed(self):
        return self.exists(xpath='//UIAKeyboard', timeout=2)

    def convert_season_episode(self, se_input):
        """
        Converts back/forth between string "S4 Ep22" and tuple (4,22) representation of the Season and Episode string
        found on episode descriptions
        """
        if type(se_input) == str:
            se_input = se_input[1:]
            se_input.replace(' ', '')

            e_ndx = se_input.index('E')

            #sometimes it looks like "S14 E10" and sometimes it's "S14 Ep10"
            if "Ep" in se_input:
                ep_offset = 2
            else:
                ep_offset = 1

            # return two ints
            return int(se_input[:e_ndx]), int(se_input[e_ndx+ep_offset:])

        else:
            # return it as "S14 Ep10"
            return "S%s Ep%s" % (se_input[0], se_input[1])

    def convert_season_episode_to_long_form(self, se_input):
        """
        Converts from "S27Ep4" to what's on the element's name, currently "S27 Ep4 Season 27 Episode 4"
        """
        se_input = se_input[1:]
        se_input.replace(' ', '')

        e_ndx = se_input.index('E')

        #sometimes it looks like "S14 E10" and sometimes it's "S14 Ep10"
        if "Ep" in se_input:
            ep_offset = 2
        else:
            ep_offset = 1

        s = se_input[:e_ndx]
        e = se_input[e_ndx+ep_offset:]

        return "S%s Ep%s Season %s Episode %s" % (s, e, s, e)

    def convert_title_season_episode_to_long_form(self, se_input, title_input):
        """
        Converts from "S27Ep4" to what's on the element's name, currently "The Price Is Right Season 44 Episode 178"
        """
        se_input = se_input[1:]
        se_input.replace(' ', '')

        e_ndx = se_input.index('E')

        #sometimes it looks like "S14 E10" and sometimes it's "S14 Ep10"
        if "Ep" in se_input:
            ep_offset = 2
        else:
            ep_offset = 1

        s = se_input[:e_ndx]
        e = se_input[e_ndx+ep_offset:]

        return "%s Season %s Episode %s" % (title_input, s, e)



####################################################################################
# PHONE/HARDWARE METHODS


####################################################################################
# NAVIGATION

    def open_drawer(self, native=False):
        e = self.exists_and_visible(id='Main Menu', timeout=1)

        if not e:
            self.go_back()
            sleep(1)
            e = self.exists_and_visible(id='Main Menu', timeout=3)

        if e.location['x'] > 80:
            return

        if e:
            e.click()
        else:
            self.go_back()
            sleep(1)
            self.click(id='Main Menu')

    def close_drawer(self):
        e = self.exists_and_visible(id='Main Menu')

        if e.location['x'] < 80:
            return

        if e:
            e.click()
        else:
            self.go_back()
            sleep(1)
            self.click(id='Main Menu')

    def goto_sign_in(self, native=False):
        self.open_drawer()
        self.click(id='Sign In')

    def goto_sign_up(self):
        self.goto_sign_in()
        self.click(id='Sign Up')

    def go_back(self):
        elem = self.exists(id='BackArrow_white', timeout=2)
        if not elem:
            elem = self._find_element(xpath="//UIAButton[@name='Back']")

        # stupid bug where the < button is offscreen, but the hamburger is in its place (but invisible, so we
        # use click_by_location)
        loc = elem.location
        if loc['x'] < 0 or loc['y'] < 0:
            elem = self._find_element(id='Main Menu')
            self.click_by_location(elem)
        else:
            elem.click()

    def goto_home(self):
        self.open_drawer()
        self.click(id='Home')

    def goto_shows(self):
        self.open_drawer()
        self.click(id='Shows')

    def goto_live_tv(self):
        self.open_drawer()
        self.click(id='Live TV')
        self.click_safe(accessibility_id='Accept', timeout=60)
        self.click_safe(accessibility_id='Allow', timeout=1)

    def goto_schedule(self):
        self.open_drawer()
        self.click(id='Schedule')

    def goto_settings(self):
        self.open_drawer()
        self.click(xpath="//UIATableCell[@name='Settings']")

    def goto_show(self, show_name):
        self.search_for(show_name)
        self.click_first_search_result()
        t_f = (self.exists(id='MyCBSStarOutlined iPhone', timeout=30) or
               self.exists(id='MyCBSStarOutlined iPad', timeout=0))

        self.assertTrueWithScreenShot(t_f, msg="Assert we're on individual show page")

    # def goto_show(self, show_name):
    #     self.goto_settings()
    #     self.click(id='SearchIcon white')
    #     e = self._find_element(id='Search for a Show')
    #     self.send_keys(show_name, e)
    #     self.click(class_name='UIACollectionCell')

####################################################################################
# CLICK WRAPPERS

    def click_search_icon(self):
        self.click(xpath="//UIAButton[@name='Search']")

    def click_search_text(self):
        self.find_search_text().click()

    def clear_search(self):
        e = self.find_search_text()
        self.clear_text_field(e, 'Search')

    def click_search_back(self):
        self.driver.find_elements_by_xpath("//UIAButton[@name='Cancel']")[-1].click()

    def click_return(self):
        size = self.driver.get_window_size()
        self.driver.tap(size['width'] - 30, size['height'] - 30)

    def click_more(self):
        self.click(id='More Information')

    def click_close_cta(self):
        self.click(id='upsell close')

####################################################################################
# GET WRAPPERS

    def get_search_result_episode_count_element(self):
        collection_views = self.driver.find_elements_by_xpath("//*[@value='page 1 of 1']")

        for cell in collection_views:
            static_texts = cell.find_elements_by_class_name('UIAStaticText')
            for static_text in static_texts:
                if ' Episode' in static_text.text:
                    return static_text

####################################################################################
# SWIPE / TAP / CLICK / SEND_KEYS

    def swipe_element_to_top_of_screen(self, elem, endy=None, startx=-20):
        """
        Swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        startx = elem.location['x']+startx
        starty = elem.location['y']

        if (not endy):
            if (self.phone):
                endy = 70
            else:
                endy = 180

        self.swipe(startx, starty, startx, endy, 1500)

####################################################################################
# SHOWS

    #### old way, when the more info icon existed in the page_source:
    ####
    # def click_info_icon_on_found_on_show_page(self, show_elem, season_name):
    #     elems = self.driver.find_elements_by_name('More Info, %s' % season_name)
    #     closest_x = 9999
    #     show_elem_x = show_elem.location['x']
    #     for elem in elems:
    #         elem_x = elem.location['x']
    #         if show_elem_x < elem_x and elem_x < closest_x:
    #             closest_x = elem_x
    #             closest = elem
    #
    #     closest.click()

    def click_info_icon_on_found_on_show_page(self, show_elem):
        # swipe it to the middle of the screen
        loc = show_elem.location
        x = loc['x']
        y = loc['y']

        size = show_elem.size
        width = size['width']
        height = size['height']

        self.swipe(x, y, 10, y, 1500)
        sleep(1)

        # use offsets to tap the (i) icon
        loc = show_elem.location
        x = loc['x']
        y = loc['y']

        size = show_elem.size
        width = size['width']
        height = size['height']

        tap_x = int(x + width*.88)
        tap_y = int(y + height*.95)

        self.tap(tap_x, tap_y)

    def find_episode_on_show_page(self, show_dict):
        season_name = "Season " + str(self.convert_season_episode(show_dict['season_episode'])[0])
        season_xpath = "//UIAStaticText[@name='%s']" % season_name

        season_elem = self.find_on_page('xpath', season_xpath)
        self.assertTrueWithScreenShot(season_elem, screenshot=True, msg="Assert our season exists")
        self.swipe_element_to_top_of_screen(season_elem, endy=.25, startx=20)

        #don't think necessary for ios: find it again to be sure we get the right positioning
        #season_elem = self._find_element(xpath=season_xpath)
        y = season_elem.location['y'] + season_elem.size['height'] + 50
        y_below = season_elem.location['y']

        season_ep_long = self.convert_season_episode_to_long_form(show_dict['season_episode'])

        show_elem = self.find_on_page_horizontal('accessibility_id', season_ep_long, swipe_y=y, max_swipes=10, y_below=y_below)
        self.assertTrueWithScreenShot(show_elem, screenshot=True, msg="Assert our show exists")

        self.click_info_icon_on_found_on_show_page(show_elem)
        sleep(2)

        scroll_views = self.driver.find_elements_by_class_name('UIAScrollView')
        texts = scroll_views[-1].find_elements_by_class_name('UIAStaticText')

        show_title_found = texts[0].text
        season_ep_found = texts[1].text
        ndx = texts[2].text.index(' ')  # remove the "Aired: "
        air_date_found = texts[2].text[ndx+1:]
        ndx = len(show_dict['episode_title'])  # remove the description after the actual title of the episode
        episode_title_found = texts[3].text[0:ndx]

        show_dict_found = {}
        show_dict_found['element']        = show_elem
        show_dict_found['show_title']     = show_title_found
        show_dict_found['episode_title']  = episode_title_found
        show_dict_found['air_date']       = air_date_found
        show_dict_found['season_episode'] = season_ep_found

        return show_dict_found

    def find_show_on_home_page(self, show_dict):
        """
        First scrolls down looking for the show category (Primetime, etc.)
        Then scrolls to the side looking for the episode
        show_dict should look like
            {'show_title': 'CSI Miami',
            'show_category': 'Primetime'}

        Returns a dict that looks like:
            {'show_title': 'CSI Miami',
            'episode_title': 'Fun in the Sun',
            'air_date': '3/5/16',
            'season_episode': 'S28Ep8''}
        """
        show_title = show_dict['show_title']
        show_category = show_dict['show_category']
        category_xpath = "//UIAStaticText[@name='%s']" % show_category
        category_elem = self.find_on_page('xpath', category_xpath)

        self.assertTrueWithScreenShot(category_elem, screenshot=True, msg="Assert our category exists")
        self.swipe_element_to_top_of_screen(category_elem, endy=.25, startx=20)

        y = category_elem.location['y'] + category_elem.size['height'] + 50
        y_below = category_elem.location['y']

        season_ep_long = self.convert_title_season_episode_to_long_form(show_dict['season_episode'], show_title)

        show_elem = self.find_on_page_horizontal('accessibility_id', season_ep_long, swipe_y=y, max_swipes=10, y_below=y_below)
        self.assertTrueWithScreenShot(show_elem, screenshot=True, msg="Assert our show exists")

        self.click_info_icon_on_found_on_show_page(show_elem)
        sleep(2)

        scroll_views = self.driver.find_elements_by_class_name('UIAScrollView')
        texts = scroll_views[-1].find_elements_by_class_name('UIAStaticText')

        show_title_found = texts[0].text
        season_ep_found = texts[1].text
        ndx = texts[2].text.index(' ')  # remove the "Aired: "
        air_date_found = texts[2].text[ndx+1:]
        ndx = len(show_dict['episode_title'])  # remove the description after the actual title of the episode
        episode_title_found = texts[3].text[0:ndx]

        show_dict_found = {}
        show_dict_found['element']        = show_elem
        show_dict_found['show_title']     = show_title_found
        show_dict_found['episode_title']  = episode_title_found
        show_dict_found['air_date']       = air_date_found
        show_dict_found['season_episode'] = season_ep_found

        return show_dict_found

    def enter_search_text(self, what_to_search_for):
        e = self.find_search_text()
        self.send_keys(element=e, data=what_to_search_for)

    def search_for(self, what_to_search_for):
        self.click_search_icon()
        self.enter_search_text(what_to_search_for)

    def click_first_search_result(self):
        element = self.get_search_result_episode_count_element()
        element.click()

####################################################################################
# FIND / EXISTS

    def find_search_text(self):
        if self.exists(id='Search for a Show', timeout=2):
            return self._find_element(id='Search for a Show')
        else:
            return self.driver.find_elements_by_class_name('UIATextField')[-1]

    def find_on_page_horizontal(self, find_by, find_value, max_swipes=10, swipe_y=.5, y_below=-1):
        if y_below == -1:
            y_below = swipe_y

        self.set_implicit_wait(0)

        for i in range(max_swipes):
            self.driver.page_source
            if find_by == 'accessibility_id':
                elems = self.driver.find_elements_by_name(find_value)
            else:
                elems = self.driver.find_elements_by_id(find_value)

            for elem in elems:
                if elem.location['y'] > y_below and \
                   elem.is_displayed():
                    self.set_implicit_wait()
                    return elem

            self.swipe(.7, swipe_y, 10, swipe_y, 1500)

        self.set_implicit_wait()
        return False
        #raise NoSuchElementException("find_on_page_horizontal failed looking for '%s'" % elem_id)

    def verify_not_equal(self, obj1, obj2, screenshot=False):
        self.assertTrueWithScreenShot(obj1 != obj2, screenshot=screenshot, msg="'%s' should NOT equal '%s'" % (obj1, obj2))

    def verify_equal(self, obj1, obj2, screenshot=False):
        self.assertTrueWithScreenShot(obj1 == obj2, screenshot=screenshot, msg="'%s' should EQUAL '%s'" % (obj1, obj2))

    def verify_exists(self, **kwargs):
        """
        Uses self.exists()
        Optional params: screenshot (default: False), timeout (default: default_implicit_wait)
        """
        screenshot = kwargs.get('screenshot')

        if 'accessibility_id' in kwargs:
            selector = kwargs['accessibility_id']
        elif 'class_name' in kwargs:
            selector = kwargs['class_name']
        elif 'id' in kwargs:
            selector = kwargs['id']
        elif 'xpath' in kwargs:
            selector = kwargs['xpath']

        self.assertTrueWithScreenShot(self.exists(**kwargs), screenshot=screenshot,
                                      msg="Should see element with text or selector: '%s'" % selector)

    def verify_exists_and_visible(self, **kwargs):
        screenshot = kwargs.get('screenshot')

        if 'accessibility_id' in kwargs:
            selector = kwargs['accessibility_id']
        elif 'class_name' in kwargs:
            selector = kwargs['class_name']
        elif 'id' in kwargs:
            selector = kwargs['id']
        elif 'xpath' in kwargs:
            selector = kwargs['xpath']

        elem = self.exists(**kwargs)
        if elem:
            t_f = elem.is_displayed()

        self.assertTrueWithScreenShot(t_f, screenshot=screenshot,
                                      msg="Should see element with text or selector: '%s'" % selector)

    def verify_not_exists(self, **kwargs):
        """
        Uses self.not_exists()
        Optional params: screenshot (default: False), timeout (default: 30 sec)
        """
        screenshot = kwargs.get('screenshot')

        if not 'timeout' in kwargs:
            kwargs['timeout'] = 30

        if 'accessibility_id' in kwargs:
            selector = kwargs['accessibility_id']
        elif 'class_name' in kwargs:
            selector = kwargs['class_name']
        elif 'id' in kwargs:
            selector = kwargs['id']
        elif 'xpath' in kwargs:
            selector = kwargs['xpath']

        self.assertTrueWithScreenShot(self.not_exists(**kwargs), screenshot=screenshot,
                                      msg="Should NOT see element with text or selector: '%s'" % selector)

    def exists(self, **kwargs):
        """
        Finds element and returns it (or False).  Waits up to <implicit_wait> seconds.
        Optional parameter: timeout=10 if you only want to wait 10 seconds.  Default=default_implicit_wait

        advanced:
            call using an element:
            my_layout = self.driver.find_element_by_class_name('android.widget.LinearLayout')
            self.exists(id='Submit', driver=my_layout)
        """
        if 'timeout' in kwargs:
            self.set_implicit_wait(kwargs['timeout'])

        if 'driver' in kwargs:
            d = kwargs['driver']
        else:
            d = self.driver

        try:
            if 'accessibility_id' in kwargs:
                e = d.find_element_by_accessibility_id(kwargs['accessibility_id'])
            elif 'class_name' in kwargs:
                e = d.find_element_by_class_name(kwargs['class_name'])
            elif 'id' in kwargs:
                e = d.find_element_by_id(kwargs['id'])
            elif 'xpath' in kwargs:
                e = d.find_element_by_xpath(kwargs['xpath'])
            else:
                raise RuntimeError("exists() called with incorrect param. kwargs = %s" % kwargs)

            return e
        except NoSuchElementException:
            return False
        finally:
            self.set_implicit_wait()

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

    def exists_and_visible(self, **kwargs):
        e = self.exists(**kwargs)

        if e and e.is_displayed():
            return e

        return False

####################################################################################
# PLAY / WATCH VIDEOS


    def watch_first_video_on_home(self):
        self.goto_home()
        self.click_on_first_video()

    def click_first_primetime_video(self, screenshot=False):
        """
        Scrolls down to Primetime section, then clicks the video right below the word "Primetime"
        """

        # Leave this here.  App was doing a weird thing were for a
        # split second "Primetime" existed, then it refreshed.
        self.exists(class_name='UIACollectionView', timeout=30)
        sleep(2)

        e = self.find_on_page('accessibility_id', 'Primetime Episodes')
        if screenshot:
            self.event.screenshot(self.screenshot())

        if not e:
            raise RuntimeError('Failed finding "Primetime Episodes" on page.')

        y = e.location['y']
        win_size = self.driver.get_window_size()['height']

        # if it's already onscreen and near the top, just tap below it
        if y < win_size * .75:
            self.tap(.15, e.location['y']+100)
        else:
            self.swipe_element_to_top_of_screen(e, endy=.4, startx=0)
            sleep(.5)

            if screenshot:
                self.event.screenshot(self.screenshot())

            self.tap(.15, .53)

        sleep(5)

    def click_on_first_video(self):
        # update_for_ios
        pass

    def click_info_icon(self):
        # update_for_ios
        pass

    def wait_for_video_to_start(self, buffer_wait=60):

        sleep(10)
        # start_time = time()
        # self.exists(id='com.cbs.app:id/player_activity_frame', timeout=buffer_wait)
        #
        # elapsed_time = time()-start_time
        # timeout = buffer_wait-elapsed_time
        #
        # # make sure we're not still spinning/buffering
        # ex = self.not_exists(id='com.cbs.app:id/loading', timeout=timeout)
        # self.assertTrueWithScreenShot(ex, screenshot=False, msg="Assert that video buffer spinner disappears")
        #
        # # DO WE NEED TO CHECK FOR ERROR POPUPS?
        # # DO WE NEED TO CHECK FOR ERROR POPUPS?
        # # DO WE NEED TO CHECK FOR ERROR POPUPS?
        #
        # # OK! The video is properly playing...

    def pause_video(self):
        # brings panel control up
        self.tap_by_touchaction(.25, .25)
        self.click(accessibility_id='UVPSkinPauseButton')
        # self.event.screenshot(self.screenshot())

    def unpause_video(self):
        self.click(accessibility_id='UVPSkinPlayButton')
        sleep(2)
        # self.event.screenshot(self.screenshot())

    def jump_in_video(self, jump_time):
        """
        We'll tap in the seek bar to jump over.  jump_time is in seconds.
        We'll find where to tap by dividing jump_time by total_time as found in the screen element
        """
        self.pause_video()
        total_time = self.driver.find_elements_by_class_name('UIAStaticText')[-1].text

        # total_time = minutes*60 + seconds
        total_time = float(total_time[-5:-3])*60 + float(total_time[-2:])

        seek_pct = jump_time / total_time

        seek_bar = self._find_element(class_name='UIASlider')

        # width * seek_pct is how far over in the bar to tap
        seek_bar_end_x = seek_bar.location['x'] + seek_bar.size['width'] * seek_pct

        # this is just the vertical middle of the seek bar
        seek_bar_end_y = seek_bar.location['y'] + seek_bar.size['height']/2

        seek_bar_start_x = seek_bar.location['x']

        while seek_bar_start_x < seek_bar_end_x:
            self.swipe(seek_bar_start_x, seek_bar_end_y, seek_bar_end_x, seek_bar_end_y, 500)
            seek_bar_start_x += 15
            print seek_bar_start_x

        self.unpause_video()

    def stop_video(self):
        try:
            self.click(id="Done", timeout=2)
        except WebDriverException:
            try:
                self.tap_by_touchaction(.25, .25)
                self.click(id="Done", timeout=5)
            except WebDriverException:
                e = self._find_element(id="Done")
                self.tap_by_touchaction(.25, .25)
                e.click()

####################################################################################
# REGISTRATION

################################################
# VALIDATE / VERIFY

    def verify_cbs_logo(self, special=None, screenshot=False):
        #cbs logo in upper left

        if special == 'video':
            id = 'cbsLogo'
            t_f = self.exists(accessibility_id=id)
        else:
            id1 = 'CBSEye_white'
            id2 = 'CBSLogo_white'
            t_f = self.exists(accessibility_id=id1, timeout=5) or \
                self.exists(accessibility_id=id2)

        self.assertTrueWithScreenShot(t_f, screenshot=screenshot, msg='Verifying CBS Logo exists')

    def verify_navigation_drawer_button(self, screenshot=False):
        # "verify menu icon"
        # "verify hamburger"
        self.verify_exists(id='Main Menu', screenshot=screenshot)

    def verify_navigation_back_button(self, screenshot=False):
        # "verify menu icon"
        # "verify hamburger"
        self.verify_exists(accessibility_id='Back', screenshot=screenshot)

    def verify_share_icon(self, screenshot=False):
        self.click_more()
        self.verify_exists(id='Share', screenshot=screenshot)
        if self.phone:
            self.click(id='Close')
        else:
            self.click_more()

    def verify_cancel_button(self, screenshot=False):
        self.verify_exists(id='Cancel', screenshot=screenshot)

    def verify_star_icon(self, screenshot=False):
        t_f = (self.exists(accessibility_id="MyCBSStarOutlined iPhone", timeout=10) or
               self.exists(accessibility_id="MyCBSStarOutlined iPad", timeout=5) or
               self.exists(accessibility_id="MyCBSStarFilled iPhone", timeout=0) or
               self.exists(accessibility_id="MyCBSStarFilled iPad", timeout=0))

        self.assertTrueWithScreenShot(t_f, screenshot=screenshot, msg="Should see 'favorite star'")

    def verify_search_icon(self, screenshot=False):
        self.verify_exists(xpath="//UIAButton[@name='Search']", screenshot=screenshot)

    def verify_search_field(self, screenshot=False):
        pass
        # todo: requested id in document
        # self.verify_exists(id='__search_textfield_id', screenshot=screenshot)

    def verify_keyboard(self, screenshot=False):
        self.assertTrueWithScreenShot(self.is_keyboard_displayed(), screenshot=screenshot, msg='Keyboard should be displayed')

    def verify_not_keyboard(self, screenshot=False):
        self.assertTrueWithScreenShot(not self.is_keyboard_displayed(), screenshot=screenshot, msg='Keyboard should NOT be displayed')

    def verify_search_show_card(self, screenshot=False):
        # todo: requested in document
        pass

    def verify_search_episode_count(self, screenshot=False):
        # there is 1 UIACollectionCell with craploads of invisible elements. name = 'page 1 of 21'
        # there is 1 UIACollectionCell with nothing in it. name = 'page 1 of 1'
        # there is 1 UIACollectionCell with 1 Cell with our staticText, this is the one we want. name = 'page 1 of 21'
        element = self.get_search_result_episode_count_element()
        self.assertTrueWithScreenShot(element, screenshot=screenshot, msg='Should see "X Episodes" text in search results')

    def verify_show_page_tabs(self, screenshot=False):
        return
        # IDs have been requested.  Nothing exists for these elements.
        self.verify_exists(accessibility_id='FULL EPISODES', screenshot=screenshot)
        self.verify_exists(accessibility_id='FREE')
        self.verify_exists(accessibility_id='CLIPS')

####################################################################################
# DEVELOPING / DEBUGGING METHODS

    def kill_ss(self):
        """
        For interactive session, turns off screenshot.
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


    # quick way to get page source.  In your interactive session, just do a self.src()
    def src(self, elem=None, tab_str='', full=False, recursing=False):

        import xml.etree.ElementTree

        self.src_skip = ['dom', 'hint', 'enabled', 'valid', 'path', 'y', 'x', 'height', 'width']

        if (not recursing):
            self.src_out_str = ''
            source = self.driver.page_source
            try:
                root = xml.etree.ElementTree.fromstring(source.encode('utf-8'))
            except Exception,e:
                print source
                print "\n\nxml.etree.ElementTree failed parsing source.  sorry."

            self.src(elem=root, tab_str='', full=full, recursing=True)
            print self.src_out_str
        else:
            self.src_out_str += '\n' + tab_str + elem.tag

            temp_hash = elem.attrib
            for key in temp_hash:
                if (not full and key in self.src_skip):
                    continue
                value = temp_hash[key]
                if (value == ''):
                    value = 'False'

                self.src_out_str += ", " + key + ": " + value

            for child in list(elem):
                self.src(elem=child, tab_str=tab_str + '  ', full=full, recursing=True)


    # QUICKER way to get page source - shows inline
    def qsrc(self, elem=None, tab_str='', full=False, recursing=False):
        self.qsrc_skip = ['dom', 'hint', 'enabled', 'valid', 'path']

        import xml.etree.ElementTree

        if (not recursing):
            self.qsrc_out_str = ''
            source = self.driver.page_source.encode('ascii', 'ignore')
            try:
                root = xml.etree.ElementTree.fromstring(source.encode('utf-8'))
            except Exception,e:
                print "\n\nxml.etree.ElementTree failed parsing source.  sorry."
                raise e

            self.qsrc(elem=root, tab_str='', full=full, recursing=True)
            print self.qsrc_out_str
        else:
            temp_str = str.ljust(str(elem.tag), 18)

            temp_hash = elem.attrib
            for key in temp_hash:
                if (not full and key in self.qsrc_skip):
                    continue
                value = temp_hash[key]
                if (value == ''):
                    value = 'False'
                if key == 'name':
                    tw = 30
                elif key == 'value':
                    tw = 18
                elif key == 'label':
                    tw = 18
                elif key == 'visible':
                    tw = 15
                else:
                    print "bad key: " + key

                temp_str += str.ljust(str(", " + key + ": " + value), tw)

            if len(temp_str) > 180:
                temp_str += "\n"

            self.qsrc_out_str += temp_str + "\n"

            for child in list(elem):
                self.qsrc(elem=child, tab_str=tab_str + '', full=full, recursing=True)


