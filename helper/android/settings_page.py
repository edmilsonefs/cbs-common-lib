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
        return self.get_element(timeout=timeout, id= self.com_cbs_app + ':id/updateButton')

    def btn_app_version_phone(self, timeout=10):
        return self.get_element(timeout=timeout, id= self.com_cbs_app + ':id/appVersionTextView')

    def txt_cbs(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/cbsTextView')

    def cbs_icon(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/appIcon')

    def validate_page(self):
        if self.user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            self.verify_exists(element=self.btn_subscribe)
        if self.user_type in [self.subscriber, self.trial]:
            self.verify_exists(element=self.btn_manage_account())
            if self.phone:
                self.verify_exists(element=self.btn_limited_commercials())
        if self.user_type == self.cf_subscriber:
            self.verify_exists(element=self.btn_manage_account())
            if self.phone:
                self.verify_exists(element=self.btn_commercial_free())
        if self.tablet:
            self.verify_exists(element=self.btn_app_version_tablet)
        if self.phone:
            self.verify_exists(element=self.cbs_icon)
            self.verify_exists(element=self.btn_app_version_phone)
            self.verify_exists(element=self.txt_cbs)
            self.verify_exists(element=self.btn_update)
        self.verify_exists(element=self.btn_send_feedback())
        self.verify_exists(element=self.btn_faq())
        self.verify_exists(element=self.btn_terms_of_use())
        if self.phone:
            self._short_swipe_down(duration=2000)
        self.verify_exists(element=self.btn_privacy_policy())
        self.verify_exists(element=self.btn_mobile_user_agreement())
        self.verify_exists(element=self.btn_video_services())
        self.verify_exists(element=self.btn_nielsen())
        self.verify_exists(element=self.btn_closed_captions())

    def goto_nielsen_info_page(self):
        self.goto_settings()
        if self.phone:
            self.swipe_down_if_element_is_not_visible(name='Nielsen Info & Your Choices')
        self.click(element=self.btn_nielsen())
        sleep(15)  # waiting for page to load

    def mvpd_logout(self):
        self.goto_settings()
        sleep(5)
        self.event.screenshot(self.screenshot())
        try:
            self.click(element=self.btn_disconnect_from_optimum(), screenshot=True)
            self.click(element=self.btn_mvpd_disconnect())
            self.click(element=self.btn_mvpd_disconnect_yes())
        except:
            self.log_info('Optimum was not connected')
        self.click(element=self.btn_navigate_up())
        if self.IS_AMAZON:
            try:
                self.click(element=self.btn_navigate_up())
            except:
                pass

    def sign_out(self):
        self.goto_settings()
        if self.phone:
            origin = self.driver.find_element_by_name('Video Services')
            destination = self.driver.find_element_by_name('Send Feedback')
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
        self.event.screenshot(self.screenshot())
        self.click(element=self.btn_sign_out_settings())
        self.click(element=self.btn_sign_out())
        self.event.screenshot(self.screenshot())
        #  To go back to home page
        self.click(element=self.btn_navigate_up())