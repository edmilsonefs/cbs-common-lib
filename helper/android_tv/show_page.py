from helper.android_tv.base_page import BasePage


class ShowPage(BasePage):
    def __init__(self, driver, event):
        super(ShowPage, self).__init__(driver, event)

    def validate_page(self, show=None):
        self.verify_exists(element=self.get_element(id=self.com_cbs_app + ':id/details_overview_image', timeout=5), screenshot=True)
        self.verify_exists(element=self.get_element(id=self.com_cbs_app + ':id/details_overview_right_panel', timeout=5))
        self.verify_exists(element=self.get_element(id=self.com_cbs_app + ':id/lb_details_description_title', timeout=5))
        self.verify_exists(element=self.get_element(id=self.com_cbs_app + ':id/lb_details_description_body', timeout=5))
        self.verify_exists(element=self.get_element(id=self.com_cbs_app + ':id/lb_details_description_body', timeout=5))
        if show is not None:
            self.verify_exists(element=self.get_element_with_text(show, 5))
        self.assertTrueWithScreenShot(len(self.get_elements(id=self.com_cbs_app + ':id/imgThumbnail', timeout=5)) > 0,
                                      msg="Some episodes should be visible")
