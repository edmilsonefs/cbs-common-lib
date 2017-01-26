from helper.android_tv.base_page import BasePage


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lbl_title())
        self.verify_exists(xpath="//*[@text='I want to see:']", timeout=20)
        self.verify_exists(xpath="//*[@text='All Shows']")
        self.verify_exists(id=self.com_cbs_app + ':id/showImage')
