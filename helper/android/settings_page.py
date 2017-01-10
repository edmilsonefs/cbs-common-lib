from helper.android.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, driver, event):
        super(SettingsPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        if self.phone:
            return self.top_toolbar(timeout=timeout).find_element_by_name('Settings')
        else:
            return self.top_toolbar(timeout=timeout).find_element_by_name('Subscription')

    def btn_nielsen(self, timeout=10):
        return self.get_element(timeout=timeout, name='Nielsen Info & Your Choices')

    def validate_page(self):
        self.verify_exists(name='Subscribe', screenshot=True)
        if self.tablet:
            self.verify_exists(name='App Version')
        if self.phone:
            self.verify_exists(id=self.com_cbs_app + ':id/appIcon')
            self.verify_exists(id=self.com_cbs_app + ':id/appVersionTextView')
            self.verify_exists(id=self.com_cbs_app + ':id/cbsTextView')
            self.verify_exists(id=self.com_cbs_app + ':id/updateButton')
        self.verify_exists(name='Send Feedback')
        # self.verify_exists(name='Push Notifications')
        self.verify_exists(name='FAQ')
        self.verify_exists(name='Terms of Use')
        if self.phone:
            self._short_swipe_down(duration=2000)
        self.verify_exists(name='Privacy Policy')
        self.verify_exists(name='Mobile User Agreement')
        self.verify_exists(name='Video Services')
        self.verify_exists(name='Nielsen Info & Your Choices')
        self.verify_exists(name='Closed Captions')

    def goto_nielsen_info(self):
        self.goto_settings()
        if self.phone:
            self._short_swipe_down(duration=2000)
        self.click(element=self.btn_nielsen())
