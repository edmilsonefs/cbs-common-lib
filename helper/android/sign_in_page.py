from helper.android.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, driver, event):
        super(SignInPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Sign In']")

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

    def btn_terms_cancel_submit(self, timeout=10):
        return self.get_element(timeout=timeout, name='CANCEL')

    def txt_terms_have_changed(self, timeout=10):
        return self.get_element(timeout=timeout, name='Our Terms Have Changed')

    def btn_facebook_ok(self, timeout=10):
        return self.get_element(timeout=timeout, name='OK ')

    def lst_social_sign_in_fields(self, timeout=10):
        return self.get_elements(timeout=timeout, class_name='android.widget.EditText')

    def sign_in(self, email, password):
        self.sign_in_without_finish(email, password)
        self.post_sign_in_accept_terms()

    def sign_in_without_finish(self, email, password):
        self.send_keys(data=email, element=self.txt_email())
        self._hide_keyboard()
        self.send_keys(data=password, element=self.txt_password())
        self._hide_keyboard()

        self.click(element=self.btn_submit(), screenshot=True)

    def sign_in_facebook(self, email, password):
        fields = self.lst_social_sign_in_fields()
        email_field = fields[0]
        password_field = fields[1]

        self.send_keys(data=email, element=email_field)
        self._hide_keyboard()
        self.send_keys(data=password, element=password_field)
        self._hide_keyboard()
        self.driver.press_keycode(66)  # Enter
        self.click(element=self.btn_facebook_ok())

        self.post_sign_in_accept_terms()

    def sign_in_twitter(self, email, password):
        fields = self.lst_social_sign_in_fields()
        email_field = fields[0]
        password_field = fields[1]

        self.send_keys(data=email, element=email_field)
        self._hide_keyboard()
        self.send_keys(data=password, element=password_field)
        self._hide_keyboard()
        self.driver.press_keycode(66)  # Enter
        self.safe_screenshot()

        self.post_sign_in_accept_terms()

    def post_sign_in_accept_terms(self):
        if self.exists(element=self.btn_terms_accept(timeout=30)):
            self.click(element=self.btn_terms_accept())
            self.click(element=self.btn_terms_accept_submit(), screenshot=True)

        if self.exists(name='Ok', timeout=5):
            self.click(element=self.get_element(name='Ok'))

        # # Need to handle the error
        # elif self.exists(name='OK', timeout=5):
        #     self.click(element=self.get_element(name='OK'))

    def validate_page(self):
        self._hide_keyboard()
        self._hide_keyboard()
        self.verify_exists(element=self.lbl_title(), screenshot=True, xpath="//*[@text='Sign In']")
        self.verify_exists(name='Sign in with your social account')
        self.verify_exists(element=self.btn_facebook_button(), id=self.com_cbs_app + ':id/imgFacebook')
        self.verify_exists(element=self.btn_twitter_button(), id=self.com_cbs_app + ':id/imgTwitter')
        if not self.IS_AMAZON:
            self.verify_exists(element=self.btn_google_button(), id=self.com_cbs_app + ':id/imgGoogle')
        self.verify_exists(name='Sign in with your email')
        self.verify_exists(name='Forgot Your Password?')
        self.verify_exists(name='Sign In')
        self.verify_exists(element=self.btn_don_t_have_an_account_sign_up(), name="Don't have an account? Sign Up")

    def click_dont_have_account_sign_up(self):
        self._hide_keyboard()
        self.click(element=self.btn_don_t_have_an_account_sign_up())


