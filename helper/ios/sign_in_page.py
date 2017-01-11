from helper.android.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, driver, event):
        super(SignInPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Sign In')

    def btn_facebook_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgFacebook')

    def btn_twitter_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgTwitter')

    def btn_google_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgGoogle')

    def txt_email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def txt_password(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtPassword')

    def btn_submit(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignIn')

    def btn_don_t_have_an_account_sign_up(self, timeout=10):
        return self.get_element(timeout=timeout, name="Don't have an account? Sign Up")

    def btn_terms_accept(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/terms_accept_checkBox')

    def btn_terms_accept_submit(self, timeout=10):
        return self.get_element(timeout=timeout, name='SUBMIT')

    def sign_in(self, email, password):
        self.send_keys(data=email, element=self.txt_email())
        self._hide_keyboard()
        self.send_keys(data=password, element=self.txt_password())
        self._hide_keyboard()

        self.click(element=self.btn_submit(), screenshot=True)

        self.post_sign_in_accept_terms()

    def post_sign_in_accept_terms(self):
        if self.exists(element=self.btn_terms_accept(timeout=30), timeout=30):
            self.click(element=self.btn_terms_accept())
            self.click(element=self.btn_terms_accept_submit(), screenshot=True)

        if self.exists(name='Ok', timeout=5):
            self.click(element=self.get_element(name='Ok'))

    def validate_page(self):
        self._hide_keyboard()
        self._hide_keyboard()
        self.verify_exists(element=self.lbl_title(), screenshot=True)
        self.verify_exists(name='Sign in with your social account')
        self.verify_exists(element=self.btn_facebook_button())
        self.verify_exists(element=self.btn_twitter_button())
        if not self.IS_AMAZON:
            self.verify_exists(element=self.btn_google_button())
        self.verify_exists(name='Sign in with your email')
        self.verify_exists(name='Forgot Your Password?')
        self.verify_exists(name='Sign In')
        self.verify_exists(element=self.btn_don_t_have_an_account_sign_up())

    def click_dont_have_account_sign_up(self):
        self._hide_keyboard()
        self.click(element=self.btn_don_t_have_an_account_sign_up())


