from helper.android_tv.base_page import BasePage


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)

    def btn_shows_items(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/imgPoster')

    def validate_page(self, show=None):
        self.verify_exists(element=self.btn_search_icon(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.assertTrueWithScreenShot(self.is_first_item_selected(), screenshot=True,
                                      msg="First item should be selected")
        if show is not None:
            self.verify_exists(element=self.get_element_with_text(show, 5))

    def is_first_item_selected(self):
        if len(self.btn_shows_items()) > 1:
            size_first = self.btn_shows_items()[0].size
            size_first = size_first['width'] * size_first['height']

            size_second = self.btn_shows_items()[1].size
            size_second = size_second['width'] * size_second['height']

            return size_first > size_second
        else:
            self.log_info("Only 1 show is on the Shows page")
            return True
