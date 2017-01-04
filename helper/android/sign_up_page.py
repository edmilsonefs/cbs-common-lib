from time import sleep

from helper.cbs import CommonHelper


class SignUpPage:
    helper = None

    def __init__(self, driver):
        self.driver = driver
        self.helper = CommonHelper(driver)

    def first_name(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtFirstName')

    def last_name(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtLastName')

    def email(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtEmail')

    def email_confirm(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtConfirmEmail')

    def password(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtPassword')

    def password_confirm(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/editConfirmPassword')

    def submit(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/btnSignUp')

    def state(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/spnState')

    def zip(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtZipCode')

    def gender(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/spnGender')

    def birth_date(self, timeout=10):
        return self.helper.get_element(timeout=timeout, id=self.helper.com_cbs_app + ':id/edtBirthdate')

    def terms_and_conditions(self, timeout=10):
        return self.helper.get_element(timeout=timeout, class_name='android.widget.CheckBox')

    def validate_page(self):
        self.helper._hide_keyboard()
        if self.helper.phone:
            self.helper.verify_exists(name='Sign Up')
        self.helper.verify_exists(name='Sign up with your social account', screenshot=True)
        self.helper.verify_exists(id=self.helper.com_cbs_app + ':id/imgFacebook')
        self.helper.verify_exists(id=self.helper.com_cbs_app + ':id/imgTwitter')
        if "KFTBWI" not in self.helper.testdroid_device:
            self.helper.verify_exists(id=self.helper.com_cbs_app + ':id/imgGoogle')
        self.helper.verify_exists(name='Sign up with your email')
        for _ in range(0, 2):
            self.helper._short_swipe_down()
        self.helper.verify_exists(name='Sign Up', screenshot=True)
        self.helper.verify_exists(name='Already have an account? Sign In')

    def register_new_user(self, year=1996):
        self.helper._hide_keyboard()

        for _ in range(0, 2):
            self.helper._short_swipe_up()

        self._register_user_part_1()
        self._register_user_part_2(year)
        self._register_user_part_3()
        self._register_user_part_4()
        self.submit_registration_form()

    def _register_user_part_1(self):

        ##### PART A: first/last/email/pwd #####

        self.fn_str = self.helper.generate_random_string()
        self.ln_str = self.helper.generate_random_string()
        email_str = "TestA%s@gmail.com" % self.helper.generate_random_string()

        first_name = self.first_name()
        self.helper.send_keys(data=self.fn_str, element=first_name)
        self.helper._hide_keyboard()

        # while not self._verify_sent_text(first_name, self.fn_str):
        #     self.send_keys(data=self.fn_str + "\n", element=first_name)

        last_name = self.last_name()
        self.helper.send_keys(data=self.ln_str, element=last_name)
        self.helper._hide_keyboard()

        # while not self._verify_sent_text(last_name, self.ln_str):
        #     self.send_keys(data=self.ln_str + "\n", element=last_name)

        email = self.email()
        self.helper.send_keys(data=email_str, element=email, screenshot=True)
        self.helper._hide_keyboard()

        # while not self._verify_sent_text(email, email_str):
        #     self.send_keys(data=email_str + "\n", element=email)

        email_confirm = self.email_confirm()
        self.helper.send_keys(data=email_str, element=email_confirm, screenshot=True)
        self.helper._hide_keyboard()

        # while not self._verify_sent_text(email_confirm, email_str):
        #     self.send_keys(data=email_str + "\n", element=email_confirm)

        if self.helper.phone:
            self.helper.swipe_element_to_top_of_screen(email_confirm, endy=400)

        pwd = self.password()
        self.helper.send_keys('abcdef', pwd)
        self.helper._hide_keyboard()

        pwd_confirm = self.password_confirm()
        self.helper.send_keys('abcdef', pwd_confirm, screenshot=True)
        self.helper._hide_keyboard()

        if self.helper.phone:
            self.helper.swipe_element_to_top_of_screen(pwd_confirm, endy=300)

    def _register_user_part_2(self, year=1996):
        self.birth_date().click()

        if self.helper.exists(id='android:id/date_picker_header_year', timeout=10):
            self.helper.click(id='android:id/date_picker_header_year', data='Click on current year')
            list_years = self.helper._find_element(id='android:id/animator')

            for _ in range(5):
                self._swipe_list_years(list_years)

            years = self.driver.find_elements_by_class_name("android.widget.TextView")

            self.helper.click(element=years[5], data='Choose year from the list')
            self.helper.click(name='OK')
        elif self.helper.exists(id='android:id/date_picker_year', timeout=10):
            self.helper.click(id='android:id/date_picker_year', data='Click on current year')
            list_years = self.helper._find_element(id='android:id/animator')

            for _ in range(5):
                self._swipe_list_years(list_years)

            years = self.driver.find_elements_by_class_name("android.widget.TextView")

            self.helper.click(element=years[5], data='Choose year from the list')
            self.helper.click(name='OK')
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

            self.helper.click(element=elem, data='Choose the date')

            self.driver.implicitly_wait(self.helper.default_implicit_wait)

    def _register_user_part_3(self):
        self.helper.click(name='Male')
        try:
            self.driver.find_element_by_name('Alaska')
            self.helper.click(name='Alaska')
        except:
            self.helper.click(id=self.helper.com_cbs_app + ':id/spnState')
            self.helper.click(name='Alaska')

    def _register_user_part_4(self):
        # I think using the resource id is generally not advised because it's just part of the app's implementation
        # and could be changed at any time.  Here we get it dynamically just so we're sure we get the same element
        # after updating it to a new value
        zip = self.zip()

        zip_text = zip.text

        self.helper.send_keys('78704', zip)
        sleep(2)

        zip = self.zip()

        self.helper.verify_not_equal(zip_text, zip.text, screenshot=True)

        if self.helper.phone:
            self.helper.swipe_element_to_top_of_screen(zip)

        self.terms_and_conditions().click()

    def submit_registration_form(self):
        self.helper._hide_keyboard()
        self.submit().click()

    def cancel_registration_form(self):
        self.helper._hide_keyboard()
        self.helper.navigate_up()

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

        self.helper.swipe(startx, starty, endx, endy, duration)
        sleep(1)

    def _swipe_list_years(self, element):
        loc = element.location
        size = element.size

        startx = loc['x'] + size['width'] / 2
        endx = startx
        starty = loc['y'] + 20
        endy = loc['y'] + size['height']
        duration = 800

        self.helper.swipe(startx, starty, endx, endy, duration)
        sleep(1)
