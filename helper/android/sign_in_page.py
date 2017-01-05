from helper.android.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, driver, event):
        super(SignInPage, self).__init__(driver, event)

    def title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Sign In')

    def facebook_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgFacebook')

    def twitter_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgTwitter')

    def google_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgGoogle')

    def email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def password(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtPassword')

    def submit(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignIn')

    def don_t_have_an_account_sign_up(self, timeout=10):
        return self.get_element(timeout=timeout, name="Don't have an account? Sign Up")

    def validate_page(self):
        self._hide_keyboard()
        self._hide_keyboard()
        self.verify_exists(element=self.title(), screenshot=True)
        self.verify_exists(name='Sign in with your social account')
        self.verify_exists(element=self.facebook_button())
        self.verify_exists(element=self.twitter_button())
        if not self.IS_AMAZON:
            self.verify_exists(element=self.google_button())
        self.verify_exists(name='Sign in with your email')
        self.verify_exists(name='Forgot Your Password?')
        self.verify_exists(name='Sign In')
        self.verify_exists(element=self.don_t_have_an_account_sign_up())

    def click_dont_have_account_sign_up(self):
        self._hide_keyboard()
        self.click(element=self.don_t_have_an_account_sign_up())
