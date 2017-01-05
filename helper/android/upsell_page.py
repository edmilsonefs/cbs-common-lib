from time import sleep

from helper.android.base_page import BasePage


class UpsellPage(BasePage):
    def __init__(self, driver, event):
        super(UpsellPage, self).__init__(driver, event)

    def email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def already_subscriber_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.already_subscriber_sign_in()
        self.click_by_location(elem, side='right')
        sleep(3)
        self._hide_keyboard()


