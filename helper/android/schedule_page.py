from time import sleep

from helper.android.base_page import BasePage


class SchedulePage(BasePage):
    def __init__(self, driver, event):
        super(SchedulePage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Schedule')

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lbl_title())
        self.verify_exists(id=self.com_cbs_app + ':id/days')
        self.verify_exists(id=self.com_cbs_app + ':id/horizontalScrollView')