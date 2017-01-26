from helper.android_tv.base_page import BasePage


class DiscoverPage(BasePage):
    def __init__(self, driver, event):
        super(DiscoverPage, self).__init__(driver, event)

    def image_banner(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgBanner')

    def lst_home_video_icons(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/imgThumbnail')

    def lst_shows_posters(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/imgPoster')

    def validate_page(self):
        self.verify_exists(element=self.btn_search_icon(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.image_banner())
