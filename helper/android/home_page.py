from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class HomePage(BasePage):
    def __init__(self, driver, event):
        super(HomePage, self).__init__(driver, event)

    def home_marquee_container(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/marqueeContainer')

    def lst_home_video_icons(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ":id/imgThumbnail")

    def txt_welcome_to_cbs(self, timeout=10):
        return self.get_element(timeout=timeout, name='Welcome to the CBS app')

    def txt_by_using_this_app(self, timeout=10):
        return self.get_element(timeout=timeout, name='By using this CBS Application, you agree to our:')

    def btn_terms_of_use(self, timeout=10):
        return self.get_element(timeout=timeout, name='Terms of Use')

    def btn_mobile_user_agreement(self, timeout=10):
        return self.get_element(timeout=timeout, name='Mobile User Agreement')

    def btn_privacy_policy(self, timeout=10):
        return self.get_element(timeout=timeout, name='Privacy Policy')

    def btn_video_services(self, timeout=10):
        return self.get_element(timeout=timeout, name='Video Services')

    def btn_accept(self, timeout=10):
        return self.get_element(timeout=timeout, name='ACCEPT')

    def validate_page(self):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.home_marquee_container())

    def click_all_access_video(self):
        if self.exists(name='Free Episodes', timeout=10):
            self._short_swipe_down(duration=3000)
        if self.exists(name=PAID, timeout=5):
            list_episodes = self.get_elements(name=PAID)
            self.click(element=list_episodes[0])
        else:
            if self.exists(name='Recently Watched', timeout=5):
                self.swipe_element_to_top_of_screen(elem=self.get_element(name='Recently Watched', timeout=10), endy=150)
            prime_container = self.get_element(xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Primetime')]]")
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
                self.assertTrueWithScreenShot(False, msg="No All Access video is found on the home page", screenshot=True)

        self.accept_popup_video_click()

    def click_movies_episode(self):
        if not self.exists(xpath="//android.widget.TextView[@text='Movies']", timeout=5):
            element = self.find_on_the_page(direction='down', xpath="//android.widget.TextView[@text='Movies']", timeout=5)
            self.swipe_element_to_top_of_screen(elem=element, endy=150)
            sleep(3)
            self.tap(0.3, 0.3, "Open Movies episode on the Home Page")
        else:
            self.swipe_element_to_top_of_screen(elem=self.get_element(xpath="//android.widget.TextView[@text='Movies']", timeout=10), endy=150)
            sleep(3)
            self.tap(0.3, 0.3, "Open Movies episode on the Home Page")

    def validate_tou_page(self):

        self.verify_exists(element=self.txt_welcome_to_cbs(), screenshot=True)
        self.verify_exists(element=self.txt_by_using_this_app())
        self.verify_exists(element=self.btn_terms_of_use())
        self.verify_exists(element=self.btn_mobile_user_agreement())
        self.verify_exists(element=self.btn_privacy_policy())
        self.verify_exists(element=self.btn_video_services())
        self.verify_exists(element=self.btn_accept())
