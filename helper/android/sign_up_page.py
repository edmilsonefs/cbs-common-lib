from time import sleep

from helper.android.base_page import BasePage


class SignUpPage(BasePage):
    def __init__(self, driver, event):
        super(SignUpPage, self).__init__(driver, event)

    def facebook_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgFacebook')

    def twitter_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgTwitter')

    def google_button(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgGoogle')

    def first_name(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtFirstName')

    def last_name(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtLastName')

    def email(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtEmail')

    def email_confirm(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtConfirmEmail')

    def password(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtPassword')

    def password_confirm(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/editConfirmPassword')

    def submit(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/btnSignUp')

    def state(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/spnState')

    def zip(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtZipCode')

    def gender(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/spnGender')

    def birth_date(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/edtBirthdate')

    def terms_and_conditions(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/chkAccountAgreement')

    def already_have_an_account_sign_in(self, timeout=10):
        return self.get_element(timeout=timeout, name='Already a subscriber? Sign In')

    def validate_page(self):
        self._hide_keyboard()
        if self.phone:
            self.verify_exists(name='Sign Up')
        self.verify_exists(name='Sign up with your social account', screenshot=True)
        self.verify_exists(id=self.com_cbs_app + ':id/imgFacebook')
        self.verify_exists(id=self.com_cbs_app + ':id/imgTwitter')
        if not self.IS_AMAZON:
            self.verify_exists(id=self.com_cbs_app + ':id/imgGoogle')
        self.verify_exists(name='Sign up with your email')
        for _ in range(0, 2):
            self._short_swipe_down()
        self.verify_exists(name='Sign Up', screenshot=True)
        self.verify_exists(name='Already have an account? Sign In')

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

        first_name = self.first_name()
        self.send_keys(data=fn_str, element=first_name)
        self._hide_keyboard()

        last_name = self.last_name()
        self.send_keys(data=ln_str, element=last_name)
        self._hide_keyboard()

        email = self.email()
        self.send_keys(data=email_str, element=email, screenshot=True)
        self._hide_keyboard()

        email_confirm = self.email_confirm()
        self.send_keys(data=email_str, element=email_confirm, screenshot=True)
        self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(email_confirm, endy=400)

        pwd = self.password()
        self.send_keys('abcdef', pwd)
        self._hide_keyboard()

        pwd_confirm = self.password_confirm()
        self.send_keys('abcdef', pwd_confirm, screenshot=True)
        self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(pwd_confirm, endy=300)

        return fn_str, ln_str

    def _register_user_part_2(self, year=1996):
        self.birth_date().click()

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
        try:
            self.driver.find_element_by_name('Alaska')
            self.click(name='Alaska')
        except:
            self.click(id=self.com_cbs_app + ':id/spnState')
            self.click(name='Alaska')

    def _register_user_part_4(self):
        # I think using the resource id is generally not advised because it's just part of the app's implementation
        # and could be changed at any time.  Here we get it dynamically just so we're sure we get the same element
        # after updating it to a new value
        zip = self.zip()

        zip_text = zip.text

        self.send_keys('78704', zip)
        sleep(2)

        zip = self.zip()

        self.verify_not_equal(zip_text, zip.text, screenshot=True)

        self._hide_keyboard()

        if self.phone:
            self.swipe_element_to_top_of_screen(zip)

        self.accept_terms_and_conditions()

    def accept_terms_and_conditions(self):
        self._hide_keyboard()
        while str(self.terms_and_conditions().get_attribute("checked")) == "false":
            self.log_info("State of T&A is: " + str(self.terms_and_conditions().get_attribute("checked")))
            self.click(element=self.terms_and_conditions(), screenshot=True)

    def submit_registration_form(self):
        self._hide_keyboard()
        self.submit().click()

    def cancel_registration_form(self):
        self._hide_keyboard()
        self.navigate_up()

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

        if (endy < 5):
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
        elem = self.already_have_an_account_sign_in()
        self.click_by_location(elem, side='right')
        sleep(3)
        self._hide_keyboard()