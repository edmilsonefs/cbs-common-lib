from time import sleep

from helper.android.base_page import BasePage


class SignUpPage(BasePage):
    def __init__(self, driver, event):
        super(SignUpPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Sign Up')

    def btn_facebook_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgFacebook')

    def btn_twitter_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgTwitter')

    def btn_google_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgGoogle')

    def txt_first_name(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtFirstName')

    def txt_last_name(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtLastName')

    def txt_email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def txt_email_confirm(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtConfirmEmail')

    def txt_password(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtPassword')

    def txt_password_confirm(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/editConfirmPassword')

    def btn_submit(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignUp')

    def btn_state(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/spnState')

    def txt_zip(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtZipCode')

    def btn_gender(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/spnGender')

    def btn_birth_date(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtBirthdate')

    def btn_terms_and_conditions(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/chkAccountAgreement')

    def btn_already_have_an_account_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, name='Already have an account? Sign In')

    def validate_page(self):
        self._hide_keyboard()
        if self.phone:
            self.verify_exists(element=self.lbl_title())
        self.verify_exists(name='Sign up with your social account', screenshot=True)
        self.verify_exists(element=self.btn_facebook_button())
        self.verify_exists(element=self.btn_twitter_button())
        if not self.IS_AMAZON:
            self.verify_exists(element=self.btn_google_button())
        self.verify_exists(name='Sign up with your email')
        for _ in range(0, 2):
            self._short_swipe_down()
        self.verify_exists(element=self.btn_submit(), screenshot=True)
        self.verify_exists(element=self.btn_already_have_an_account_sign_in())

    def register_new_user(self, year=1996):
        self._hide_keyboard()

        for _ in range(0, 2):
            self._short_swipe_up()

        fn, ln = self._register_user_part_1()
        self._register_user_part_2(year)
        self._register_user_part_3()
        self._register_user_part_4()
        self.submit_registration_form()

        return fn, ln

    def _register_user_part_1(self):

        ##### PART A: first/last/email/pwd #####

        fn_str = self.generate_random_string()
        ln_str = self.generate_random_string()
        email_str = "TestA%s@gmail.com" % self.generate_random_string()

        first_name = self.txt_first_name()
        self.send_keys(data=fn_str, element=first_name)
        self._hide_keyboard()

        last_name = self.txt_last_name()
        self.send_keys(data=ln_str, element=last_name)
        self._hide_keyboard()

        email = self.txt_email()
        self.send_keys(data=email_str, element=email, screenshot=True)
        self._hide_keyboard()

        email_confirm = self.exists(element=self.txt_email_confirm())
        if email_confirm is not False:
            self.send_keys(data=email_str, element=email_confirm, screenshot=True)
            self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(email_confirm, endy=400)

        pwd = self.txt_password()
        self.send_keys('abcdef', pwd)
        self._hide_keyboard()

        pwd_confirm = self.txt_password_confirm()
        self.send_keys('abcdef', pwd_confirm, screenshot=True)
        self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(pwd_confirm, endy=300)

        return fn_str, ln_str

    def _register_user_part_2(self, year=1996):
        self.btn_birth_date().click()

        if self.exists(id='android:id/date_picker_header_year', timeout=10):
            self.click(id='android:id/date_picker_header_year', data='Click on current year')
            list_years = self._find_element(id='android:id/animator')

            for _ in range(5):
                self._swipe_list_years(list_years)

            years = self.driver.find_elements_by_class_name("android.widget.TextView")

            self.click(element=years[5], data='Choose year from the list')
            self.click(name='OK')
        elif self.exists(id='android:id/date_picker_year', timeout=10):
            self.click(id='android:id/date_picker_year', data='Click on current year')
            list_years = self._find_element(id='android:id/animator')

            for _ in range(5):
                self._swipe_list_years(list_years)

            years = self.driver.find_elements_by_class_name("android.widget.TextView")

            self.click(element=years[5], data='Choose year from the list')
            self.click(name='OK')
        else:
            pickers = self.driver.find_elements_by_class_name('android.widget.NumberPicker')

            year_picker = pickers[2]

            year_but = year_picker.find_element_by_class_name('android.widget.Button')

            # swipe a bunch of times to make the user 18 years old
            # do in two steps to try to speed it up some
            for i in range(10):
                self._swipe_datepicker_down(year_but)

            for i in range(10):
                self._swipe_datepicker_down(year_but)
                year_picker = self.driver.find_elements_by_class_name('android.widget.NumberPicker')[2]
                current_year = year_picker.find_element_by_class_name('android.widget.Button').text

                if current_year < year:
                    break

            self.driver.implicitly_wait(10)
            try:
                elem = self.driver.find_element_by_name('Set')
            except:
                elem = self.driver.find_element_by_name('Done')

            self.click(element=elem, data='Choose the date')

            self.driver.implicitly_wait(self.default_implicit_wait)

    def _register_user_part_3(self):
        self.click(name='Male')

    def _register_user_part_4(self):
        # I think using the resource id is generally not advised because it's just part of the app's implementation
        # and could be changed at any time.  Here we get it dynamically just so we're sure we get the same element
        # after updating it to a new value
        zip = self.txt_zip()

        zip_text = zip.text

        self.send_keys('78704', zip)
        sleep(2)

        zip = self.txt_zip()

        self.verify_not_equal(zip_text, zip.text, screenshot=True)

        self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(zip)

        self.accept_terms_and_conditions()

    def accept_terms_and_conditions(self):
        self._hide_keyboard()
        while str(self.btn_terms_and_conditions().get_attribute("checked")) == "false":
            self.log_info("State of T&A is: " + str(self.btn_terms_and_conditions().get_attribute("checked")))
            self.click(element=self.btn_terms_and_conditions(), screenshot=True)

    def submit_registration_form(self):
        self._hide_keyboard()
        self._short_swipe_down(duration=1000)
        self._short_swipe_down(duration=1000)
        self.click(element=self.btn_submit())

    def cancel_registration_form(self):
        self._hide_keyboard()
        self.click(element=self.btn_navigate_up())

    def _swipe_datepicker_down(self, element):
        """
        just swipes the element up a little to change it
        """
        loc = element.location
        size = element.size

        startx = loc['x'] + size['width'] / 2
        endx = startx
        starty = loc['y'] + size['height'] / 2
        endy = starty + 200
        duration = 800

        if endy < 5:
            endy = 5
            duration = 600

        self.swipe(startx, starty, endx, endy, duration)
        sleep(1)

    def _swipe_list_years(self, element):
        loc = element.location
        size = element.size

        startx = loc['x'] + size['width'] / 2
        endx = startx
        starty = loc['y'] + 20
        endy = loc['y'] + size['height']
        duration = 800

        self.swipe(startx, starty, endx, endy, duration)
        sleep(1)

    def select_sign_in_from_text_link(self):
        self.event._log_info(self.event._event_data('Select Sign In'))
        if not self.exists(element=self.btn_already_have_an_account_sign_in()):
            self._short_swipe_down(duration=1000)
            self._short_swipe_down(duration=1000)
            self._short_swipe_down(duration=1000)
        elem = self.btn_already_have_an_account_sign_in()
        self.click_by_location(elem, side='right')
        sleep(3)
        self._hide_keyboard()