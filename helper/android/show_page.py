from time import sleep

from helper.android.base_page import BasePage

class ShowPage(BasePage):
    def __init__(self, driver, event):
        super(ShowPage, self).__init__(driver, event)

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        # self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail')
        self.verify_exists(name='More options')
        # self.verify_exists(xpath="//*[@resource-id='" + self.com_cbs_app + ":id/imgMyCbsToggle']")
        # if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
        #     self.verify_exists(id=self.com_cbs_app + ':id/allAccessEpisodesContainer')
        # else:
        #     self.verify_not_exists(id=self.com_cbs_app + ':id/allAccessEpisodesContainer', timeout=10)