from helper.android.base_page import BasePage


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Shows')

    def btn_all_shows(self, timeout=10):
        return self.get_element(timeout=timeout, name='All Shows')

    def btn_featured(self, timeout=10):
        return self.get_element(timeout=timeout, name='Featured')

    def btn_primetime(self, timeout=10):
        return self.get_element(timeout=timeout, name='Primetime')

    def btn_daytime(self, timeout=10):
        return self.get_element(timeout=timeout, name='Daytime')

    def btn_latenight(self, timeout=10):
        return self.get_element(timeout=timeout, name='Late Night')

    def btn_specials(self, timeout=10):
        return self.get_element(timeout=timeout, name='Specials')

    def btn_news(self, timeout=10):
        return self.get_element(timeout=timeout, name='News')

    def btn_classics(self, timeout=10):
        return self.get_element(timeout=timeout, name='Classics')

    def lst_shows_icons(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/showImage')

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lbl_title())
        self.verify_exists(xpath="//*[@text='I want to see:']", timeout=20)
        self.verify_exists(xpath="//*[@text='All Shows']")
        self.verify_exists(id=self.com_cbs_app + ':id/showImage')
