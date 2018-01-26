from helper.android.base_page import BasePage

PAID = "paid"


class HomePage(BasePage):
    def __init__(self, driver, event):
        super(HomePage, self).__init__(driver, event)
        self.home_marquee_container_selector = self.com_cbs_app + ':id/marqueeContainer'
        self.lst_home_video_icons_selector = self.com_cbs_app + ':id/imgThumbnail'
        self.txt_welcome_to_cbs_selector = 'Welcome to the CBS app'
        self.txt_by_using_this_app_selector = 'By using this CBS Application, you agree to our:'
        self.btn_terms_of_use_selector = 'Terms of Use'
        self.btn_mobile_user_agreement_selector = 'Mobile User Agreement'
        self.btn_privacy_policy_selector = 'Privacy Policy'
        self.btn_video_services_selector = 'Video Services'
        self.btn_accept_selector = 'ACCEPT'

    def home_marquee_container(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.home_marquee_container_selector)

    def lst_home_video_icons(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.lst_home_video_icons_selector)

    def txt_welcome_to_cbs(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.txt_welcome_to_cbs_selector)

    def txt_by_using_this_app(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.txt_by_using_this_app_selector)

    def btn_terms_of_use(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.btn_terms_of_use_selector)

    def btn_mobile_user_agreement(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.btn_mobile_user_agreement_selector)

    def btn_privacy_policy(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.btn_privacy_policy_selector)

    def btn_video_services(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.btn_video_services_selector)

    def btn_accept(self, timeout=10):
        return self.get_element(timeout=timeout, name=self.btn_accept_selector)

    def validate_page(self, check_marquee=True):
        # Validation B
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True, name='Open navigation drawer')
        self.verify_exists(element=self.img_logo(), class_name='android.widget.ImageView')
        self.verify_exists(element=self.btn_search_icon(), id=self.com_cbs_app + ':id/action_search')
        if check_marquee:
            self.verify_exists(element=self.home_marquee_container(), id=self.home_marquee_container_selector)

    def click_all_access_video(self):
        if self.exists(name='Free Episodes', timeout=10):
            self._short_swipe_down(duration=3000)
        if self.exists(name=PAID, timeout=5):
            list_episodes = self.get_elements(name=PAID)
            self.click(element=list_episodes[0])
        else:
            if self.exists(name='Recently Watched', timeout=5):
                self.swipe_element_to_top_of_screen(elem=self.get_element(name='Recently Watched', timeout=10),
                                                    endy=150)
            prime_container = self.get_element(
                xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Stream Star Trek')]]")
            self.swipe_element_to_top_of_screen(elem=prime_container,endy=250)
            prime_container = self.get_element(
                xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Stream Star Trek')]]")
            if prime_container.location['y'] + prime_container.size['height'] > self.driver.get_window_size()['height']:
                self._short_swipe_down(duration=3000)
            for _ in range(0, 60):
                self._short_swipe_left(prime_container, 500)
            count = 0
            while count < 100:
                self._short_swipe_left(prime_container, 1000)
                if self.exists(name=PAID, timeout=5):
                    list_episodes = self.get_elements(name=PAID)
                    self.click(element=list_episodes[0])
                    self.safe_screenshot()
                    break
                else:
                    count += 1
            if count == 100:
                self.assertTrueWithScreenShot(False, msg="No All Access video is found on the home page",
                                              screenshot=True)

        self.accept_popup_video_click()

    def click_movies_episode(self):
        self.find_on_the_page(direction='down', xpath="//android.widget.TextView[@text='Movies']", timeout=5)

        self.click(element=self.get_elements(id=self.com_cbs_app + ':id/movieImage')[0])

    def validate_tou_page(self):
        # Validation A
        self.verify_exists(element=self.txt_welcome_to_cbs(), screenshot=True, name=self.txt_welcome_to_cbs_selector)
        self.verify_exists(element=self.txt_by_using_this_app(), name=self.txt_by_using_this_app_selector)
        self.verify_exists(element=self.btn_terms_of_use(), name=self.btn_terms_of_use_selector)
        self.verify_exists(element=self.btn_mobile_user_agreement(), name=self.btn_mobile_user_agreement_selector)
        self.verify_exists(element=self.btn_privacy_policy(), name=self.btn_privacy_policy_selector)
        self.verify_exists(element=self.btn_video_services(), name=self.btn_video_services_selector)
        self.verify_exists(element=self.btn_accept(), name=self.btn_accept_selector)
