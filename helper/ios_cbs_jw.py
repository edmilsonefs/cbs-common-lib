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









####################################################################################
# REGISTRATION


