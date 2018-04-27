from helper.android.base_page import BasePage


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Shows']")

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

    def txt_want_to_see(self, timeout=10):
        self.get_element(timeout=timeout, name='I want to see:')

    def lst_shows_icons(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/showImage')

    def click_first_show(self):
        self.click(id='showImage')

    def validate_page(self, category='All Shows'):
        text_list = [
            'Open navigation drawer',
            'android.widget.ImageView',
            'action_search',
            'Shows',
            'I want to see:',
            category,
            'showImage'
            ]
        self.verify_in_batch(text_list, False)

    def validate_all_shows_dropdown_menu(self):
        text_list = [
            'All Shows',
            'Featured',
            'Primetime',
            'Daytime',
            'Late Night',
            'Specials',
            'News',
            'Classics'
            ]
        self.verify_in_batch(text_list, False)

