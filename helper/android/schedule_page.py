from helper.android.base_page import BasePage


class SchedulePage(BasePage):
    def __init__(self, driver, event):
        super(SchedulePage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Schedule']")

    def lst_shows_icon(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/title')

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True, name='Open navigation drawer')
        self.verify_exists(element=self.img_logo(), class_name='android.widget.ImageView')
        self.verify_exists(element=self.btn_search_icon(), id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(element=self.lbl_title(), xpath="//*[@text='Schedule']")
        self.verify_exists(id=self.com_cbs_app + ':id/days')
        self.verify_exists(id=self.com_cbs_app + ':id/horizontalScrollView')