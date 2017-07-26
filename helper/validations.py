from time import sleep

from helper.cbs import CommonHelper
from helper.ios_cbs import CommonIOSHelper
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

class Validations(CommonHelper, CommonIOSHelper):

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
            CommonHelper.verify_exists(name='Welcome to the CBS app')
            CommonHelper.verify_exists(name='By using this CBS Application, you agree to our:')
            CommonHelper.verify_exists(name='Terms of Use')
            CommonHelper.verify_exists(name='Mobile User Agreement')
            CommonHelper.verify_exists(name='Privacy Policy')
            CommonHelper.verify_exists(name='Video Services')
            CommonHelper.verify_exists(name='ACCEPT')

    def validation_b(self): #TODO update validation
        if self.user_type in [self.subscriber, self.trial, self.cf_subscriber]:
            self.verify_exists(id='CBSLogo_AllAccess_white', screenshot=False)
        else:
            self.verify_exists(id='CBSLogo_white', screenshot=False)
            self.verify_exists(id="Main Menu")
            self.verify_exists(id='Search')
            # self.verify_exists(id='Marquee', timeout=60) TODO impossible to verify because of sliding

    def validation_d(self): #TODO update validation
        if self.IS_ANDROID:
            self.sign_in_page_android.validate_page()
        elif self.IS_IOS:
            pass

    def validation_e(self): #TODO update validation
        if self.IS_ANDROID:
            self.sign_up_page_android.validate_page()
        elif self.IS_IOS:
            pass

    def validation_f(self): #TODO update Validation.
        if self.user_type == self.anonymous:
            self.verify_exists(id='Sign In', screenshot=False)
        self.verify_exists(id="Settings")
        self.verify_exists(id='Home')
        self.verify_exists(id='Shows')
        self.verify_exists(id='Live TV')
        # self.verify_exists(id='Movies')
        self.verify_exists(id='Schedule')
        # self.verify_exists(name='My CBS')
        self.verify_exists(id='Store')

    # Show Page
    def validation_h(self, user_type="anonymous"):
        if self.IS_ANDROID:
            self.show_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            pass

    def validation_i(self): #TODO update validation
        self.verify_exists(id='Watch Episode', screenshot=False)
        self.verify_exists(id='More From Show')
        self.verify_exists(id='Close')

    # Schedule Page
    def validation_k(self):
        if self.IS_ANDROID:
            self.schedule_page_android.validate_page()
        elif self.IS_IOS:
            pass

    def validation_l(self): # TODO update validation
        self.close_big_advertisement()
        self.verify_exists(xpath="//UIAButton[@name='Add to My CBS' or @name='Remove from My CBS']", screenshot=True)
        self.verify_exists(id='Share')
        self.verify_exists(id='Cancel')

    # Shows Page
    def validation_m(self, category): #TODO update validation
        if self.IS_ANDROID:
            self.shows_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_exists(id="Main Menu", screenshot=False)
            self.verify_exists(id='Shows')
            self.verify_exists(id='Search')
            self.verify_exists(id='I want to see: %s' % category)

    def validation_n(self):
        self.verify_exists(name='All Shows', screenshot=False)
        self.verify_exists(name='Featured')
        self.verify_exists(name='Primetime')
        self.verify_exists(name='Daytime')
        self.verify_exists(name='Late Night')
        self.verify_exists(name='Specials')
        self.verify_exists(name='News')
        self.verify_exists(name='Classics')

    def validation_o(self): #TODO update validation
        self.verify_exists(id='com.cbs.app:id/showInfo', screenshot=False)

    def validation_p(self):
        self.verify_exists(name='Like on Facebook', screenshot=False)
        self.verify_exists(name='Follow on Twitter')
        self.verify_exists(name='Share')
        self.verify_exists(name='Add to Calendar')
        self.verify_exists(name='Show Info')

    # Settings Page
    def validation_q(self): #TODO update validation
        if self.IS_ANDROID:
            self.settings_page_android.validate_page()
        elif self.IS_IOS:
            sleep(3)
            # if self.user_type in [self.subscriber, self.trial, self.cf_subscriber]:
            #     self.verify_exists(name='Subscription')
            # else:
            #     self.verify_exists(name='Subscribe')

            if self.phone:
                if self.user_type == self.anonymous:
                    self.verify_not_exists(id="Sign Out", timeout=10, screenshot=True)
                else:
                    self.verify_exists(id="Sign Out", screenshot=True)
            else:
                if self.user_type != self.anonymous:
                    self.verify_exists(id="Sign Out", screenshot=True)
            self.verify_exists(xpath="//UIATableCell[contains(@name,'App Version')]")
            if self.phone:
                self.verify_exists(xpath="//UIATableCell[@name='Send Feedback']")
            else:
                self.verify_exists(xpath="//UIATableCell[@name='Help']")
            self.verify_exists(xpath="//UIATableCell[@name='Terms Of Use']")
            self.verify_exists(xpath="//UIATableCell[@name='Privacy Policy']")
            self.verify_exists(xpath="//UIATableCell[@name='Mobile User Agreement']")
            self.verify_exists(xpath="//UIATableCell[@name='Video Services']")
            # if self.phone:
            #     self.verify_exists(xpath="//UIATableCell[@name='Nielsen Info & Your Choices']")
            # else:
            #     self.verify_exists(xpath="//UIATableCell[@name='Nielsen Info']")

    # Live TV Page
    def validation_u(self, user_type="anonymous"): #TODO update validation
        if self.IS_ANDROID:
            self.live_tv_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            if user_type in [self.subscriber, self.trial, self.cf_subscriber]:
                self.verify_exists(id="Schedule", screenshot=False)
                self.verify_exists(id="Start Watching")
                self.verify_exists(id="Already have an account? Sign In")
                self.verify_exists(id="VERIFY NOW")
                self.verify_exists(id="TV PROVIDER")
                self.verify_exists(id="Stream Live TV with your cable")
                self.verify_exists(id="satellite or telco provider.")
            else:
                self.verify_exists(id="Two ways to watch Live TV", screenshot=False)
                self.verify_exists(id="Instantly watch your local CBS station at home or on the go!")
                self.verify_exists(xpath="//UIAStaticText[contains(@name,'Get Live TV plus thousands')]")

    # Upsell Page
    def validation_v(self, user_type="anonymous"):
        if self.IS_ANDROID:
            self.upsell_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            pass

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

            CommonHelper.verify_exists(name=dict_errors[error_number], screenshot=True)
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
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s should be visible" % dict[error])
                else:
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s should be visible" % dict[error])
                counter += 1

    def validation_xf(self):
        if self.IS_ANDROID:
            CommonHelper.verify_exists(name='Sign up with your Facebook account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
                CommonHelper.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_xt(self):
        if self.IS_ANDROID:
            CommonHelper.verify_exists(name='Sign up with your Twitter account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            CommonHelper.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_xg(self):
        if self.IS_ANDROID:
            CommonHelper.verify_exists(name='Sign up with your Google account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            CommonHelper.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

    def validation_y(self, error_number): #TODO update validation
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

            CommonHelper.verify_exists(name=dict_errors[error_number], screenshot=True)
        elif self.IS_IOS:
            dict = {
                "a": "Invalid email and/or password.",
            }

            counter = 0
            page_source = self.driver.page_source
            for error in error_number:
                if counter == 0:
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s is absent" % dict[error])
                else:
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s is absent" % dict[error])
                counter += 1

    def validation_ab(self, name):
        self.open_drawer()
        if self.IS_ANDROID:
            CommonHelper.verify_exists(name=name, screenshot=True)
        elif self.IS_IOS:
            pass #TODO

    def validation_ac(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            pass

    def validation_ae(self, mvpd=False):
        self.verify_exists(
            xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']") # cbs logo
        self.verify_exists(id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(id=self.com_cbs_app + ':id/imgStationLogo')
        if mvpd:
            self.verify_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
        else:
            self.verify_not_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
        self.verify_exists(id=self.com_cbs_app + ':id/programsContentFlipper')  # schedule table

    def validation_ag(self, anonymous=False, ex_subscriber=False, registered=False):
        # Tablet has the navigate up icon instead of open navigation drawer icon
        if self.tablet:
            self.verify_exists(name='Navigate up', screenshot=True)
        else:
            self.verify_exists(name='Open navigation drawer', screenshot=True)
        self.verify_cbs_logo()
        self.verify_exists(name='Live TV')
        self.verify_exists(id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(name='Two ways to watch Live TV')
        self.verify_exists(name='Instantly watch your local CBS station at home or on the go!')
        self.verify_exists(id=self.com_cbs_app + ':id/imageView')  # cbs all access
        #TODO should be substituted with 'Get Live TV plus thousands of full episodes on demand.'
        self.verify_exists(name='Stream Live TV plus thousands of full episodes on demand.')
        self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
        if anonymous:
            self.verify_exists(name='Already have an account? Sign In')
            self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
        if registered:
            self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
            self.verify_not_exists(name='Already have CBS ALL ACCESS? Sign In')
        if ex_subscriber:
            self.verify_exists(name='Get Started')
            self.verify_not_exists(name='Already have CBS ALL ACCESS? Sign In')
            self.verify_not_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
        self.swipe_down_and_verify_if_exists(name='OR')
        self.swipe_down_and_verify_if_exists(name='TV PROVIDER')
        #TODO text should be changed to 'Stream CBS live with your cable or satellite provider'
        # TODO still checking swipping down to verify all texts on all devices
        self.swipe_down_and_verify_if_exists(name='Stream Live TV with your cable, satellite or telco provider.', screenshot=True)
        self.swipe_down_and_verify_if_exists(name='Verify Now')
        self.swipe_down_and_verify_if_exists(id_element='com.cbs.app:id/txtLearnMore')
        self.swipe_down_and_verify_if_exists(name='Where is Live TV Available')
        self.swipe_down_and_verify_if_exists(name='Live TV is available for over 90% of the country and growing. ')
        self.swipe_down_and_verify_if_exists(id_element=self.com_cbs_app + ':id/btnCheckAvailability')
        self.swipe_down_and_verify_if_exists(name='How to Watch Live TV')
        self.swipe_down_and_verify_if_exists(name="You don't have to worry about missing a minute of your favorite shows. Stream your local news, hit CBS shows, special events like The GRAMMY's and select sporting events at home or on the go across devices.")
        self.swipe_down_and_verify_if_exists(name='SEE DEVICES')
        self.swipe_down_and_verify_if_exists(name='Questions?')
        self.swipe_down_and_verify_if_exists(name='READ OUR FAQ')
        self.swipe_down_and_verify_if_exists(name='Disclaimer')
        self.swipe_down_and_verify_if_exists(name='Some programming may not be available for live streaming. However, we are continuing to work towards offering more live programming. When a program is not available, you will see a message that states that the program is not currently available.')

    def validation_at(self, user_type="anonymous", category="All Shows"): #TODO update validation
        if self.IS_ANDROID:
            self.movies_page_android.validate_page(user_type=user_type, category=category)
        elif self.IS_IOS:
            pass

    def validation_al(self):
        self.verify_exists(name='Sign in with your TV provider to start streaming')
        self.verify_exists(id=self.com_cbs_app + ':id/gridRecyclerView', screenshot=True)
        self.verify_exists(name='Questions?')
        self.verify_exists(name='READ OUR FAQ')

    def validation_am(self):
        self.event.screenshot(self.screenshot())
        #TODO substitute with 'Your account has been verified!'
        self.verify_exists(name='Complete the verification process', screenshot=True)
        self.verify_exists(name='Register for a free CBS account to get exclusive benefits including:')
        self.verify_exists(name='Personalize experience with My CBS')
        self.verify_exists(name='Resume video across apps and web')
        self.verify_exists(name='Exclusive content')
        self.verify_exists(name='Fan votes and sweepstakes')
        self.verify_exists(name='Latest content delivered right to your inbox')
        self.verify_exists(name='Sign Up')
        self.verify_exists(name='Already have an account? Sign In')
