from time import sleep
from helper.ios.base_page import BasePage


class LiveTvPage(BasePage):
    def __init__(self, driver, event):
        super(LiveTvPage, self).__init__(driver, event)

    # def lbl_title(self, timeout=10):
    #     return self.top_toolbar(timeout=timeout).find_element_by_id('Live TV')

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'TRY 1 ') and contains(@text,' FREE') "
                                                       "and (contains(@text,'MONTH') or contains(@text,'WEEK'))]")

    def btn_verify_now(self, timeout=10):
        return self.get_element(timeout=timeout, id='VERIFY NOW')

    def btn_get_started(self, timeout=10):
        return self.get_element(timeout=timeout, id='GET STARTED')

    def btn_start_watching(self, timeout=10):
        return self.get_element(timeout=timeout, id='Start Watching')

    def btn_provider_logo(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='//UIACollectionCell[2]')

    def btn_take_a_tour(self, timeout=10):
        return self.get_element(timeout=timeout, id='Take the tour')

    def btn_take_a_quick_tour(self, timeout=10):
        return self.get_element(timeout=timeout, id='TAKE A QUICK TOUR')

    def btn_read_our_faq(self, timeout=10):
        return self.get_element(timeout=timeout, id='READ OUR FAQ')

    def btn_learn_more(self, timeout=10):
        return self.get_element(timeout=timeout, id='Learn more')

    # def btn_see_devices(self, timeout=10):
    #     return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSeeDevices')

    def btn_check_availability(self, timeout=10):
        return self.get_element(timeout=timeout, id='CHECK AVAILABILITY')

    def btn_already_have_an_account_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, id='Already have an account? Sign In')

    def lbl_two_ways_to_watch_live_tv(self, timeout=10):
        return self.get_element(timeout=timeout, id='Two ways to watch Live TV')

    def validate_page(self, user_type="anonymous"):
        self.verify_exists(element=self.lbl_title())
        if self.phone:
            self.verify_exists(element=self.btn_hamburger_menu())
        else:
            self.verify_exists(element=self.btn_navigate_up())
        if user_type not in [self.subscriber, self.cf_subscriber, self.trial]:
            self.verify_exists(name='Two ways to watch Live TV')
            self.verify_exists(id='CBSEye_white')
            if user_type == self.anonymous:
                self.verify_exists(element=self.btn_already_have_an_account_sign_in())
            self.verify_exists(name='TV PROVIDER')
            if user_type in [self.anonymous, self.registered]:
                self.verify_exists(element=self.btn_try_1_week_month_free())
            elif user_type == self.ex_subscriber:
                self.verify_exists(element=self.btn_get_started())
            if self.phone:
                self._short_swipe_down()
            self.verify_exists(element=self.btn_verify_now())
        # else:
        #     self.verify_exists(id=self.com_cbs_app + ':id/imgStationLogo')
        #     self.verify_exists(id=self.com_cbs_app + ':id/programsContentFlipper')
        #     self.verify_not_exists(id=self.com_cbs_app + ':id/imgProviderLogo', timeout=10)

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.btn_already_have_an_account_sign_in()
        if len(elem) == 1:
            self.click_by_location(elem[0], side='right')
        elif len(elem) > 1:
            self.click_by_location(elem[1], side='right')
        sleep(3)
        self._hide_keyboard()
