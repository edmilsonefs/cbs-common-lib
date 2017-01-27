from helper.android_tv.base_page import BasePage


class LiveTvPage(BasePage):
    def __init__(self, driver, event):
        super(LiveTvPage, self).__init__(driver, event)

    def validate_page(self):
        self.verify_exists(element=self.btn_search_icon(), screenshot=True)
        self.verify_exists(element=self.img_logo())
