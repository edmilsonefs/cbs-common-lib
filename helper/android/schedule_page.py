from helper.android.base_page import BasePage


class SchedulePage(BasePage):
    def __init__(self, driver, event):
        super(SchedulePage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Schedule']")

    def lst_shows_icon(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/title')

    def validate_page(self):
        text_list = [
            'Open navigation drawer', 
            'android.widget.ImageView', 
            ':id/action_search', 
            'Schedule', 
            ':id/days', 
            ':id/horizontalScrollView'
            ]
        self.verify_in_batch(text_list, False)
