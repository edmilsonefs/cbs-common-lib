from ios_cbs import *


class CCommonIOSHelperJW(CommonIOSHelper):

    # You only have to click the Accept Terms box and CONTINUE button the very first time you log in
    # Kind of an edge case, but very necessary in case you log in and log out repeatedly


    def setup_method(self, method):
        super(CCommonIOSHelperJW, self).setup_method(method,
                                          {'waitForAppScript': '$.delay(5000); $.acceptAlert();'})

        self.set_implicit_wait()



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
# PHONE/HARDWARE METHODS


####################################################################################
# NAVIGATION



    # def goto_show(self, show_name):
    #     self.goto_settings()
    #     self.click(id='SearchIcon white')
    #     e = self._find_element(id='Search for a Show')
    #     self.send_keys(show_name, e)
    #     self.click(class_name='UIACollectionCell')


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




        #raise NoSuchElementException("find_on_page_horizontal failed looking for '%s'" % elem_id)



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



####################################################################################
# REGISTRATION


