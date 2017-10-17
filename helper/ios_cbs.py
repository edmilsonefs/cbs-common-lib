# TODO rename file to common_ios.py

import os
import random
import re
from time import sleep, time

import subprocess
from xml.etree import ElementTree


from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

from testlio.base import TestlioAutomationTest, SCREENSHOTS_DIR

class CommonIOSHelper(TestlioAutomationTest):
    phone = False
    tablet = False
    needToAccept = True
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
    already_accepted_terms = False
    passed = False
    element_type = '//UIA'  # iOS 9
    UIAWindow_XPATH = '//UIAApplication[1]/UIAWindow[1]'
    signed_out = False
    xcuitest = False

    def setup_method(self, method, caps=False):
        # subprocess.call("adb shell am start -n io.appium.settings/.Settings -e wifi off", shell=True)

        if not caps:
            super(CommonIOSHelper, self).setup_method(method, {'waitForAppScript': '$.delay(5000); $.acceptAlert();'})
        else:
            super(CommonIOSHelper, self).setup_method(method, caps=caps)

        if 'iPad' in self.driver.capabilities['deviceName']:
            self.tablet = True
            self.phone = False
        else:
            self.tablet = False
            self.phone = True
        if self.is_xcuitest():
            self.element_type = '//XCUIElementType' #iOS 10
            self.xcuitest = True

        # wait for the splash screen to disappear
        # self._accept_alert(1)
        self.not_exists(accessibility_id='SplashEyeLogo', timeout=60)
        # self._accept_alert(1)
        # self.safe_screenshot()
        # self.click_safe(xpath="//*[@name='OK']", timeout=60)
        # self.click_safe(id="START NOW", timeout=30)
        self.goto_home()
        # self.click_safe(xpath="//*[@name='OK' OR @name='Ok' OR @name='ok']", timeout=60)

    def teardown_method(self, method):
        if self.passed:
            self.event.start(data='Test completed successfully')
        else:
            self.event.start(data='Test failed. Getting screenshot and page_source.')
            if self.driver:
                try:
                    self.safe_screenshot()
                except Exception:
                    self.event.start(data='in teardown: screenshot failed')
                try:
                    self.driver.page_source
                except Exception:
                    self.event.start(data='in teardown: page source failed')

        self.event.stop()
        # sleep(60)

        try:
            self.driver.quit()
        except Exception:
            self.event.start(data='in teardown: driver.quit() failed')

        # sleep(80)
        sleep(20)

    ####################################################################################
    # SETUP/LOGIN METHODS

    def is_xcuitest(self):
        try:
            v = int(str(str(os.popen("xcodebuild -version").read()).split(" ")[1]).split(".")[0])
        except:
            return False
        return v > 7

    def login(self, username, password):
        """
        This assumes you are on the Sign In screen.
        """

        # username
        if self.phone:
            if self.xcuitest:
                user_elem = self._find_element(class_name='XCUIElementTypeTextField')
            else:
                user_elem = self._find_element(class_name='UIATextField')
        else:
            for e in self.driver.find_elements_by_xpath("//*[@value='Email']"):
                if e.is_displayed():
                    user_elem = e
                    break

        user_elem.click()
        self.send_keys(element=user_elem, data=username)

        # password
        if self.phone:
            if self.xcuitest:
                pwd_elem = self._find_element(class_name='XCUIElementTypeSecureTextField')
            else:
                pwd_elem = self._find_element(class_name='UIASecureTextField')
        else:
            for e in self.driver.find_elements_by_xpath("//*[@value='Password']"):
                if e.is_displayed():
                    pwd_elem = e
                    break

        pwd_elem.click()
        self.send_keys(element=pwd_elem, data=password)

        # sign in button
        if self.phone:
            if self.xcuitest:
                sign_in_button = self._find_element(accessibility_id='SIGN IN')
            else:
                sign_in_button = self._find_element(xpath="//*[@name='SIGN IN']")
        else:
            for e in self.driver.find_elements_by_xpath("//*[@name='SIGN IN']"):
                if e.is_displayed():
                    sign_in_button = e
                    break

        sleep(3)
        sign_in_button.click()

        self.finish_login()

        # self.goto_settings()
        # self.assertTrueWithScreenShot(self.exists(accessibility_id='Sign Out', timeout=0),
        #                               screenshot=True,
        #                               msg="Verify 'Sign Out' button on Settings page.")

    def logout(self, safe=False):
        self.goto_settings()
        if safe:
            self.click_safe(id='Sign Out', timeout=6)
        else:
            self.click(id='Sign Out')

    ####################################################################################
    # MENU
    def goto_home(self):
        self.open_drawer()
        self.click(id='Home')

    def goto_shows(self):
        self.open_drawer()
        self.click(id='Shows')

    def goto_live_tv(self):
        self.open_drawer()
        #self.click(xpath="//*[@name='Live TV']")
        self.click(accessibility_id='Live TV')
        self._accept_alert(2)

    def goto_schedule(self):
        self.open_drawer()
        self.click(id='Schedule')

    def goto_settings(self):
        self.open_drawer()
        self.click(accessibility_id='Settings')
        #self.click(xpath="//*[@name='Settings']")

    def goto_movies(self):
        self.open_drawer()
        self.click(id='Movies')

    def goto_subscribe(self):
        self.open_drawer()
        self.click(id='Subscribe')

    def goto_show(self, show_name):
        self.search_for(show_name)
        self.safe_screenshot()
        self.hide_keyboard()
        sleep(5)
        self.click_first_search_result()
        sleep(10) #wait for page is loaded
        # t_f = self.exists(xpath="//*[contains(@name,'MyCBSStar')]", timeout=30)
        # self.assertTrueWithScreenShot(t_f, msg="The individual show page should be loaded at least in 30 seconds", screenshot=True)

    def goto_show_with_extended_search(self, show_name):
        self.search_for_extended(show_name)
        self.safe_screenshot()
        self.click_first_search_result()
        # if self.xcuitest:
        #     if self.phone:
        #         try:
        #             t_f = self.exists(accessibility_id='MyCBSStarOutlined iPhone', timeout=10)
        #         except:
        #             t_f = self.exists(accessibility_id='MyCBSStarFilled iPhone', timeout=10)
        #     else:
        #         try:
        #             t_f = self.exists(accessibility_id='MyCBSStarOutlined iPad', timeout=10)
        #         except:
        #             t_f = self.exists(accessibility_id='MyCBSStarFilled iPad', timeout=10)
        # else:
        t_f = self.exists(xpath="//*[contains(@name,'MyCBSStar')]", timeout=30)

        #Commented until cbs star won't be visible to appium
        #self.assertTrueWithScreenShot(t_f, msg="Assert we're on individual show page", screenshot=True)

    def goto_sign_in(self):
        self.open_drawer()
        #elems = self.driver.find_elements_by_xpath("//*[@name='Sign In']")
        elems = self.driver.find_elements_by_accessibility_id('Sign In')
        self.click(element=elems[0])

    def sign_out(self):
        # self.execute_script('target.frontMostApp().mainWindow().tableViews()[0].cells()["Sign Out"].tap()')
        # self.click(element=self.find_by_uiautomation('target.frontMostApp().mainWindow().tableViews()[0].cells()["Sign Out"]'))
        #self.click(xpath="//*[@name='Sign Out']")
        if self.click_safe(accessibility_id='Sign Out', timeout=5):
            self.signed_out = True

    def goto_sign_out(self, sign_out=True):
        self.goto_settings()
        if sign_out:
            self.sign_out()
            self.goto_home()

    def goto_sign_up(self):
        self.goto_sign_in()
        self.click(id='Sign Up')

    # def go_to_show(self, show_name):
    #     self.goto_show(show_name)
    #     # self.go_to_shows()
    #     # self.click(element=self.get_clickable_element(id="Search", timeout=30))
    #     # sleep(3)
    #     # self.send_text_native(show_name)
    #     # self.driver.tap([(80, 170)])
    #     # # self.close_big_advertisement()

    ####################################################################################
    # SEARCH
    def select_sign_in_checkbox(self):
        self.tap_element(xpath="//" + self.element_prefix() + "ScrollView[.//" + self.element_prefix() + "Button[@name='CONTINUE']]//" + self.element_prefix() + "Button[not(@name)]")

    def enter_search_text(self, what_to_search_for):
        e = self.find_search_text()
        self.send_keys(element=e, data=what_to_search_for)

    def enter_search_text_extended(self, what_to_search_for):
        if self.xcuitest:
            #TODO add back the logic of checking if only one show is available.
            e = self.find_search_text()
            for i in range(0, len(what_to_search_for)):
                self.send_keys(element=e, data=what_to_search_for[i])
                if i > 15:
                    break

            if self.exists(element=self.get_element(id="No Shows Found", timeout=2)):
                self.assertTrueWithScreenShot(False, msg="No show '" + what_to_search_for + "' found", screenshot=True)
        else:
            count = 0
            e = self.find_search_text()
            for i in range(0, len(what_to_search_for)):
                self.send_keys(element=e, data=what_to_search_for[i])
                if count >= 2:
                    if self.exists(element=self.get_element(id="No Shows Found", timeout=5)):
                        self.assertTrueWithScreenShot(False, msg="No show '" + what_to_search_for + "' found", screenshot=True)
                    if len(self.get_elements(xpath="//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell")) == 1:
                        break
                count += 1

    def search_for(self, what_to_search_for):
        self.click_search_icon()
        self.enter_search_text(what_to_search_for)
        self.hide_keyboard()

    def search_for_extended(self, what_to_search_for): # method to search by typing symbol by symbol
        self.click_search_icon()
        self.enter_search_text_extended(what_to_search_for)

    def click_first_search_result(self):
        if self.xcuitest:
            self.tap(.25, .25)
        else:
            element = self.get_search_result_episode_count_element()
            element.click()

    ####################################################################################
    # HEADER
    def header_back_button(self):
        self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
        sleep(2)

    def click_search_icon(self):
        try:
            self.click(accessibility_id='Search')
            #self.click(xpath="//*[@name='Search']")
        except:
            self.close_drawer()
            self.click(accessibility_id='Search')
#            self.click(xpath="//*[@name='Search']")

    def click_search_text(self):
        self.find_search_text().click()

    def clear_search(self):
        e = self.find_search_text()
        self.clear_text_field(e, 'Search')

    def click_search_back(self):
        #self.driver.find_elements_by_xpath("//UIAButton[@name='Cancel']")[-1].click()
        self.driver.find_element_by_accessibility_id('Cancel').click()

    def back(self):
        try:
            ta = TouchAction(self.driver)
            ta.press(x=25, y=25).release().perform()
            self.log_info("Press back")
        except:
            self.log_info("Fail to press back")

    def go_back(self):
        try:
            elem = self.exists(id='BackArrow_white', timeout=10)
            if not elem:
                try:
                    if self.phone:
                        elem = self.get_element(xpath="//*[@name='Back']", timeout=10)
                    else:
                        elem = self.get_element(xpath="//*[@name='Back ']", timeout=10)
                except:
                    pass


            if self.xcuitest:
                elem.click() # add, if below element loc click is removed.
            else:

            # stupid bug where the < button is offscreen, but the hamburger is in its place (but invisible, so we
            # use click_by_location)
                loc = elem.location
                if loc['x'] < 0 or loc['y'] < 0:
                    elem = self._find_element(id='Main Menu')
                    self.click_by_location(elem, side='middle')
                else:
                    elem.click()
        except:
            pass

    def _open_drawer(self):
        number_of_tries = 0
        while not self.exists_and_visible(id='Main Menu', timeout=7):
            number_of_tries += 1
            if number_of_tries == 5:
                break

            self.back()
            self.tap(3, 3)
            sleep(1)

        e = self.exists_and_visible(id='Main Menu', timeout=6)

        if e and e.location['x'] > 80:
            return

        if e:
            e.click()
        else:
            self.tap(3, 3)
            self.go_back()
            sleep(1)
            self.click(id='Main Menu')

    def open_drawer(self, native=False):
        self._open_drawer()

    def open_drawer_ios(self):
        self._open_drawer()

    def close_drawer(self):
        e = self.exists_and_visible(id='Main Menu')

        if e and e.location['x'] < 80:
            return

        if e:
            e.click()
        else:
            self.go_back()
            sleep(1)
            self.click(id='Main Menu')

    ####################################################################################
    # SHOW PAGE
    def get_table_with_show_episodes(self):
        return self.get_element(xpath="//XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell[1]")

    def click_first_show_page_episode(self):
        more_info_icon = self.get_elements(id='More Info')
        x = more_info_icon[0].location['x']
        y = more_info_icon[0].location['y']

        self.tap(x - 20, y - 20)

    def click_info_icon_on_found_on_show_page(self, show_elem):
        self.click_show_info_icon()

    def click_show_info_icon(self):
        more_info_icon = self.get_elements(id='More Info')
        self.click(element=more_info_icon[0])

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

    def verify_exists_video_element(self, **kwargs):
        if not self.exists(**kwargs):
            self.tap(0.5, 0.5)
            self.verify_exists(**kwargs)

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

    def verify_cbs_logo_using_xml(self, root=False, screenshot=False):
        """
        Verifies cbs logo, but using raw xml, not Appium methods.
        Sometimes these methods don't work.  See section header (XML Methods) for details.
        """
        el = self._exists_element_using_xml(root, find_by='id', find_key='CBSLogo_white')

        # you apparently can't test true/false using a xml.etree.ElementTree.Element
        if not (el == False):
            el = True

        self.assertTrueWithScreenShot(el, screenshot=screenshot, msg="Should see CBS logo")

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
            if args[0] in ['class_name', 'id', 'xpath']:
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

    def get_hack_season_name(self, exception_hack):
        if exception_hack == 'AFTER SHOW':
            # for Big Brother After Show, there is no season, it just says "After Show"
            season_name = 'AFTER SHOW'
        elif exception_hack == 'Specials':
            # for specials, there's only one episode, or only one row of episodes anyway
            show_elem = self._find_element(id=self.com_cbs_app + ":id/showName")
            return show_elem
        elif exception_hack == '60 Minutes':
            season_name = "Latest Full Episodes"
        else:
            raise NameError('Given hack is not handled')

        return season_name

    def find_episode_on_show_page(self, show_dict, exception_hack=False):
        try:
            int(show_dict['season_number'])
        except:
            raise ValueError('Season number needs to be numeric')

        try:
            int(show_dict['episode_number'])
        except:
            raise ValueError('Episode number needs to be numeric')

        episode_title = 'S%s Ep%s' % (show_dict['season_number'], show_dict['episode_number'])

        if exception_hack:
            season_name = self.get_hack_season_name(exception_hack)
        else:
            season_name = "Season " + str(show_dict['season_number'])

        #no need in this hack currently
#        if show_dict['show_title'] == 'Big Brother':
#            action = TouchAction(self.driver)
#            window_sizes = self.driver.get_window_size()
#            height = window_sizes['height']
#            width = window_sizes['width']
#
#            #7 Plus
#            if width == 414 and height == 736:
#                action.press(x=200, y=300).release().perform()
#            #SE
#            elif width == 320 and height == 568:
#                action.press(x=200, y=220).release().perform()
#            #7
#            elif width ==375 and height == 667:
#                action.press(x=200, y=270).release().perform()
#            #ipad 9.7
#            elif width == 768 and height == 1024:
#                action.press(x=300, y=400).release().perform()
#            #ipad 12.9
#            elif width == 1024 and height == 1366:
#                action.press(x=300, y=400).release().perform()

        # //UIATableView[1]/UIATableCell[1]/UIACollectionView[1]/UIACollectionCell
        season_elem = self.find_on_page('accessibility_id', season_name)
        self.assertTrueWithScreenShot(season_elem, screenshot=True, msg="Assert our season exists: %s" % season_name)
        #self.swipe_element_to_top_of_screen(season_elem, endy=.25, startx=20)

        # may help get the position correctly
        sleep(2)

        show_elem = self.find_on_page_horizontal(episode_title)
        self.assertTrueWithScreenShot(show_elem, screenshot=True, msg="Assert our show exists: %s" % episode_title)

        return show_elem

    ####################################################################################
    # VIDEO PLAYER

    def restart_from_the_beggining(self):
        self.click_safe(id='Restart From Beginning', timeout=6)

    def close_video(self):
        count = 0
        while count < 10:
            if self.exists(id="Search", timeout=6) and self.exists(id="Search", timeout=6).is_displayed():
                break
            else:
                self.video_done_button()
                count += 1

    def video_done_button(self):
        self.safe_screenshot()
        try:
            ta = TouchAction(self.driver)
            ta.press(x=100, y=100).release().perform()
        except:
            pass
        self.safe_screenshot()
        try:
            self.click(id="Done", timeout=6)
        except:
            try:
                ta = TouchAction(self.driver)
                ta.press(x=100, y=100).release().perform()
            except:
                pass
            self.click_safe(id="Done", timeout=6)
        self.log_info("End of stream")
        self.safe_screenshot()

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

    def pause_video(self):
        # brings panel control up
        try:
#            self.tap_by_touchaction(.5, .5)
            self.click(element=self.get_element(id='UVPSkinPauseButton', timeout=1))
        except:
            try:
                self.tap_by_touchaction(.5, .5)
                self.click(element=self.get_element(id='UVPSkinPauseButton', timeout=10))
            except:
                pass

    def unpause_video(self):
        try:
            self.click(element=self.get_element(id='UVPSkinPlayButton', timeout=1))
        except:
            try:
                self.tap_by_touchaction(.5, .5)
                self.click(element=self.get_element(id='UVPSkinPlayButton', timeout=10))
                sleep(2)
            except:
                pass

    def jump_in_video(self, jump_time):
        """
        We'll tap in the seek bar to jump over.  jump_time is in seconds.
        We'll find where to tap by dividing jump_time by total_time as found in the screen element
        """
        self.pause_video()
        current_time = self.driver.find_element_by_xpath('//XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText[1]')
        current_time_text = current_time.text
        remaining_time = self.driver.find_element_by_xpath('//XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText[2]')
        remaining_time_text = remaining_time.text

        # total_time = minutes*60 + seconds
        remaining_time_seconds = float(remaining_time_text[-5:-3])*60 + float(remaining_time_text[-2:])
        current_time_seconds = float(current_time_text[-5:-3])*60 + float(current_time_text[-2:])
        total_time_seconds = remaining_time_seconds + current_time_seconds

        # it is too precise. Maybe add some second to jump_time
        seek_point = jump_time / total_time_seconds + 0.1


        seek_bar = self._find_element(class_name='XCUIElementTypeSlider')
        seek_bar.set_value(str(seek_point))

        #hopefully we won't need code below, it is not working anyways
#        seek_bar_size = seek_bar.size['width'] - current_time.size['width'] - remaining_time.size['width']
#        seek_bar_percentage = float(float(str(seek_bar.get_attribute("value"))[:-1]) / 100)
#
#        # width * seek_pct is how far over in the bar to tap
#        seek_bar_end_x = seek_bar.location['x'] + (seek_bar.size['width'] * seek_pct) - remaining_time.size['width']
#
#        # this is just the vertical middle of the seek bar
#        seek_bar_end_y = seek_bar.location['y'] + seek_bar.size['height']/2
#
#        seek_bar_start_x = seek_bar.location['x'] + current_time.size['width'] + (seek_bar_size * seek_bar_percentage)
#
#        while seek_bar_start_x < seek_bar_end_x:
#            self.swipe(seek_bar_start_x, seek_bar_end_y, seek_bar_end_x, seek_bar_end_y, 2000)
#            seek_bar_start_x += 15
#            print seek_bar_start_x

        #unpause explicitly if needed
        self.unpause_video()

    def find_by_uiautomation(self, value, hide_keyboard=False):
        return self.driver.find_element_by_ios_uiautomation(value)

    def set_implicit_wait(self, wait_time=-1):
        """
        wrapper that sets implicit wait, defualts to self.default_implicit_wait
        """
        if wait_time == -1:
            wait_time = self.default_implicit_wait

        self.driver.implicitly_wait(wait_time)

    def _choose_y_coordinate(self, ad):
        """
        Returns y coordinate located not in the ad area
        """
        s_height = self.driver.get_window_size()['height']
        ad_y_start = ad.location['y']
        ad_y_end = ad_y_start + ad.size['height']

        if ad_y_end + 10 > s_height:
            y = ad_y_start - 10
        else:
            y = ad_y_end + 10

        return y

    def _smart_scroll_down(self):
        """
        Scrolls down while evading ads
        """
        ads = self.driver.find_elements_by_class_name('XCUIElementTypeLink')
        displayed_ads = [x for x in ads if x.is_displayed()]
        x_cord = 0.5
        if len(displayed_ads) > 0:
            ad = displayed_ads[len(displayed_ads)-1]
            new_y = self._choose_y_coordinate(ad)
            self.swipe(x_cord, new_y, x_cord, -0.7, 1500)
        else:
            self.swipe(x_cord, .9, x_cord, -0.7, 1500)


    def find_on_page(self, find_by, find_key, max_swipes=10, x=.5):
        """
        Scrolls down the page looking for an element.  Call the method like this:
        self.find_on_page('name', 'Settings')
        self.find_on_page('id', 'com.cbs.app:id/seasonEpisode')
        """
        self.set_implicit_wait(3)
        device_size = self.driver.get_window_size()

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
                    device_height = device_size['height']
                    device_width = device_size['width']
                    pointX = device_width/4
                    fromY = device_height - 100 #need to check with various devices
                    self.driver.swipe(pointX, fromY, pointX, -device_height/4, 1500)
                else:
                    self._smart_scroll_down()
                pass

        self.set_implicit_wait()
        return False

    def send_text_native(self, value):
        self.driver.execute_script(
            'var vKeyboard = target.frontMostApp().keyboard(); vKeyboard.setInterKeyDelay(0.1); vKeyboard.typeString("%s");' % value)


    # def verify_exists_and_visible(self, **kwargs):
    #     screenshot = kwargs.get('screenshot')
    #
    #     if 'accessibility_id' in kwargs:
    #         selector = kwargs['accessibility_id']
    #     elif 'class_name' in kwargs:
    #         selector = kwargs['class_name']
    #     elif 'id' in kwargs:
    #         selector = kwargs['id']
    #     elif 'xpath' in kwargs:
    #         selector = kwargs['xpath']
    #
    #     elem = self.exists(**kwargs)
    #     if elem:
    #         t_f = elem.is_displayed()
    #
    #     self.assertTrueWithScreenShot(t_f, screenshot=screenshot,
    #                                   msg="Should see element with text or selector: '%s'" % selector)

    def _accept_alert(self, count):
        action = False
        for x in range(0, count):
            try:
                # Accepts terms of service & other popups there may be
                self.wait_and_accept_alert(timeout=5)
                sleep(2)
                action = True
                break
            except:
                action = False
        return action

    def _dismiss_alert(self, count):
        action = False
        for x in range(0, count):
            try:
                # Accepts terms of service & other popups there may be
                self.wait_and_dismiss_alert(timeout=10)
                sleep(5)
                action = True
                break
            except:
                action = False
        return action

    ####################################################################################
    # LOW LEVEL METHODS

    def execute_script(self, script):
        """
        send javascript directly, for example see _accept_terms_popup()
        """
        sleep(5)
        self.driver.execute_script('var target = UIATarget.localTarget();')
        self.driver.execute_script(script)

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

        try:
            self.driver.swipe(startx, starty, endx, endy, swipe_time)
        except:
            self.log_info("Swipe is failing")

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
        screen_size = self.driver.get_window_size()
        if self.tablet:
            if kwargs['side'] == 'middle':
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'left':
                x = loc['x'] + size['width'] / 4
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'right':
                x = loc['x'] + size['width'] - 50
                y = loc['y'] + 10
            else:
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

        elif self.phone:
            if kwargs['side'] == 'middle':
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'left':
                x = loc['x'] + size['width'] / 4
                y = loc['y'] + size['height'] / 2

            elif kwargs['side'] == 'right':
                x = screen_size['width'] - 40
                y = loc['y'] + 5
            else:
                x = loc['x'] + size['width'] / 2
                y = loc['y'] + size['height'] / 2

        # an array of tuples
        action = TouchAction(self.driver)
        action.tap(x=x, y=y).perform()

    def click_movies_episode_on_home_page(self):
        window_size_height = self.driver.get_window_size()["height"]
        count = 0
        while not self.is_element_visible(self.exists(id='Movies', timeout=6)) and count < 70:
            self.swipe_down(1, (400 if self.tablet else 200))
            count += 1

        count = 0
        if self.is_element_visible(self.exists(id='Movies', timeout=6)):
            movies = self.exists(id='Movies', timeout=6)
            while movies.location['y'] + movies.size['height'] > window_size_height / (2 if self.phone else 3) and count < 70:
                self.swipe_down(1, (400 if self.tablet else 100))
                count += 1
                movies = self.exists(id='Movies', timeout=6)

        self.assertTrueWithScreenShot(self.exists(id='Movies', timeout=6).is_displayed(), screenshot=True, msg='Movies Posters should be presented')

        movies = self.exists(id='Movies', timeout=6)

        count = 0
        while movies.location['y'] + movies.size['height'] > window_size_height / (2 if self.phone else 3) and count < 10:
            self.swipe_down(count=1, distance=50)
            count += 1

        self.safe_screenshot()
        label = self.get_element(id="Movies")
        x = label.location['x']
        y = label.location['y']
        self.tap(x + 50, y + label.size['height'] + 40)
        self.safe_screenshot()
        self.accept_video_popup()
        self.safe_screenshot()

    def accept_video_popup(self):
        self.click_safe(id='ACCEPT', timeout=10)
        self.click_safe(id='Accept', timeout=10)

    def click_watch_movie(self):
        self.click(id="Watch Movie", timeout=7)

    def click_watch_trailer(self):
        self.click(id="Preview Trailer", timeout=7)
        self.accept_video_popup()

    def click_subscribe_to_watch(self):
        self.click(id="Subscribe to Watch", timeout=7)
        self.accept_video_popup()

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

    def wait_until_element_is_visible(self, element_css=None, element_id=None, element_xpath=None):

        count = 0
        while count <= 10:
            self.driver.implicitly_wait(20)
            try:
                if element_css:
                    self.driver.find_elements_by_class_name(element_css)
                    break
                if element_id:
                    self.driver.find_element_by_id(element_id)
                    break
                if element_xpath:
                    self.driver.find_element_by_xpath(element_xpath)
            except:
                pass
            count += 1

    ####################################################################################
    # GET WRAPPERS

    def _isIntInStr(self, item):

        episode = ' Episodes'
        clip = ' Clip' 
        index = -1
        if episode in item:
            index = item.find(episode)
        else:
            index = item.find(clip)

        target = item[0: index]
        return target.isdigit()

    def get_show_cards(self):

        episode = ' Episodes'
        clip = ' Clip'

        static_text_elements = self.driver.find_elements_by_class_name('XCUIElementTypeStaticText')
        static_texts = [x.text for x in static_text_elements if x.text is not None]
        show_cards = [x for x in static_texts if episode in x or clip in x]

        #Currently we can see also primetime episodes, etc in page source.
        show_cards = [x for x in show_cards if self._isIntInStr(x)]

        return show_cards

    def get_search_result_episode_count_element(self):

        if self.xcuitest:
            target_cell = self.driver.find_element_by_xpath('//XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell')

            static_text = target_cell.find_element_by_class_name('XCUIElementTypeStaticText')
            if ' Episode' in static_text.text:
                return static_text
        else:
            collection_views = self.driver.find_elements_by_xpath("//*[@value='page 1 of 1']")

            for cell in collection_views:
                static_texts = cell.find_elements_by_class_name('UIAStaticText')
                for static_text in static_texts:
                    if ' Episode' in static_text.text:
                        return static_text

    ####################################################################################
    # SWIPE / TAP / CLICK / SEND_KEYS

    def swipe_el_to_top_of_screen(self, elem, endy=None, startx=-20, time=1500):
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

        self.swipe(startx, starty, startx, endy, time)

    def hide_keyboard(self):
        self.tap(0.95, 0.95)

    def close_big_advertisement(self):
        if self.tablet:
            self.click_safe(id='Close Advertisement', timeout=6)

    def click_episode_indicator(self):
        self.click(element=self.get_element(xpath="//XCUIElementTypeStaticText[contains(@name,'Full Episodes:')]"))

    def back_while_open_drawer_is_visible(self):
        counter = 0
        try:
            self.driver.implicitly_wait(10)
        except:
            pass
        while counter < 10:
            #TODO AllAccess logo is not used anymore. Unified for all users.
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


    ####################################################################################
    # HOME PAGE

    def click_first_primetime_video(self, screenshot=False):
        """
        Scrolls down to Primetime section, then clicks the video right below the word "Primetime"
        """

        # Leave this here.  App was doing a weird thing were for a
        # split second "Primetime" existed, then it refreshed.
        # self.exists(class_name='UIACollectionView', timeout=30)
        sleep(10)

        e = self.find_on_page('accessibility_id', 'Primetime Episodes')
        if screenshot:
            self.safe_screenshot()

        if not e:
            raise RuntimeError('Failed finding "Primetime Episodes" on page.')

        y = e.location['y']
        win_size = self.driver.get_window_size()['height']

        # if it's already onscreen and near the top, just tap below it
        if y < win_size * .75:
            self.tap(.15, e.location['y']+100)
        else:
            self.swipe_el_to_top_of_screen(e, endy=.4, startx=0)
            sleep(.5)

            if screenshot:
                self.safe_screenshot()

            self.tap(.15, .53)

        sleep(5)

    def click_movies_poster(self):
        sleep(2)
        self.tap(0.2, 0.2)

    def click_my_cbs_star(self):
        element = self.exists(xpath="//*[contains(@name,'MyCBSStar')]")
        self.click(element=element)
        self._dismiss_alert(1)
        return element.get_attribute("name")

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

        category_elem = self.find_on_page('accessibility_id', show_category)
        self.assertTrueWithScreenShot(category_elem, screenshot=True, msg="Assert '" + show_category + "' category exists")
        y_orig = category_elem.location['y']

        # self.swipe_element_to_top_of_screen(category_elem, endy=.25, startx=20)

        # For some stupid reason, it over-swipes sometimes.  Make sure it's still on the screen
        self.driver.page_source
        category_elem = self.exists(id=show_dict['show_category'], timeout=2)
        screen_height = self.driver.get_window_size()["height"]
        if not category_elem or category_elem.location['y'] < screen_height * .12:
            self.swipe(.5, 0.5, .5, -0.2, 1500)
        sleep(2)
        self.driver.page_source

        # find it again to be sure we get the right positioning
        category_elem = self._find_element(id=show_category)
        y = category_elem.location['y'] + category_elem.size['height'] - 20

        # swipe left to right to reset to the beginning of the list
        for i in range(2):
            self.swipe(0.4, y, 0.7, y, 2000)
            sleep(1)

        season_ep = 'S%s Ep%s' % (show_dict['season_number'], show_dict['episode_number'])

        # We have to try multiple times just in case we see a "S3 Ep4" (for example) from a different show.
        # Should be extremely rare.
        season_ep_elem = self.find_on_page_horizontal(season_ep)
        # The rare case that we see an elem with the right season and episode numbers, but it's the wrong show.
        # Swipe it off the screen and try again...
        if not season_ep_elem:
            self.safe_screenshot()
            self.swipe_element_to_top_of_screen(category_elem, endy=.25, startx=20)
            season_ep_elem = self.find_on_page_horizontal(season_ep)
            if not season_ep_elem:
                self.safe_screenshot()
                self.swipe(0.4, y, 0.1, y, 1500)
                season_ep_elem = self.find_on_page_horizontal(season_ep)

        self.assertTrueWithScreenShot(season_ep_elem, screenshot=True,
                                      msg="Assert our season/episode exists: %s" % season_ep)

        return season_ep_elem

    ################################################
    # VALIDATE / VERIFY
    def verify_exists_in_xml(self, text, screenshot):
        if type(text) is list:
            self.assertTrueWithScreenShot(any(x not in self.driver.page_source for x in text), screenshot=screenshot,
                                          msg="One of the elements with text '%s' is absent" % text)
        else:
            self.assertTrueWithScreenShot(text in self.driver.page_source, screenshot=screenshot,
                                          msg="The element with text '%s' is absent" % text)

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

    def exists_and_visible(self, **kwargs):
        e = self.exists(**kwargs)

        if e and e.is_displayed():
            return e

        return False

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
        #self.verify_exists(xpath='//*[@name="Share"]', screenshot=screenshot)
        self.verify_exists(accessibility_id='Share', screenshot=screenshot)
        if self.phone:
            self.click(id='Close')
        else:
            if self.xcuitest:
                self.click(xpath='//*[@name="PopoverDismissRegion"]')
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
        self.verify_exists(accessibility_id='Search', screenshot=screenshot)
#        self.verify_exists(xpath="//UIAButton[@name='Search']", screenshot=screenshot)

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

    def verify_show_cards_exist(self, screenshot=False):
        show_cards = self.get_show_cards()
        show_cards_count = len(show_cards)
        self.verify_not_equal(show_cards_count, 0, screenshot)

    def verify_show_episode_indicator(self, screenshot=False):
        text_cells = self.driver.find_elements_by_class_name('XCUIElementTypeStaticText')
        indicator = None
        for cell in text_cells:
            if cell.text is not None:
                if 'Full Episodes' in cell.text and 'Free' in cell.text and 'With CBS All Access' in cell.text:
                    indicator = cell
                    break
        self.assertTrueWithScreenShot(indicator, screenshot=screenshot, msg='Should see episode indicator')


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
        if self.xcuitest: #iOS 10
            return self.exists(class_name='XCUIElementTypeKeyboard', timeout=2)
        else:
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


    def change_to_landscape(self):
        self.driver.orientation = 'LANDSCAPE'

    def change_to_portrait(self):
        self.driver.orientation = 'PORTRAIT'

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

    def element_prefix(self):
        if self.xcuitest:
            return 'XCUIElementType'
        else:
            return 'UIA'

    ####################################################################################
    # FIND / EXISTS

    def find_search_text(self):
        if self.exists(id='Search for a Show', timeout=2):
            return self._find_element(id='Search for a Show')
        else:
            return self.driver.find_elements_by_class_name('UIATextField')[-1]

    def find_on_page_horizontal(self, find_value):
        find_value_converted = ""
        if bool(re.search("S\d+ Ep\d+", find_value)):
            find_value_converted = find_value.replace("S", "Season ")
            find_value_converted = find_value_converted.replace("Ep", "Episode ")
        else:
            if "/" in find_value:

                find_value_episode = find_value.split("/")[0]
                find_value_season = find_value.split("/")[1]

                find_value_episode = find_value_episode if len(find_value_episode) > 1 else "0" + find_value_episode

                find_value = "Ep" + find_value_episode + find_value_season
                find_value = find_value.split(":")[0]

        #self.set_implicit_wait(30)
        if self.xcuitest:
            return self.get_element(xpath="//*[contains(@name,'" + find_value + "') or contains(@name,'" + find_value_converted + "')][1]", timeout=60)
        else:
            return self.get_element(xpath="//UIACollectionCell[contains(@name,'" + find_value + "') or contains(@name,'" + find_value_converted + "')][1]", timeout=60)

    def tap_element(self, **kwargs):
        elem = self.exists(**kwargs)
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

    def screenshot(self):
        sleep(1)  # wait for animations to complete before taking a screenshot
        import time

        try:
            path = "{dir}/{name}-{time}.png".format(dir=SCREENSHOTS_DIR, name=self.name, time=time.mktime(time.gmtime()))

            if not os.environ['IOS_UDID'] and not os.environ['UDID']:
                raise Exception('screenshot failed. IOS_UDID not provided')

            if os.environ['IOS_UDID']:
                subprocess.call("echo $IOS_UDID &> consoleoutput.txt", shell=True)
                subprocess.call("idevicescreenshot -u $IOS_UDID \"" + path + "\" &> consoleoutput2.txt", shell=True)
            else:
                subprocess.call("echo $UDID &> consoleoutput.txt", shell=True)
                subprocess.call("idevicescreenshot -u $UDID \"" + path + "\" &> consoleoutput2.txt", shell=True)

            return path
        except:
            return False

    def safe_screenshot(self):
        try:
            self.event.screenshot(self.screenshot())
        except:
            pass

    def log_info(self, info):
        self.event._log_info(self.event._event_data(info))

    def click_facebook_icon(self):
        self.click(id='FacebookLogo')

    ####################################################################################
    # LOGIN
    def set_sign_in_email(self, email):
        elem = self.get_element(xpath='//XCUIElementTypeTextField[1]')
        elem.clear()
        self.send_text(element=elem, data=email)
        self.hide_keyboard()

    def set_sign_in_password(self, password):
        elem = self.get_element(xpath='//XCUIElementTypeSecureTextField[1]')
        elem.clear()
        self.send_text(element=elem, data=password)
        self.hide_keyboard()

    def login_(self, email, password):
        self.set_sign_in_email(email)
        self.set_sign_in_password(password)

        self.click(accessibility_id='SIGN IN')

        self.finish_login()

    def finish_login(self):
        # Complete registration if required

        self.driver.implicitly_wait(10)
        if self.exists(id='CONTINUE', timeout=10):
            if self.xcuitest:    #iOS 10 switch
                self.tap_element(xpath="//XCUIElementTypeButton[not(@name)]")
                sleep(3)
            try:
                if self.xcuitest:
                    self.tap_element(xpath="//*[./*[@name='CONTINUE']]//*[1]")
                else:
                    self.tap_element(xpath="//UIAScrollView[./UIAButton[@name='CONTINUE']]//UIAButton[1]")
                self.click(accessibility_id='CONTINUE')
                sleep(3)
            except:
                try:
                    self.driver.find_element_by_id(accessibility_id='CONTINUE', timeout=5)
                except:
                    if self.xcuitest:
                        self.tap_element(xpath="//*[./*[@name='CONTINUE']]//*[1]")
                    else:
                        self.tap_element(xpath="//UIAScrollView[./UIAButton[@name='CONTINUE']]//UIAButton[1]")
                    self.click(accessibility_id='CONTINUE')
                    sleep(3)
                self.safe_screenshot()
            self.driver.implicitly_wait(30)

    def sign_in_facebook(self, username, password, finish_login=False):
        try:
            self.click(xpath="//UIAButton[@name='Continue']")
        except:
            email_field = self._find_element(xpath=self.element_type + "TextField")
            self.send_text(data=username, element=email_field)

            password_field = self._find_element(
                xpath=self.element_type + "SecureTextField[@value='Facebook Password']")
            self.send_text(data=password, element=password_field)

            self.click(xpath=self.element_type + "Button[@name='Log In']")
            self.event.screenshot(self.screenshot())

            self.click(xpath=self.element_type + "Button[@name='Continue']")
            self.event.screenshot(self.screenshot())
        if finish_login:
            self.finish_login()
        self.event.screenshot(self.screenshot())

    ####################################################################################
    # CLICK WRAPPERS

    def click_return(self):
        self.tap(0.95, 0.95)

    def click_more(self):
        self.click(id='More Information')

    def click_close_cta(self):
        self.click(id='upsell close')

    def click_close_movies_popup(self):
        self.click_safe(id='Close')


    ####################################################################################
    # SWIPE
    def swipe_element_to_top_of_screen(self, elem=None, endy=None, startx=-20):
        """
        Swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        loc = elem.location
        startx = loc['x'] + startx
        starty = loc['y']

        # in case it's behind the banner ad at the bottom, swipe up a little
        window_height = self.driver.get_window_size()['height']
        if starty > .8 * window_height:
            self.swipe(.5, .5, .5, 0.3, 1500)
            starty = starty - window_height * .2
            sleep(1)

        if not endy:
            if self.phone:
                endy = 70
            else:
                endy = 180

        self.swipe(startx, starty, startx, endy, 1500)

    def swipe_element_to_bottom_of_screen(self, elem=None, endy=None, startx=-20):
        """
        Swipe NEXT TO the element, to the top of the screen.
        Don't swipe directly ON the element because if it's a picker we'll just edit the value
        """
        window_size_y = self.driver.get_window_size()["height"]
        self.swipe(30, window_size_y - 80, 30, window_size_y - 500)

    def short_swipe_down(self):
        window_size_y = self.driver.get_window_size()["height"]
        self.swipe(30, window_size_y - 100, 30, window_size_y - 150)

    def swipe_down(self, count, distance):
        window_size_y = self.driver.get_window_size()["height"]
        for _ in range(0, count):
            self.swipe(30, window_size_y - 100, 30, window_size_y - 100 - distance, )

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

    ####################################################################################
    # Live TV

    def select_verify_now(self):
        self.click(id='VERIFY NOW', screenshot=True)

    def select_optimum_from_provider_page(self):
        self.click(xpath='//UIACollectionCell[3]')

    def go_to_optimum_page(self):
        self.go_to_providers_page()
        self.select_optimum_from_provider_page()
        # self.click(xpath='//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')

    def go_to_providers_page(self):
        self.goto_live_tv()
        self.select_verify_now()

    def start_watching_button(self):
        self.click(id='Start Watching')

    def login_optimum(self, username, password):
        email_field = self.driver.find_element_by_class_name('UIATextField').click()
        self.send_keys(element=email_field, data=username, class_name='UIATextField')

        password_field_element = self.driver.find_element_by_xpath(
            '//UIASecureTextField[1]')
        self.click(password_field_element)
        self.send_keys(element=password_field_element, data=password)

        if self.tablet:
            self.click(xpath='//UIAImage[3]')
        else:
            self.click(xpath='//UIAImage[2]')
        self.event.screenshot(self.screenshot())
        sleep(5)
