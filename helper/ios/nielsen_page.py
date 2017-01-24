from helper.ios.base_page import BasePage
from helper.ios.settings_page import SettingsPage

class NielsenPage(BasePage):
    settings_page = None

    def __init__(self, driver, event):
        super(NielsenPage, self).__init__(driver, event)
        self.settings_page = SettingsPage(self.driver, self.event)

    # def lbl_title(self, timeout=10):
    #     return self.top_toolbar(timeout=timeout).find_element_by_name('Nielsen Info & Your Choices')

    def btn_opt_out(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='(//UIAStaticText[@name="click here"])[1]')

    def btn_opt_in(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='(//UIAStaticText[@name="click here"])[2]')

    def btn_ok(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='//UIAButton[@name="OK"]')

    def btn_close(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='(//UIAButton[@name="Close"])')

    def goto_nielsen_opt_out(self):
        self.settings_page.goto_nielsen_info()
        # Nielsen page now needs to scroll to end of page to find buttons
        if self.tablet:
            el1 = self.driver.find_element_by_xpath('//UIAStaticText[7]')
            el2 = self.driver.find_element_by_xpath('//UIAStaticText[3]')
            self.driver.drag_and_drop(el1, el2)
        self.click(element=self.btn_opt_out(), screenshot=True)
        self.click(element=self.btn_ok())
        self.click(element=self.btn_close())

    def goto_nielsen_opt_in(self):
        window_height = self.driver.get_window_size()["height"]
        self.settings_page.goto_nielsen_info()
        # Nielsen page now needs to scroll to end of page to find buttons
        if self.tablet:
            el1 = self.driver.find_element_by_xpath('//UIAStaticText[7]')
            el2 = self.driver.find_element_by_xpath('//UIAStaticText[3]')
            self.driver.drag_and_drop(el1, el2)
        self.event.screenshot(self.screenshot())
        self.click(element=self.btn_opt_in(), screenshot=True)
        self.click(element=self.btn_ok())
        self.click(element=self.btn_close())







