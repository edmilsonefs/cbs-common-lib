from time import sleep
from helper.android.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, driver, event):
        super(SettingsPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        if self.phone:
            return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Settings']")
        else:
            return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Manage Account']")

    def btn_nielsen(self, timeout=10):
        return self.get_element(timeout=timeout, name='Nielsen Info & Your Choices')

    def btn_disconnect_from_optimum(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='//*[contains(@text,"Disconnect from Optimum")]')

    def btn_mvpd_disconnect(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnMvpdLogoutSettings')

    def btn_mvpd_disconnect_yes(self, timeout=10):
        return self.get_element(timeout=timeout, id='android:id/button1')

    def btn_sign_out_settings(self, timeout=10):
        return self.get_element(timeout=timeout, name='Sign Out')

    def btn_sign_out(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/signOutButton')

    def btn_faq(self, timeout=10):
        return self.get_element(timeout=timeout, name='FAQ')

    def btn_app_version_tablet(self, timeout=10):
        return self.get_element(timeout=timeout, name='App Version')

    def btn_terms_of_use(self, timeout=10):
        return self.get_element(timeout=timeout, name='Terms of Use')

    def btn_privacy_policy(self, timeout=10):
        return self.get_element(timeout=timeout, name='Privacy Policy')

    def btn_mobile_user_agreement(self, timeout=10):
        return self.get_element(timeout=timeout, name='Mobile User Agreement')

    def btn_video_services(self, timeout=10):
        return self.get_element(timeout=timeout, name='Video Services')

    def btn_closed_captions(self, timeout=10):
        return self.get_element(timeout=timeout, name='Closed Captions')

    def btn_send_feedback(self, timeout=10):
        return self.get_element(timeout=timeout, name='Send Feedback')

    def btn_manage_account(self, timeout=10):
        return self.get_element(timeout=timeout, name='Manage Account')

    def btn_limited_commercials(self, timeout=10):
        return self.get_element(timeout=timeout, name='Limited Commercials')

    def btn_commercial_free(self, timeout=10):
        return self.get_element(timeout=timeout, name='Commercial Free')

    def btn_subscribe(self, timeout=10):
        return self.get_element(timeout=timeout, name='Subscribe')

    def btn_update(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/updateButton')

    def btn_app_version_phone(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/appVersionTextView')

    def txt_cbs(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/cbsTextView')

    def cbs_icon(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/appIcon')

    def validate_page(self, user_type="anonymous"):
        text_list_one = ['Send Feedback', 'FAQ', 'Terms of Use']
        if user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            text_list_one.append('Subscribe')
        if user_type in [self.subscriber, self.trial, self.cf_subscriber]:
            text_list_one.append('Manage Account')
        if user_type == self.cf_subscriber:
            text_list_one.append('Manage Account')
        if self.tablet:
            text_list_one.append('App Version')
        if self.phone:
            text_list_one.append(':id/appIcon')
            text_list_one.append(':id/appVersionTextView')
            text_list_one.append(':id/cbsTextView')
        self.verify_in_batch(text_list_one, False)
        if self.phone:
            self._short_swipe_down(duration=2000)
        text_list_two = [
            'Privacy Policy',
            'Mobile User Agreement',
            'Video Services',
            'Nielsen Info.*Your Choices',
            'Closed Captions'
            ]
        if user_type != self.anonymous:
            text_list_two.append('Sign Out')
        self.verify_in_batch(text_list_two, False)

    def goto_nielsen_info_page(self):
        self.goto_settings()
        if self.phone:
            self.swipe_down_if_element_is_not_visible(name='Nielsen Info & Your Choices')
        self.click(element=self.btn_nielsen())
        sleep(15)  # waiting for page to load

    def mvpd_logout(self):
        self.goto_settings()
        sleep(5)
        self.safe_screenshot()
        try:
            self.click(element=self.btn_disconnect_from_optimum(), screenshot=True)
            if self.exists(element=self.btn_mvpd_disconnect()):
                self.click(element=self.btn_mvpd_disconnect())
            else:
                self.click(element=self.btn_disconnect_from_optimum())
                self.click(element=self.btn_mvpd_disconnect())
            if self.exists(element=self.btn_mvpd_disconnect_yes()):
                self.click(element=self.btn_mvpd_disconnect_yes())
        except:
            self.log_info('Optimum was not connected')
        sleep(5)
        self.navigate_up()
        if self.IS_AMAZON:
            try:
                self.click(element=self.btn_navigate_up())
            except:
                pass

    def sign_out(self):
        self.goto_settings()
        if self.phone:
            origin = self.settings_page.btn_video_services()
            destination = self.settings_page.btn_send_feedback()
            self.driver.drag_and_drop(origin, destination)
            self.safe_screenshot()
            self.swipe_down_if_element_is_not_visible(name='Sign Out')
            self.safe_screenshot()
        self.click(name='Sign Out')
        if self.tablet:
            self.click_safe(name='Sign Out')
        self.safe_screenshot()
        self.click(element=self.settings_page.btn_sign_out())
        self.safe_screenshot()
        #  To go back to home page
        self.click(element=self.settings_page.btn_navigate_up())
