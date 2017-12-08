from helper.android.base_page import BasePage
from helper.android.settings_page import SettingsPage


class NielsenPage(BasePage):
    settings_page = None

    def __init__(self, driver, event):
        super(NielsenPage, self).__init__(driver, event)
        self.settings_page = SettingsPage(self.driver, self.event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Nielsen Info & Your Choices']")

    def btn_opt_out(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//android.view.View[contains(@content-desc,'click here')][1]")

    def btn_opt_in(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//android.view.View[contains(@content-desc,'click here')][2]")

    def btn_ok(self, timeout=10):
        return self.get_element(timeout=timeout, name='OK')

    def goto_nielsen_opt_out(self):
        window_height = self.driver.get_window_size()["height"]
        self.settings_page.goto_nielsen_info_page()
        # Nielsen page now needs to scroll to end of page to find buttons
        for i in range(0, 5):
            self.driver.swipe(500, window_height - 600, 500, 200)
        self.click(element=self.btn_opt_out(), screenshot=True)
        self.click(element=self.btn_ok())
        self.navigate_up()

    def goto_nielsen_opt_in(self):
        window_height = self.driver.get_window_size()["height"]
        self.settings_page.goto_nielsen_info_page()
        # Nielsen page now needs to scroll to end of page to find buttons
        for i in range(0, 5):
            self.driver.swipe(500, window_height - 600, 500, 200)
        self.safe_screenshot()
        self.click(element=self.btn_opt_in(), screenshot=True)
        self.click(element=self.btn_ok())
        self.navigate_up()







