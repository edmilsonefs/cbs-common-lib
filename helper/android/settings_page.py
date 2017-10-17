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

    def validate_page(self):
        # validation Q
        if self.user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            self.verify_exists(element=self.btn_subscribe, name='Subscribe')
        if self.user_type in [self.subscriber, self.trial]:    # TODO add lc subscriber user type
            self.verify_exists(element=self.btn_manage_account(), name='Manage Account')
            if self.phone:
                self.verify_exists(element=self.btn_limited_commercials(), name='Limited Commercials')  # TODO - not in spec
        if self.user_type == self.cf_subscriber:
            self.verify_exists(element=self.btn_manage_account(), name='Manage Account')
            if self.phone:
                self.verify_exists(element=self.btn_commercial_free(), name='Commercial Free')
        if self.tablet:
            self.verify_exists(element=self.btn_app_version_tablet, name='App Version')
        if self.phone:
            self.verify_exists(element=self.cbs_icon, id=self.com_cbs_app + ':id/appIcon')
            self.verify_exists(element=self.btn_app_version_phone, id=self.com_cbs_app + ':id/appVersionTextView')
            self.verify_exists(element=self.txt_cbs, id=self.com_cbs_app + ':id/cbsTextView')
            self.verify_exists(element=self.btn_update, id=self.com_cbs_app + ':id/updateButton')
        self.log_info("Problem with 'Send Feedback'")
        self.safe_screenshot()
        self.verify_exists(element=self.btn_send_feedback(), name='Send Feedback')
        self.verify_exists(element=self.btn_faq(), name='FAQ')
        self.verify_exists(element=self.btn_terms_of_use(), name='Terms of Use')
        if self.phone:
            self._short_swipe_down(duration=2000)
        self.verify_exists(element=self.btn_privacy_policy(), name='Privacy Policy')
        self.verify_exists(element=self.btn_mobile_user_agreement(), name='Mobile User Agreement')
        self.verify_exists(element=self.btn_video_services(), name='Video Services')
        self.verify_exists(element=self.btn_nielsen(), name='Nielsen Info & Your Choices')
        self.verify_exists(element=self.btn_closed_captions(), name='Closed Captions')
        #TODO add push notifications
        #TODO add sign out

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
            origin = self.btn_video_services()
            destination = self.btn_send_feedback()
            self.driver.drag_and_drop(origin, destination)
            self.event.screenshot(self.screenshot())
        self.event.screenshot(self.screenshot())
        self.click(element=self.btn_sign_out_settings())
        self.click(element=self.btn_sign_out())
        self.event.screenshot(self.screenshot())
        #  To go back to home page
        self.click(element=self.btn_navigate_up())
