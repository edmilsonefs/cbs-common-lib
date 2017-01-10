from time import sleep

from helper.android.base_page import BasePage


class UpsellPage(BasePage):
    def __init__(self, driver, event):
        super(UpsellPage, self).__init__(driver, event)

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                                       "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")

    def btn_get_started(self, timeout=10):
        return self.get_element(timeout=timeout, name='GET STARTED')

    def btn_already_a_subscriber_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, name='Already a subscriber? Sign In')

    def btn_take_the_tour(self, timeout=10):
        return self.get_element(timeout=timeout, name='Take the Tour')

    def validate_page(self, user_type="anonymous"):
        self.verify_exists(id=self.com_cbs_app + ':id/allAccessLogo', timeout=10, screenshot=True)
        if user_type in [self.anonymous, self.registered]:
            self.verify_exists(
                xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
            self.verify_exists(element=self.btn_try_1_week_month_free())
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
            self.verify_exists(element=self.btn_get_started())
            if user_type == self.registered:
                self.verify_not_exists(name='SELECT', timeout=10)
        elif user_type in [self.subscriber, self.trial]:
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
            self.verify_exists(xpath="//*[contains(@text,'UPGRADE')]")
        elif user_type == self.cf_subscriber:
            self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
        else:
            if user_type == self.ex_subscriber:
                self.verify_exists(
                    xpath="//android.widget.TextView[contains(@text,'LIMITED') and contains(@text,'COMMERCIALS')]")
                self.verify_exists(xpath="//*[contains(@text,'COMMERCIAL FREE')]")
                self.verify_exists(xpath="//*[contains(@text,'Only $ 5.99/month')]")
                self.verify_exists(name='SELECT')
                self.verify_not_exists(element=self.btn_try_1_week_month_free(), timeout=10)
                self.verify_not_exists(element=self.btn_get_started(), timeout=10)

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.btn_already_a_subscriber_sign_in()
        self.click_by_location(elem, side='right')
        sleep(3)
        self._hide_keyboard()


