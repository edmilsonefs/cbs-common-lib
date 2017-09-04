from time import sleep
from helper.cbs import CommonHelper as CommonHelperAndroid
from helper.ios_cbs import CommonIOSHelper as CommonHelperIOS
from helper.android.home_page import HomePage as HomePageAndroid
from helper.android.settings_page import SettingsPage as SettingsPageAndroid
from helper.android.shows_page import ShowsPage as ShowsPageAndroid
from helper.android.show_page import ShowPage as ShowPageAndroid
from helper.android.live_tv_page import LiveTvPage as LiveTvPageAndroid
from helper.android.upsell_page import UpsellPage as UpsellPageAndroid
from helper.android.sign_in_page import SignInPage as SignInPageAndroid
from helper.android.sign_up_page import SignUpPage as SignUpPageAndroid
from helper.android.schedule_page import SchedulePage as SchedulePageAndroid
from helper.android.movies_page import MoviesPage as MoviesPageAndroid
import os


class Validations(CommonHelperAndroid, CommonHelperIOS):
    home_page_android = None
    settings_page_android = None
    shows_page_android = None
    show_page_android = None
    live_tv_page_android = None
    upsell_page_android = None
    sign_in_page_android = None
    sign_up_page_android = None
    schedule_page_android = None
    movies_page_android = None

    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()
        self.home_page_android = HomePageAndroid(self.driver, self.event)
        self.settings_page_android = SettingsPageAndroid(self.driver, self.event)
        self.shows_page_android = ShowsPageAndroid(self.driver, self.event)
        self.show_page_android = ShowPageAndroid(self.driver, self.event)
        self.live_tv_page_android = LiveTvPageAndroid(self.driver, self.event)
        self.upsell_page_android = UpsellPageAndroid(self.driver, self.event)
        self.sign_in_page_android = SignInPageAndroid(self.driver, self.event)
        self.sign_up_page_android = SignUpPageAndroid(self.driver, self.event)
        self.schedule_page_android = SchedulePageAndroid(self.driver, self.event)
        self.movies_page_android = MoviesPageAndroid(self.driver, self.event)

    def validation_a(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name=' Welcome to the CBS app ', screenshot=True)
            CommonHelperAndroid.verify_exists(name='By using this CBS Application, you agree to our:')
            CommonHelperAndroid.verify_exists(name=' Terms of Use ')
            CommonHelperAndroid.verify_exists(name=' Mobile User Agreement ')
            CommonHelperAndroid.verify_exists(name=' Privacy Policy ')
            CommonHelperAndroid.verify_exists(name=' Video Services ')
            CommonHelperAndroid.verify_exists(name='Accept')

    def validation_b(self):
        if self.IS_ANDROID:
            self.home_page_android.validate_page()
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Main Menu', timeout=25, screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white', timeout=25)
            CommonHelperIOS.verify_exists(id='Marquee', timeout=10)
            CommonHelperIOS.verify_exists(id='Search', timeout=10)

    def validation_d(self):
        if self.IS_ANDROID:
            self.sign_in_page_android.validate_page()
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='SIGN IN')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(id='Sign in with your social account', screenshot=True)
            CommonHelperIOS.verify_exists(id='Sign in with your email')
            if self.is_xcuitest():
                CommonHelperIOS.verify_exists(
                    xpath='//XCUIElementTypeStaticText[@name="Don\'t have an account? Sign Up"])[2]')
            else:
                CommonHelperIOS.verify_exists(id="Don\'t have an account? Sign Up")

    def validation_e(self):
        if self.IS_ANDROID:
            self.sign_up_page_android.validate_page()
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Sign in with your social account')
            CommonHelperIOS.verify_exists(id='Sign Up')
            # TODO Close icon? Only id = Back button is present
            CommonHelperIOS.verify_exists(id='FacebookLogo')
            CommonHelperIOS.verify_exists(id='TwitterLogo')
            CommonHelperIOS.verify_exists(id="GooglePlusLogo")
            CommonHelperIOS.verify_exists(id='Sign up with your email')
            CommonHelperIOS.verify_exists(id='Already have an account? Sign In')
            self.swipe_element_to_bottom_of_screen()
            try:
                CommonHelperIOS.verify_exists(id='SIGN UP')
            except:
                print('could not swipe')

    def validation_f(self):  # TODO update Validation.
        if self.user_type == self.anonymous:
            CommonHelperIOS.verify_exists(id='Sign In', screenshot=False)
        CommonHelperIOS.verify_exists(id="Settings")
        CommonHelperIOS.verify_exists(id='Home')
        CommonHelperIOS.verify_exists(id='Shows')
        CommonHelperIOS.verify_exists(id='Live TV')
        # CommonHelperIOS.verify_exists(id='Movies')
        CommonHelperIOS.verify_exists(id='Schedule')
        # CommonHelperIOS.verify_exists(name='My CBS')
        CommonHelperIOS.verify_exists(id='Store')

        # Show Page

    def validation_h(self, user_type="anonymous"):
        if self.IS_ANDROID:
            self.show_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            # sleep(20)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id="Search")
            # sleep(10)
            CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')  # ShowImage
            # TODO Add to MyCBS button, not present in xml tree
            # self.verify_share_icon()
            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                CommonHelperIOS.verify_search_episode_count()
                CommonHelperIOS.verify_show_episode_indicator()

            if self.user_type in [self.subscriber, self.trial, self.cfs_subscriber]:
                CommonHelperIOS.verify_show_cards_not_exist()

    def validation_i(self):  # TODO update validation
        CommonHelperIOS.verify_exists(id='Watch Episode', screenshot=False)
        CommonHelperIOS.verify_exists(id='More From Show')
        CommonHelperIOS.verify_exists(id='Close')

        # Schedule Page

    def validation_k(self):
        if self.IS_ANDROID:
            self.schedule_page_android.validate_page()
        elif self.IS_IOS:
            pass

    def validation_l(self):  # TODO update validation
        self.close_big_advertisement()
        CommonHelperIOS.verify_exists(xpath="//UIAButton[@name='Add to My CBS' or @name='Remove from My CBS']", screenshot=True)
        CommonHelperIOS.verify_exists(id='Share')
        CommonHelperIOS.verify_exists(id='Cancel')

        # Shows Page

    def validation_m(self, category='All Shows'):  # TODO update validation
        if self.IS_ANDROID:
            self.shows_page_android.validate_page(category)
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id="Main Menu", screenshot=False)
            CommonHelperIOS.verify_exists(id='Shows')
            CommonHelperIOS.verify_exists(id='Search')
            CommonHelperIOS.verify_exists(id='I want to see: %s' % category)

    def validation_n(self):
        CommonHelperIOS.verify_exists(name='All Shows', screenshot=False)
        CommonHelperIOS.verify_exists(name='Featured')
        CommonHelperIOS.verify_exists(name='Primetime')
        CommonHelperIOS.verify_exists(name='Daytime')
        CommonHelperIOS.verify_exists(name='Late Night')
        CommonHelperIOS.verify_exists(name='Specials')
        CommonHelperIOS.verify_exists(name='News')
        CommonHelperIOS.verify_exists(name='Classics')

    def validation_o(self):  # TODO update validation
        CommonHelperIOS.verify_exists(id='com.cbs.app:id/showInfo', screenshot=False)

    def validation_p(self):
        CommonHelperIOS.verify_exists(name='Like on Facebook', screenshot=False)
        CommonHelperIOS.verify_exists(name='Follow on Twitter')
        CommonHelperIOS.verify_exists(name='Share')
        CommonHelperIOS.verify_exists(name='Add to Calendar')
        CommonHelperIOS.verify_exists(name='Show Info')

        # Settings Page

    def validation_q(self):  # TODO update validation
        if self.IS_ANDROID:
            self.settings_page_android.validate_page()
        elif self.IS_IOS:
            sleep(3)
            # if self.user_type in [self.subscriber, self.trial, self.cf_subscriber]:
            #     CommonHelperIOS.verify_exists(name='Subscription')
            # else:
            #     CommonHelperIOS.verify_exists(name='Subscribe')

            if self.phone:
                if self.user_type == self.anonymous:
                    CommonHelperIOS.verify_not_exists(id="Sign Out", timeout=10, screenshot=True)
                else:
                    CommonHelperIOS.verify_exists(id="Sign Out", screenshot=True)
            else:
                if self.user_type != self.anonymous:
                    CommonHelperIOS.verify_exists(id="Sign Out", screenshot=True)
            CommonHelperIOS.verify_exists(xpath="//UIATableCell[contains(@name,'App Version')]")
            if self.phone:
                CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Send Feedback']")
            else:
                CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Help']")
            CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Terms Of Use']")
            CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Privacy Policy']")
            CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Mobile User Agreement']")
            CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Video Services']")
            # if self.phone:
            #     CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Nielsen Info & Your Choices']")
            # else:
            #     CommonHelperIOS.verify_exists(xpath="//UIATableCell[@name='Nielsen Info']")

    def validation_t(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_show_cards_exist()

            # Live TV Page

    def validation_u(self, user_type="anonymous"):  # TODO update validation, Updated for IOS
        # Upsell Page
        if self.IS_ANDROID:
            self.live_tv_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            # This goes until you can find possible differences between users. This saves time.
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='Live TV')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(id='Two ways to watch Live TV')
            CommonHelperIOS.verify_exists(id='Take the tour')
            CommonHelperIOS.verify_exists(id='OR')
            CommonHelperIOS.verify_exists(id='TV PROVIDER')
            CommonHelperIOS.verify_exists(id='VERIFY NOW')
            CommonHelperIOS.verify_exists(id='Learn More')

            if self.user_type == self.anonymous:
                # CommonHelperIOS.verify_exists(id='Already have an account? Sign In')  # not being able to get element id
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')

            if self.user_type == self.ex_subscriber:
                CommonHelperIOS.verify_exists(id='GET STARTED')
                CommonHelperIOS.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_not_exists(id='Already have an account? Sign In')
            try:
                CommonHelperIOS.driver.find_element_by_id('Learn more')
            except:
                CommonHelperIOS.short_swipe_down()

            if self.user_type == self.subscriber:
                if self.phone:
                    CommonHelperIOS.verify_exists(id='Start Watching')
                else:
                    if self.is_xcuitest():
                        CommonHelperIOS.verify_exists(
                            xpath='//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]')  # Schedule
                        CommonHelperIOS.verify_exists(
                            xpath='//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage')  # Video Image

    def validation_v(self, user_type="anonymous"):
        if self.IS_ANDROID:
            self.upsell_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered]:
                CommonHelperIOS.verify_exists(
                    xpath="//UIAStaticText[contains(@name,'LIMITED') and contains(@name,'COMMERCIALS')]")
            CommonHelperIOS.verify_exists(element=self.get_element(id='TRY 1 WEEK FREE'))
            CommonHelperIOS.verify_exists(xpath="//UIAStaticText[contains(@name,'COMMERCIAL FREE')]")
            CommonHelperIOS.verify_exists(element=self.get_element(id='GET STARTED'))
            if user_type == self.registered:
                CommonHelperIOS.verify_not_exists(name='SELECT', timeout=10)
            elif user_type in [self.subscriber, self.trial]:
                CommonHelperIOS.verify_exists(xpath="//UIAStaticText[contains(@name,'COMMERCIAL FREE')]")
                CommonHelperIOS.verify_exists(xpath="//UIButton[contains(@name,'UPGRADE')]")
            elif user_type == self.cf_subscriber:
                CommonHelperIOS.verify_exists(xpath="//UIAStaticText[contains(@name,'COMMERCIAL FREE')]")
            else:
                if user_type == self.ex_subscriber:
                    CommonHelperIOS.verify_exists(
                        xpath="//UIAStaticText[contains(@name,'LIMITED') and contains(@name,'COMMERCIALS')]", timeout=20)
                    CommonHelperIOS.verify_exists(xpath="//UIAStaticText[contains(@name,'COMMERCIAL FREE')]", timeout=20)
                    CommonHelperIOS.verify_exists(xpath="//UIAStaticText[contains(@name,'Only $5.99/month')]", timeout=20)
                    CommonHelperIOS.verify_exists(id='SELECT', timeout=20)
                    CommonHelperIOS.verify_not_exists(element=self.get_element(id='GET STARTED'), timeout=10)
                    CommonHelperIOS.verify_not_exists(element=self.get_element(id='TRY 1 WEEK FREE'), timeout=10)

    def validation_w(self, error_number):
        if self.IS_ANDROID:
            dict_errors = {"a": "You must provide a first name.",
                           "b": "You must provide a last name.",
                           "c": "You must provide an email.",
                           "d": "You must provide a valid email.",
                           "e": "Your email must match your confirmation email.",
                           "f": "You must provide a password.",
                           "g": "Your password must match your confirmation password.",
                           "h": "You must provide a zip code.",
                           "i": "You must accept the terms and conditions.",
                           "j": "Password must contain at least 6 characters.",
                           "k": "You must provide a ZIP Code.",
                           "l": "Email already exists.",
                           "m": "We are sorry, but we are unable to create an account for you at this time."}

            CommonHelperAndroid.verify_exists(name=dict_errors[error_number], screenshot=True)
        elif self.IS_IOS:
            dict = {
                "a": "First Name Required",
                "b": "Last Name Required",
                "c": "Valid Email Required",
                "e": "Password Required",
                "g": "Birthday Required",
                "h": "Gender Requested",
                "j": "Valid ZIP Required",
                "k": "Emails Must Match",
                "l": "Password Must Be At Least 6 Characters",
                "m": "Passwords Must Match",
                "n": "We found the following errors with your registration",
                "o": "The email you entered is already associated with an account. Please click below to sign into your account",
                # "n": "Account Already Exists",
                # "o": "This email has already been registered. Please sign In to your account to enjoy watching All Access.",
            }

            page_source = self.driver.page_source

            counter = 0
            for error in error_number:
                if counter == 0:
                    CommonHelperIOS.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s should be visible" % dict[error])
                else:
                    CommonHelperIOS.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s should be visible" % dict[error])
                counter += 1

    def validation_x(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='Sign Up')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(id='Please complete your registration')
            CommonHelperIOS.verify_exists(id='CONTINUE')

    def validation_xf(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='Sign up with your Facebook account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
                CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_xt(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='Sign up with your Twitter account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_xg(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='Sign up with your Google account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_y(self, error_number):  # TODO update validation
        if self.IS_ANDROID:
            dict_errors = {"a": "You must provide an email.",
                           "b": "You must provide a valid email.",
                           "c": "You must provide a password.",
                           "d": "Invalid username/password.",
                           "e": "You need to accept our terms in order to continue.",
                           "f": "Our Terms Have Changed",
                           "g": "By registering you become a member of the CBS Interactive family of sites and you have "
                                "read and agree to the Terms of Use, Privacy Policy and Video Services Policy. "
                                "You understand that on occasion, you will receive updates, alerts and promotions from "
                                "CBS. You agree that CBS may share information about you with companies that provide "
                                "content, products or services featured on CBS sites so that they may contact "
                                "you about their products or services."}

            CommonHelperAndroid.verify_exists(name=dict_errors[error_number], screenshot=True)
        elif self.IS_IOS:
            dict = {
                "a": "Invalid email and/or password.",
            }

            counter = 0
            page_source = self.driver.page_source
            for error in error_number:
                if counter == 0:
                    CommonHelperIOS.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s is absent" % dict[error])
                else:
                    CommonHelperIOS.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s is absent" % dict[error])
                counter += 1

    def validation_z(self):
        if self.IS_ANDROID:
            CommonHelperIOS.verify_not_exists(name='paid')
        elif self.IS_IOS:
            pass

    def validation_aa(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            pass  # TODO

    def validation_ab(self, name):
        if self.IS_ANDROID:
            CommonHelperAndroid.open_drawer()
            CommonHelperAndroid.verify_exists(name=name, screenshot=True)
        elif self.IS_IOS:
            CommonHelperIOS.open_drawer()
            self.assertTrue(name in self.driver.page_source,
                            msg="Username should be visible in the menu after registration", screenshot=True)

    def validation_ac(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            pass

    def validation_ad(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            pass

    def validation_ae(self, mvpd=False):
        if self.IS_ANDROID:
            # cbs logo
            CommonHelperAndroid.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/action_search')
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/imgStationLogo')
            if mvpd:
                CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
            else:
                CommonHelperAndroid.verify_not_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/programsContentFlipper')  # schedule table
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='CBSEye_white', screenshot=True)
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(xpath=self.element_type + 'TextView[1]')  # schedule table
            if self.is_xcuitest():  # iOS 10 switch
                CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeOther/XCUIElementTypeImage[1]')  # station icon
            else:
                CommonHelperIOS.verify_exists(xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[2]')  # station icon
            if self.user_type == self.mvpd_auth:
                if self.is_xcuitest():
                    CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[3]')
                else:
                    CommonHelperIOS.verify_exists(xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[3]')
            else:
                if self.is_xcuitest():
                    CommonHelperIOS.verify_not_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[3]')
                    # else:
                    #     CommonHelperIOS.verify_exists(xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[3]')
                    # provider logo is not visible but element is on page source so it gives a false fail

    def validation_af(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='CBS', screenshot=True)
            CommonHelperAndroid.verify_exists(
                name='Sorry, the video you would like to watch is not available in the CBS app at this time.')
            CommonHelperAndroid.verify_exists(name='OK')

    def validation_ag(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')  # cbs icon
            CommonHelperIOS.verify_exists(id='Live TV')
            CommonHelperIOS.verify_exists(id='Two ways to watch Live TV')
            CommonHelperIOS.verify_exists(id='Instantly watch your local CBS station at home or on the go!')
            CommonHelperIOS.verify_exists(id='Stream Live TV plus thousands of full episodes on demand.', timeout=30)
            CommonHelperIOS.verify_exists(
                id='Take the tour')  # TODO Take the tour on Simulator, in Spec - Take a tour  (in spec for validation_u there is take the tour). Need clarification
            CommonHelperIOS.verify_exists(id='OR')
            CommonHelperIOS.verify_exists(id='TV PROVIDER')
            CommonHelperIOS.verify_exists(id='Stream Live TV with your cable, satellite or telco provider.')
            CommonHelperIOS.verify_exists(id='VERIFY NOW')
            CommonHelperIOS.verify_exists(id='Learn More')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='Where is Live TV Available')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='Live TV is available for over 90% of the country and growing.')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='CHECK AVAILABILITY')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='What You Get with Live TV')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='You don\'t have to worry about missing a minute of' /
                                                    'your favorite shows. Stream your local news, hit CBS shows, special events like The' /
                                                    'GRAMMYs and select sporting events at home or on the go across devices.')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='SEE DEVICES')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='Questions?')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='READ OUR FAQ')
            CommonHelperIOS.swipe_down_and_verify_if_exists(id='Disclaimer')
            CommonHelperIOS.swipe_down_and_verify_if_exists(
                id='Some programming is not available for live streaming through CBS All Access.' /
                   'We are continuing to work towards offering more live programming. In the meantime,' /
                   'when a program is not available to you via CBS All Access, you will see a message that' /
                   'states that the program is currently not available.')
            if self.user_type == self.anonymous:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')

            if self.user_type == self.ex_subscriber:
                CommonHelperIOS.verify_exists(id='GET STARTED')
                CommonHelperIOS.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')
                CommonHelperIOS.verify_not_exists(id='TRY 1 WEEK FREE')

    def validation_ah(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            sleep(8)
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='Live TV')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(xpath=self.element_type + 'StaticText[@name="How to Watch Live TV"]')
            CommonHelperIOS.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Desktops and Laptops"]')
            CommonHelperIOS.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Smartphones and Tablets"]')
            CommonHelperIOS.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Streaming media players"]')
            CommonHelperIOS.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Gaming consoles"]')

    def validation_ai(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.driver.implicitly_wait(5)
            sleep(5)
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='Live TV')
            CommonHelperIOS.verify_exists(id="Search")
            try:
                CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Frequently Asked Questions"]')
            except:
                self.screenshot()
            self.driver.implicitly_wait(30)

    def validation_aj(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id='Live TV')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(id='Check Live TV Availability')
            CommonHelperIOS.verify_exists(
                id='CBS would like to use your current location to determine if Live TV is available in your area.' \
                   'If prompted, please share your location. By using this CBS application, you agree to our Terms of Use,' \
                   'Privacy Policy, and Video Service Policy.')
            CommonHelperIOS.verify_exists(id='CHECK AVAILABILITY')

    def validation_ak(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Success!', screenshot=True)
            CommonHelperIOS.verify_exists(
                xpath="//XCUIElementTypeStaticText[@name='Choose an option below to start streaming live TV.'])[1]")
            CommonHelperIOS.verify_exists(name='OR')
            CommonHelperIOS.verify_exists(name='TV PROVIDER')
            CommonHelperIOS.verify_exists(name='VERIFY NOW')

            if self.is_xcuitest():
                CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeCollectionView')
                CommonHelperIOS.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')
            else:
                CommonHelperIOS.verify_exists(class_name='UIACollectionView')  # schedule

            if self.user_type in [self.anonymous, self.registered]:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
            else:
                CommonHelperIOS.verify_not_exists(id='GET STARTED')

    def validation_al(self):
        if self.IS_ANDROID:
            CommonHelperIOS.verify_exists(name='Sign in with your TV provider to start streaming')
            CommonHelperIOS.verify_exists(id=self.com_cbs_app + ':id/gridRecyclerView', screenshot=True)
            CommonHelperIOS.verify_exists(name='Questions?')
            CommonHelperIOS.verify_exists(name='READ OUR FAQ')
        elif self.IS_IOS:
            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                CommonHelperIOS.verify_exists(id='Sign in with your TV provider to start streaming')
                CommonHelperIOS.verify_exists(id='Questions?')
                CommonHelperIOS.verify_exists(id='READ OUR FAQ')
                CommonHelperIOS.verify_exists(xpath=self.element_type + "CollectionView", screenshot=True)

    def validation_am(self):
        self.event.screenshot(self.screenshot())
        CommonHelperIOS.verify_exists(id='Complete the verification process', screenshot=True)
        CommonHelperIOS.verify_exists(id='Register for a free CBS account to get exclusive benefits including:')
        CommonHelperIOS.verify_exists(id='Personalize experience with My CBS')
        CommonHelperIOS.verify_exists(id='Resume video across apps and web')
        CommonHelperIOS.verify_exists(id='Exclusive content')
        CommonHelperIOS.verify_exists(id='Fan votes and sweepstakes')
        CommonHelperIOS.verify_exists(id='Latest content delivered right to your inbox')
        CommonHelperIOS.verify_exists(id='Sign Up')
        CommonHelperIOS.verify_exists(name='Already have an account? Sign In')

    def validation_ao(self):  # TODO need clarification about TV Unavailable page
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='Sorry, your local CBS station is not currently available', screenshot=True)
            CommonHelperAndroid.verify_exists(
                name='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these Videos:')
            CommonHelperAndroid.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail')
            CommonHelperAndroid.verify_not_exists(name='GET NOTIFIED')
        elif self.IS_IOS:
            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                CommonHelperIOS.verify_exists(id="Sorry, your local CBS station is not currently available", screenshot=True)
                CommonHelperIOS.verify_exists(
                    id='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these videos.')
                # self.verify_exist()  # TODO  video thumbnail
                CommonHelperIOS.verify_not_exists(id='GET NOTIFIED')

    def validation_aq(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Watch Live TV')
            CommonHelperIOS.verify_exists(id='Over 8,500 Episodes on Demand')
            CommonHelperIOS.verify_exists(id='New Episodes on CBS App Next Day')
            CommonHelperIOS.verify_exists(id='TAKE A QUICK TOUR')
            CommonHelperIOS.verify_exists(id='Questions?')
            CommonHelperIOS.verify_exists(id='READ OUR FAQ')

            if self.user_type == self.anonymous:
                CommonHelperIOS.verify_exists(id='Your TV provider is not supported in this area', screenshot=True)
                CommonHelperIOS.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_exists(id='Already have an account? Sign In')
            else:
                CommonHelperIOS.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                CommonHelperIOS.verify_exists(id='Sorry, your TV provider is not supported in this area', screenshot=True)
                CommonHelperIOS.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')

            if self.user_type == self.ex_subscriber:
                CommonHelperIOS.verify_exists(id='Sorry, your TV provider is not supported in your area,', screenshot=True)
                CommonHelperIOS.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                CommonHelperIOS.verify_not_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_exists(id='GET STARTED')

    def validation_as(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            CommonHelperIOS.verify_exists(id='Main Menu', screenshot=True)
            CommonHelperIOS.verify_exists(id='CBSEye_white')
            CommonHelperIOS.verify_exists(id="Search")
            CommonHelperIOS.verify_exists(id='We show that CBS is not authorized for you by your TV provider,')
            CommonHelperIOS.verify_exists(id='but you can sign up for CBS All Access to watch now.')
            CommonHelperIOS.verify_exists(id='CBSAllAccess')
            CommonHelperIOS.verify_exists(id='Watch Live TV')
            CommonHelperIOS.verify_exists(id='Over 8,500 Episodes on Demand')
            CommonHelperIOS.verify_exists(id='TAKE A QUICK TOUR')
            CommonHelperIOS.verify_exists(id='New Episodes on CBS App Next Day')
            CommonHelperIOS.verify_exists(id='Questions?')
            CommonHelperIOS.verify_exists(id='READ OUR FAQ')

            if self.user_type == self.anonymous:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                CommonHelperIOS.verify_exists(id='TRY 1 WEEK FREE')
                CommonHelperIOS.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.ex_subscriber:
                CommonHelperIOS.verify_exists(id='GET STARTED')
                CommonHelperIOS.verify_not_exists(id='Already have an account? Sign In')

    def validation_at(self, user_type="anonymous", category="All Shows"):  # TODO update validation
        if self.IS_ANDROID:
            self.movies_page_android.validate_page(user_type=user_type, category=category)
        elif self.IS_IOS:
            pass

            # Video Validation

    def validation_video(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.accept_popup_video_click()
            try:
                CommonHelperAndroid.click_play_from_beginning()
            except:
                pass
            self.driver.implicitly_wait(60)
            CommonHelperAndroid.verify_exists(id=CommonHelperAndroid.com_cbs_app + ':id/player_activity_frame',
                                              screenshot=True)

            self.driver.back()
        elif self.IS_IOS:
            pass
