from helper.android.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, driver, event):
        super(SignInPage, self).__init__(driver, event)

    def email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def password(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtPassword')

    def submit(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignIn')
