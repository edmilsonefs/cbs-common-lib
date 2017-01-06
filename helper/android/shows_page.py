from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Shows')

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lbl_title())
        self.verify_exists(xpath="//*[@text='I want to see:']")
        self.verify_exists(xpath="//*[@text='All Shows']")
        self.verify_exists(id=self.com_cbs_app + ':id/showImage')