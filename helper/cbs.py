import threading
import os

local = threading.local()

class CommonHelper:
    def init(self, driver):
        # stores the webdriver as a local thread attribute to avoid having to pass the webdriver everywhere as parameter
        local.driver = driver
        self._identify_device()

    def _identify_device(self):
        local.testdroid_device = os.getenv('TESTDROID_DEVICE')

        local.is_amazon = True if 'Amazon' in local.testdroid_device else False

        if ('Nexus 7' in local.testdroid_device or 'samsung SM-T330NU' in local.testdroid_device) \
                or (local.is_amazon and 'HD' in local.testdroid_device):
            local.is_tablet = True
            local.is_phone = False
        else:
            local.is_tablet = False
            local.is_phone = True

    def get_testdroid_device(self):
        return local.testdroid_device

    def is_phone(self):
        return local.is_phone

    def is_tablet(self):
        return local.is_tablet

    def is_amazon(self):
        return local.is_amazon

    def is_amazon_tablet(self):
        return local.is_amazon and local.is_tablet

    def click_until_element_is_visible(self, element_to_be_visible, element_to_click, click_function):
        local.driver.implicitly_wait(20)

        element = None
        count = 0
        while element is None and count < 30:
            try:
                element = local.driver.find_element_by_name(element_to_be_visible)
            except:
                click_function(name=element_to_click)
                count += 1

        local.driver.implicitly_wait(30)

    def go_to_menu_page_and_select_option(self, menu_option):
        # This is to avoid navigation drawer not being clicked properly
        count = 0
        local.driver.implicitly_wait(10)
        while count < 30:
            try:
                local.driver.find_element_by_name('Open navigation drawer').click()
                local.driver.find_element_by_name(menu_option).click()
                break
            except:
                pass
            count += 1
        local.driver.implicitly_wait(30)

    def click_by_location(self, elem):
        """
        sometimes elem.click() fails for whatever reason.  get x,y coords and click by that
        """
        loc = elem.location
        size = elem.size
        x = loc['x'] + size['width'] / 2
        y = loc['y'] + size['height'] / 2

        # an array of tuples
        local.driver.tap([(x, y)])
