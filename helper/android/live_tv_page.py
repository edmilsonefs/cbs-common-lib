from time import sleep
from helper.android.base_page import BasePage


class LiveTvPage(BasePage):
    def __init__(self, driver, event):
        super(LiveTvPage, self).__init__(driver, event)


    def lbl_title(self, timeout=60):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Live TV']")

    def btn_try_1_week_month_free(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//*[contains(@text,'Try 1 ') and contains(@text,' free') "
                                                       "and (contains(@text,'month') or contains(@text,'week'))]")

    def btn_verify_now(self, timeout=10):
        return self.get_element(timeout=timeout, name='Verify Now')

    def btn_get_started(self, timeout=10):
        return self.get_element(timeout=timeout, name='Get Started')

    def btn_start_watching(self, timeout=10):
        return self.get_element(timeout=timeout, name='Start Watching')

    def btn_provider_logo(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/ivProviderLogo')

    def btn_take_a_tour(self, timeout=10):
        return self.get_element(timeout=timeout, name='Take a Tour')

    def btn_take_a_quick_tour(self, timeout=10):
        return self.get_element(timeout=timeout, name='Take A Quick Tour')

    def btn_read_our_faq(self, timeout=10):
        return self.get_element(timeout=timeout, name='READ OUR FAQ')

    def btn_get_notified(self, timeout=10):
        return self.get_element(timeout=timeout, name='GET NOTIFIED')

    def btn_video_no_local_station_page(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgThumbnail')

    def btn_learn_more(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/txtLearnMore')

    def btn_see_devices(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSeeDevices')

    def btn_check_availability(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnCheckAvailability')

    def btn_sign_up(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignUp')

    def lst_already_have_an_account_sign_in(self, timeout=10):
        return self.get_elements(timeout=timeout, name='Already have an account? Sign In')

    def lbl_two_ways_to_watch_live_tv(self, timeout=10):
        return self.get_element(timeout=timeout, name='Two ways to watch Live TV')

    def lst_optimum_sign_in_fields(self, timeout=15):
        return self.get_elements(timeout=timeout, class_name='android.widget.EditText')

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        elem = self.lst_already_have_an_account_sign_in()
        if len(elem) == 1:
            self.click_by_location(elem[0], side='right')
        elif len(elem) > 1:
            self.click_by_location(elem[1], side='right')
        sleep(3)
        self._hide_keyboard()

    def optimum_sign_in(self, user, password):
        if self.testdroid_device == 'asus Nexus 7':
            self.driver.tap([(600, 600)])
        if self.IS_AMAZON:
            self.driver.tap([(350, 290)])
        self.event.screenshot(self.screenshot())
        fields = self.lst_optimum_sign_in_fields()
        email_field = fields[0]
        password_field = fields[1]

        self.click(email_field)
        self.send_keys(data=user, element=email_field)
        self.event.screenshot(self.screenshot())
        self._hide_keyboard()
        self.send_keys(data=password, element=password_field)
        self._hide_keyboard()
        self.event.screenshot(self.screenshot())
        self.driver.press_keycode(66)  # Enter
        sleep(5)
        self.log_info("after pressing enter")
        self.event.screenshot(self.screenshot())

    def goto_providers_page(self):
        window_size_y = self.driver.get_window_size()["height"]
        self.goto_live_tv()
        if self.phone:
            self.driver.swipe(35, window_size_y - 600, 35, 700)
        self.click(element=self.btn_verify_now())
        sleep(5)
        self.event.screenshot(self.screenshot())
        if self.IS_AMAZON:
            self.driver.tap([(620, 710)])
        self.event.screenshot(self.screenshot())

    def goto_optimum_sign_in(self):
        self.goto_providers_page()
        self.click(element=self.btn_provider_logo())
        if self.IS_AMAZON:
            self.driver.tap([(620, 710)])
        else:
            self.click_allow_popup()
        self.event.screenshot(self.screenshot())

    def swipe_down_on_live_tv_page(self):
        origin = self.get_element(name='TV PROVIDER')
        destination = self.get_element(name=self.lbl_two_ways_to_watch_live_tv())
        self.driver.drag_and_drop(origin, destination)
        self.event.screenshot(self.screenshot())

    def validate_page(self, user_type="anonymous"):
        for i in range(2):
            self.click_allow_popup()

        self.verify_exists(element=self.lbl_title())
        if self.phone:
            self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True, name='Open navigation drawer')
        else:
            self.verify_exists(element=self.btn_navigate_up(), name='Navigate up')

        self._short_swipe_up()
        self._short_swipe_up()
        if user_type in [self.subscriber, self.cf_subscriber, self.trial]:
            if self.phone:
                self.verify_exists(element=self.btn_start_watching(), name='Start Watching')
            else:
                self.verify_exists(id=self.com_cbs_app + ':id/videoPlayerContainer', screenshot=True)
        if user_type == self.anonymous:
            self.verify_exists(element=self.lst_already_have_an_account_sign_in()[0], name='Already have an account? Sign In')
        if user_type in [self.anonymous, self.registered]:
            self.verify_exists(element=self.lbl_two_ways_to_watch_live_tv(), name='Two ways to watch Live TV')
            self.verify_exists(element=self.img_logo())
            self.verify_exists(element=self.btn_try_1_week_month_free())
        elif user_type == self.ex_subscriber:
            self.verify_exists(element=self.lbl_two_ways_to_watch_live_tv(), name='Two ways to watch Live TV')
            self.verify_exists(element=self.img_logo(), class_name='android.widget.ImageView')
            self.verify_exists(element=self.btn_get_started(), name='Get Started')
        if self.phone:
            self._short_swipe_down()
        # self.verify_exists(element=self.btn_verify_now()) TODO : should it be here?
