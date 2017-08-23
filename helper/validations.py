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
            self.verify_exists(id='Main Menu', timeout=25, screenshot=True)
            self.verify_exists(id='CBSEye_white', timeout=25)
            self.verify_exists(id='Search', timeout=10)

    def validation_d(self):
        if self.IS_ANDROID:
            self.sign_in_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='SIGN IN')
            self.verify_exists(id="Search")
            self.verify_exists(id='Sign in with your social account', screenshot=True)
            self.verify_exists(id='Sign in with your email')
            self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Don\'t have an account? Sign Up"])[2]')

    def validation_e(self):
        if self.IS_ANDROID:
            self.sign_up_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_exists(id='Sign in with your social account')
            self.verify_exists(id='Sign Up')
            # TODO Close icon? Only id = Back button is present
            self.verify_exists(id='FacebookLogo')
            self.verify_exists(id='TwitterLogo')
            self.verify_exists(id="GooglePlusLogo")
            self.verify_exists(id='Sign up with your email')
            self.verify_exists(id='Already have an account? Sign In')
            self.swipe_element_to_bottom_of_screen()
            try:
                self.verify_exists(id='SIGN UP')
            except:
                print('could not swipe')

    def validation_f(self):  # TODO update Validation.
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
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id="Search")
            self.verify_exists(xpath='XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')  # ShowImage
            # TODO Add to MyCBS button, not present in xml tree
            self.verify_share_icon()
            if self.user_type in [self.anonymous, self.registered, self.exsubscriber]:
                self.verify_search_episode_count()
                self.verify_show_episode_indicator()

            if self.user_type in [self.subscriber, self.trial_subscriber, self.cfs_subscriber]:
                #TODO add method verify_show_cards_not_exist() to ios_cbs
                # def verify_show_cards_not_exist(self, screenshot=False):
                #     show_cards = self.get_show_cards()
                #     show_cards_count = len(show_cards)
                #     self.verify_equal(show_cards_count, 0, screenshot)

    def validation_i(self):  # TODO update validation
        self.verify_exists(id='Watch Episode', screenshot=False)
        self.verify_exists(id='More From Show')
        self.verify_exists(id='Close')

    # Schedule Page
    def validation_k(self):
        if self.IS_ANDROID:
            self.schedule_page_android.validate_page()
        elif self.IS_IOS:
            pass

    def validation_l(self):  # TODO update validation
        self.close_big_advertisement()
        self.verify_exists(xpath="//UIAButton[@name='Add to My CBS' or @name='Remove from My CBS']", screenshot=True)
        self.verify_exists(id='Share')
        self.verify_exists(id='Cancel')

    # Shows Page
    def validation_m(self, category='All Shows'):  # TODO update validation
        if self.IS_ANDROID:
            self.shows_page_android.validate_page(category)
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

    def validation_o(self):  # TODO update validation
        self.verify_exists(id='com.cbs.app:id/showInfo', screenshot=False)

    def validation_p(self):
        self.verify_exists(name='Like on Facebook', screenshot=False)
        self.verify_exists(name='Follow on Twitter')
        self.verify_exists(name='Share')
        self.verify_exists(name='Add to Calendar')
        self.verify_exists(name='Show Info')

    # Settings Page
    def validation_q(self):  # TODO update validation
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
    def validation_t(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.verify_show_cards_exist()

    # Live TV Page
    def validation_u(self, user_type="anonymous"):  # TODO update validation, Updated for IOS
        if self.IS_ANDROID:
            self.live_tv_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            # This goes until you can find possible differences between users. This saves time.
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            self.verify_exists(id='Two ways to watch Live TV')
            self.verify_exists(id='Take the tour')
            self.verify_exists(id='OR')
            self.verify_exists(id='TV PROVIDER')
            self.verify_exists(id='VERIFY NOW')
            self.verify_exists(id='Learn More')

            if self.user_type == self.anonymous:
                self.verify_exists(id='Already have an account? Sign In')  # not being able to get element id
                self.verify_exists(id='TRY 1 WEEK FREE')

            if self.user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_not_exists(id='Already have an account? Sign In')
            try:
                self.driver.find_element_by_id('Learn More')
            except:
                self.short_swipe_down()

            if self.user_type == self.subscriber:
                if self.phone:
                    self.verify_exist(id='Start Watching')
                else:
                    self.verify_exist(id='Schedule')
                    self.verify_exist(id='Video player')#TODO need to check with ipad
                    self.mvpd_video_page_validation()#TODO need to check with ipad

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
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s should be visible" % dict[error])
                else:
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s should be visible" % dict[error])
                counter += 1

    def validation_x(self):
        if self.IS_ANDROID:
            pass
        if self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Sign Up')
            self.verify_exists(id="Search")
            self.verify_exists(id='Please complete your registration')
            self.verify_exists(id='CONTINUE')

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
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=True,
                                                  msg="Error message %s is absent" % dict[error])
                else:
                    self.assertTrueWithScreenShot(dict[error] in page_source, screenshot=False,
                                                  msg="Error message %s is absent" % dict[error])
                counter += 1

    def validation_z(self):
        if self.IS_ANDROID:
            self.verify_not_exists(name='paid')
        elif self.IS_IOS:
            pass

    def validation_aa(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            pass  # TODO

    def validation_ab(self, name):
        self.open_drawer()
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name=name, screenshot=True)
        elif self.IS_IOS:
            pass  # TODO

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
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")  # cbs logo
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(id=self.com_cbs_app + ':id/imgStationLogo')
            if mvpd:
                self.verify_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
            else:
                self.verify_not_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
            self.verify_exists(id=self.com_cbs_app + ':id/programsContentFlipper')  # schedule table
        if self.IS_IOS:#TODO update after getting  correct credentials for mvpd
            self.verify_exists(id='CBSEye_white', screenshot=True)
            self.verify_exists(id="Search")
            self.verify_exists(
                xpath='//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]')  # schedule table
            if os.environ.get('AUTOMATION_NAME') == 'XCUITest':  # iOS 10 switch
                self.verify_exists(xpath='//XCUIElementTypeOther/XCUIElementTypeImage[1]')  # station icon
            else:
                self.verify_exists(xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[2]')  # station icon
            if self.user_type == self.mvpd_auth:
                self.verifyt_exists(
                    xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[3]')  # TODO provider logo mvpd failed login ios10
            else:
                self.verify_not_exists(
                    xpath='//UIAApplication[1]/UIAWindow[1]/UIAImage[3]')  # TODO provider logo locator detection ios10


    def validation_af(self):
        if self.IS_ANDROID:
            CommonHelperAndroid.verify_exists(name='CBS', screenshot=True)
            CommonHelperAndroid.verify_exists(
                name='Sorry, the video you would like to watch is not available in the CBS app at this time.')
            CommonHelperAndroid.verify_exists(name='OK')

    def validation_ag(self):
        if self.IS_ANDROID:
            pass
        if self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')  # cbs icon
            self.verify_exists(id='Live TV')
            self.verify_exists(id='Two ways to watch Live TV')
            self.verify_exists(id='Instantly watch your local CBS station at home or on the go!')
            self.verify_exists(id='Stream Live TV plus thousands of full episodes on demand.', timeout=30)
            self.verify_exists(id='Take the tour')#TODO Take the tour on Simulator, in Spec - Take a tour  (in spec for validation_u there is take the tour). Need clarification
            self.verify_exists(id='OR')
            self.verify_exists(id='TV PROVIDER')
            self.verify_exists(id='Stream Live TV with your cable, satellite or telco provider.')
            self.verify_exists(id='VERIFY NOW')
            self.verify_exists(id='Learn More')
            self.swipe_down_and_verify_if_exists(id='Where is Live TV Available')
            self.swipe_down_and_verify_if_exists(id='Live TV is available for over 90% of the country and growing.')
            self.swipe_down_and_verify_if_exists(id='CHECK AVAILABILITY')
            self.swipe_down_and_verify_if_exists(id='What You Get with Live TV')
            self.swipe_down_and_verify_if_exists(id='You don\'t have to worry about missing a minute of'/
                                                    'your favorite shows. Stream your local news, hit CBS shows, special events like The'/
                                                    'GRAMMYs and select sporting events at home or on the go across devices.')
            self.swipe_down_and_verify_if_exists(id='SEE DEVICES')
            self.swipe_down_and_verify_if_exists(id='Questions?')
            self.swipe_down_and_verify_if_exists(id='READ OUR FAQ')
            self.swipe_down_and_verify_if_exists(id='Disclaimer')
            self.swipe_down_and_verify_if_exists(id='Some programming is not available for live streaming through CBS All Access.'/
                                                    'We are continuing to work towards offering more live programming. In the meantime,'/
                                                    'when a program is not available to you via CBS All Access, you will see a message that'/
                                                    'states that the program is currently not available.')
            if self.user_type == self.anonymous:
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')

            if self.user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')
                self.verify_not_exists(id='TRY 1 WEEK FREE')

    def validation_ah(self):
        if self.IS_ANDROID:
            pass
        if self.IS_IOS:
            sleep(5)
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Is there an additional cost required to stream Live TV?"]')
            self.verify_exists(id='There is no additional cost to stream Live TV If you have an All Access '
                                  'subscription or if you verify with your TV provider credentials.')
            self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="How do I find out if my TV provider is participating?"]')
            self.verify_exists(id='To view participating TV providers available in your area, click \"Verify Now\" on the Live TV page')
            self.verify_exists(id='If your TV provider is not listed, don\'t worry. We\'re working hard to add more providers.'/
                                  'You can be notified when we add more providers by signing up for a free CBS account.')
            self.select_verify_exists(xpath='//XCUIElementTypeStaticText[@name="Still have questions?"]')
            self.verify_exists(id='If you have a question that hasn\'t been answered here, please visit our complete FAQ site at cbs.com/help.')



    def validation_ai(self):
        if self.IS_ANDROID:
            pass
        if self.IS_IOS:
            self.driver.implicitly_wait(5)
            sleep(5)
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            try:
                self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Frequently Asked Questions"]')
            except:
                self.screenshot()
            self.driver.implicitly_wait(30)

    def validation_aj(self):
        if self.IS_ANDROID:
            pass
        if self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            self.verify_exists(id='Check Live TV Availability')
            self.verify_exists(id='CBS would like to use your current location to determine if Live TV is available in your area.'\
                                  'If prompted, please share your location. By using this CBS application, you agree to our Terms of Use,'\
                                  'Privacy Policy, and Video Service Policy.')
            self.verify_exists(id='CHECK AVAILABILITY')



    def validation_ak(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.verify_exists(id='Success!', screenshot=True)
            self.verify_exists(xpath="//XCUIElementTypeStaticText[@name='Choose an option below to start streaming live TV.'])[1]")
            self.verify_exists(name='OR')
            self.verify_exists(name='TV PROVIDER')
            self.verify_exists(name='VERIFY NOW')

            if os.environ.get('AUTOMATION_NAME') == 'XCUITest':
                self.verify_exists(xpath='//XCUIElementTypeCollectionView')
                self.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')
            else:
                self.verify_exists(class_name='UIACollectionView')  # schedule

            if self.user_type in [self.anonymous, self.registered]:
                self.verify_exists(id='TRY 1 WEEK FREE')
            else:
                self.verify_not_exists(id='GET STARTED')


    def validation_al(self):
        if self.IS_ANDROID:
            self.verify_exists(name='Sign in with your TV provider to start streaming')
            self.verify_exists(id=self.com_cbs_app + ':id/gridRecyclerView', screenshot=True)
            self.verify_exists(name='Questions?')
            self.verify_exists(name='READ OUR FAQ')
        if self.IS_IOS:
            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(id='Sign in with your TV provider to start streaming')
                self.verify_exists(id='Questions?')
                self.verify_exists(id='READ OUR FAQ')
                if os.environ.get('AUTOMATION_NAME') == 'XCUITest':
                    self.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')
                else:
                    self.verify_exists(xpath="//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]", screenshot=True)


    def validation_am(self):#TODO Account Verified Page - still open question
        self.event.screenshot(self.screenshot())
        # TODO substitute with 'Your account has been verified!'
        self.verify_exists(name='Complete the verification process', screenshot=True)
        self.verify_exists(name='Register for a free CBS account to get exclusive benefits including:')
        self.verify_exists(name='Personalize experience with My CBS')
        self.verify_exists(name='Resume video across apps and web')
        self.verify_exists(name='Exclusive content')
        self.verify_exists(name='Fan votes and sweepstakes')
        self.verify_exists(name='Latest content delivered right to your inbox')
        self.verify_exists(name='Sign Up')
        self.verify_exists(name='Already have an account? Sign In')

    def validation_ao(self):#TODO need clarification about TV Unavailable page
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(id="Sorry, your local CBS station is not currently available", screenshot=True)
                self.verify_exists(id='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these videos.')
                self.verify_exist()#TODO  video thumbnail
                self.verify_not_exists(id='GET NOTIFIED')


    def validation_aq(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.verify_exists(id='Watch Live TV')
            self.verify_exists(id='Over 8,500 Episodes on Demand')
            self.verify_exists(id='New Episodes on CBS App Next Day')
            self.verify_exists(id='TAKE A QUICK TOUR')
            self.verify_exists(id='Questions?')
            self.verify_exists(id='READ OUR FAQ')

            if self.user_type == self.anonymous:
                self.verify_exists(id='Your TV provider is not supported in this area', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_exists(id='Already have an account? Sign In')
            else:
                self.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                self.verify_exists(id='Sorry, your TV provider is not supported in this area', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_exists(id='TRY 1 WEEK FREE')

            if self.user_type == self.ex_subscriber:
                self.verify_exists(id='Sorry, your TV provider is not supported in your area,', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_not_exists(id='TRY 1 WEEK FREE')
                self.verify_exists(id='GET STARTED')


    def validation_as(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id="Search")
            self.verify_exists(id='We show that CBS is not authorized for you by your TV provider,')
            self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
            self.verify_exists(id='CBSAllAccess')
            self.verify_exists(id='Watch Live TV')
            self.verify_exists(id='Over 8,500 Episodes on Demand')
            self.verify_exists(id='TAKE A QUICK TOUR')
            self.verify_exists(id='New Episodes on CBS App Next Day')
            self.verify_exists(id='Questions?')
            self.verify_exists(id='READ OUR FAQ')

            if self.user_type == self.anonymous:
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_exists(id='Already have an account? Sign In')

            if self.user_type == self.registered:
                self.verify_exists(id='TRY 1 WEEK FREE')
                self.verify_not_exists(id='Already have an account? Sign In')

            if self.user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have an account? Sign In')

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
            CommonHelperAndroid.verify_exists(id=CommonHelperAndroid.com_cbs_app + ':id/player_activity_frame', screenshot=True)

            self.driver.back()
        elif self.IS_IOS:
            pass
