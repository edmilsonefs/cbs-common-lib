from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class LiveTvPage(BasePage):
    def __init__(self, driver, event):
        super(LiveTvPage, self).__init__(driver, event)

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'Try 1 ') and contains(@text,' free') "
                                                       "and (contains(@text,'month') or contains(@text,'week'))]")

    def btn_verify_now(self, timeout=10):
        return self.get_element(timeout=timeout, name='Verify Now')

    def btn_already_have_an_account_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, name='Already have an account? Sign In')

    def validate_page(self, user_type="anonymous"):
        self.verify_exists(name='Two ways to watch Live TV')
        self.verify_exists(id=self.com_cbs_app + ':id/imageView')
        if user_type == self.anonymous:
            self.verify_exists(element=self.btn_already_have_an_account_sign_in())
        self.verify_exists(name='TV PROVIDER')
        if user_type in [self.anonymous, self.registered]:
            self.verify_exists(element=self.btn_try_1_week_month_free())
        elif user_type == self.ex_subscriber:
            self.verify_exists(name='Get Started')
        if self.phone:
            self._short_swipe_down()
        self.verify_exists(element=self.btn_verify_now())

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.btn_already_have_an_account_sign_in()
        self.click_by_location(elem, side='right')
        sleep(3)
        self._hide_keyboard()