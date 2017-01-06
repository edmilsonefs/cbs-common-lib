from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class SettingsPage(BasePage):
    def __init__(self, driver, event):
        super(SettingsPage, self).__init__(driver, event)

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