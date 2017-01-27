from time import sleep
from helper.android_tv.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, driver, event):
        super(SettingsPage, self).__init__(driver, event)

    def validate_page(self):
        self.verify_exists(element=self.btn_search_icon(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(xpath="//android.widget.TextView[@resource-id='"
                                 + self.com_cbs_app + ":id/row_header' and @text='SETTINGS']")