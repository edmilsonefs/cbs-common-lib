from time import sleep

from helper.android.base_page import BasePage


class UpsellPage(BasePage):
    def __init__(self, driver, event):
        super(UpsellPage, self).__init__(driver, event)

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                                       "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")

    def btn_get_started(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//android.widget.Button[@text='GET STARTED' or @text='TRY 3 DAYS FREE']")

    def btn_already_a_subscriber_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/txtAlreadyHaveAnAccount")

    def btn_take_the_tour(self, timeout=10):
        return self.get_element(timeout=timeout, name='Take the Tour')

    def validate_page(self, user_type="anonymous"):
        text_list = ['allAccessLogo']
        if user_type in [self.anonymous, self.registered]:
            text_list.append('LIMITED COMMERCIALS')
            text_list.append('TRY 1 WEEK FREE')
            text_list.append('COMMERCIAL FREE')
            text_list.append('TRY 3 DAYS FREE')
            #if user_type == self.registered:
                #text_list.append('SELECT') #todo: Does this exist? Doesn't seem like it
        elif user_type in [self.subscriber, self.trial]:
            text_list.append('UPGRADE')
        elif user_type == self.cf_subscriber:
            text_list.append('COMMERCIAL FREE')
        else:
            if user_type == self.ex_subscriber:
                text_list.append('LIMITED COMMERCIALS')
                text_list.append('COMMERCIAL FREE')
                text_list.append('Only $5.99/month')
                text_list.append('SELECT')
                #text_list.append('TRY 1 MONTH FREE') Doesn't exist on page, design change?
                #text_list.append('GET STARTED') See above

        self.verify_in_batch(text_list, False, True, False, True, 20)

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.btn_already_a_subscriber_sign_in()
        page_source_before = self.driver.page_source
        self.click(element=elem)
        sleep(3)
        page_source_after = self.driver.page_source
        if page_source_after == page_source_before:
            self.click_by_location(elem, side='right')
            sleep(3)
        self._hide_keyboard()


