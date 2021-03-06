from time import sleep

from helper.android.base_page import BasePage


class UpsellPage(BasePage):
    def __init__(self, driver, event):
        super(UpsellPage, self).__init__(driver, event)

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                                       "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")

    def btn_get_started(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                                       "and (contains(@text,'MONTH') or contains(@text,'WEEK')) or @text='GET STARTED']")

    def btn_already_a_subscriber_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[@text='Already have an account? Sign In' or @text='Already a subscriber? Sign In']")

    def btn_take_the_tour(self, timeout=10):
        return self.get_element(timeout=timeout, name='Take the Tour')

    def validate_page(self, user_type="anonymous"):
        text_list = ['allAccessLogo']
        if user_type in [self.anonymous, self.registered]:
            text_list.append('LIMITED COMMERCIALS')
            text_list.append('COMMERCIAL FREE')
            text_list.append('GET STARTED|TRY \d+ (WEEK|WEEKS|MONTH|MONTHS) FREE')
        elif user_type in [self.subscriber, self.trial]:
            text_list.append('COMMERCIAL FREE')
            text_list.append('UPGRADE')
            text_list.append('READ OUR FAQ')
        elif user_type == self.cf_subscriber:
            text_list.append('COMMERCIAL FREE')
            text_list.append('READ OUR FAQ')
            self.verify_not_exists(name='UPGRADE')
        else:
            if user_type == self.ex_subscriber:
                text_list.append('LIMITED COMMERCIALS')
                text_list.append('COMMERCIAL FREE')
                text_list.append('Only \$5\.99\/month')
                text_list.append('Only \$9\.99\/month')
                text_list.append('SELECT')

        self.verify_in_batch(text_list, case_sensitive=False, strict_visibility=True, screenshot=True, strict=False,
                             with_timeout=20)

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        self.click(element=self.btn_already_a_subscriber_sign_in())
        # elem = self.btn_already_a_subscriber_sign_in()
        # page_source_before = self.driver.page_source
        # self.click(element=elem)
        # sleep(3)
        # page_source_after = self.driver.page_source
        # if page_source_after == page_source_before:
        #     self.click_by_location(elem, side='right')
        #     sleep(3)
        self._hide_keyboard()


