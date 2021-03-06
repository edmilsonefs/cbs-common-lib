from time import sleep

from helper.android.home_page import HomePage as HomePageAndroid
from helper.android.live_tv_page import LiveTvPage as LiveTvPageAndroid
from helper.android.movies_page import MoviesPage as MoviesPageAndroid
from helper.android.schedule_page import SchedulePage as SchedulePageAndroid
from helper.android.settings_page import SettingsPage as SettingsPageAndroid
from helper.android.show_page import ShowPage as ShowPageAndroid
from helper.android.shows_page import ShowsPage as ShowsPageAndroid
from helper.android.sign_in_page import SignInPage as SignInPageAndroid
from helper.android.sign_up_page import SignUpPage as SignUpPageAndroid
from helper.android.upsell_page import UpsellPage as UpsellPageAndroid
from helper.android.video_page import VideoPage as VideoPageAndroid
from helper.cbs import CommonHelper
from helper.ios_cbs import CommonIOSHelper


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
    video_page_android = None

    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
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
        self.video_page_android = VideoPageAndroid(self.driver, self.event)

        if str(self.driver.capabilities['platformName']).lower() == 'android':
            self.IS_ANDROID = True
            self.IS_IOS = False

            self.init_variables()
        elif str(self.driver.capabilities['platformName']).lower() == 'ios':
            self.IS_ANDROID = False
            self.IS_IOS = True

            Validations.__bases__ = (CommonIOSHelper, CommonHelper)
            if 'iPad' in self.driver.capabilities['deviceName']:
                self.tablet = True
                self.phone = False
            else:
                self.tablet = False
                self.phone = True
            if self.is_xcuitest():
                self.element_type = '//XCUIElementType'  # iOS 10
                self.xcuitest = True

    def validation_a(self):
        if self.IS_ANDROID:
            self.verify_in_batch(['Welcome to the CBS app',
                                  'Before you get started, please review and agree to the following:|By using this CBS Application, you agree to our:',
                                  'Terms of Use',
                                  'Mobile User Agreement',
                                  'Privacy Policy',
                                  'Video Services',
                                  'ACCEPT'])
        elif self.IS_IOS:
            self.verify_in_batch(
                ['By watching this video, you agree to our: |By watching this video or stream, you agree to our: ',
                 'Terms of Use',
                 'Mobile User Agreement',
                 'Privacy Policy',
                 'Video Services',
                 'crossbutton|.*',
                 'I ACCEPT|Accept'], strict_visibility=False)
            # self.verify_exists(id='By watching this video, you agree to our: ', screenshot=True)
            # self.verify_exists(id='Terms of Use')
            # self.verify_exists(id='Mobile User Agreement')
            # self.verify_exists(id='Privacy Policy')
            # self.verify_exists(id='Video Services')
            # self.verify_exists(id='crossbutton')
            # self.verify_exists(id='I ACCEPT')

    def validation_b(self, check_marquee=True):
        if self.IS_ANDROID:
            self.home_page_android.validate_page(check_marquee)
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'Search'])
            # self.verify_exists(id='MarqueeCollectionView', timeout=10) #add home page marquee

    def validation_c(self):
        if self.IS_ANDROID:
            # self.verify_in_batch(['Our Terms Have Changed',
            #                       ':id/terms_accept_checkBox',
            #                       'By registering you become a member of the CBS Interactive family of sites and you have '
            #                       'read and agree to the Terms of Use, Privacy Policy and Video Services Policy. '
            #                       'You understand that on occasion, you will receive updates, alerts and promotions from '
            #                       'CBS. You agree that CBS may share information about you with companies that provide '
            #                       'content, products or services featured on CBS sites so that they may contact '
            #                       'you about their products or services.',
            #                       'CANCEL',
            #                       'SUBMIT'])
            pass
        elif self.IS_IOS:
            self.verify_in_batch(['Search', 'Sign In', 'Our terms have changed', 'CONTINUE'])

    def validation_d(self):
        if self.IS_ANDROID:
            self.sign_in_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_navigation_back_button()  # Cbs logo appear as back button
            self.verify_in_batch(['SIGN IN', 'Sign in with your social account', 'Sign in with your email'],
                                 screenshot=True)
            # self.verify_exists(id="Don't have an account? Sign Up")

    def validation_e(self):
        if self.IS_ANDROID:
            self.sign_up_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_in_batch(['Sign up with your email', 'SIGN UP'])
            # Already have an account? Sign in - doesn't exist on this page

    def validation_f(self, user_type='anonymous', name=None, mvpd=None):
        self.log_info("Validation F")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = ['Home', 'Shows', 'Live TV', 'Movies', 'Schedule', 'Shop', 'Settings']
            if user_type == self.anonymous:
                text_list.append('Sign In')
            else:
                self.verify_exists(name=name)
            if user_type in [self.subscriber, self.trial]:
                text_list.append('Upgrade')
            elif user_type == self.cf_subscriber:
                self.verify_not_exists(name='Upgrade')
                self.verify_not_exists(name='Subscribe')
            else:
                text_list.append('Subscribe')
            if mvpd:
                self.verify_not_exists(name="TV Provider")
            else:
                text_list.append('TV Provider')
            self.verify_in_batch(text_list, False)
        if self.IS_IOS:
            self.safe_screenshot()
            text_list = ['Home', 'Shows', 'Live TV', 'Movies', 'Schedule', 'Store', 'Settings']
            if user_type == self.anonymous:
                text_list.append('Sign In')
                self.verify_exists(xpath='//XCUIElementTypeButton[@name="Subscribe"]')
            else:
                pass
                # self.verify_exists(name=name)

            if user_type in [self.ex_subscriber, self.registered]:
                self.verify_exists(xpath='//XCUIElementTypeButton[@name="Subscribe"]')

            if user_type == self.trial:
                #TODO self.lc_subscriber
                text_list.append('Upgrade')

            elif user_type == self.cf_subscriber:
                self.verify_not_exists(name='Upgrade')
                self.verify_not_exists(xpath='//XCUIElementTypeButton[@name="Subscribe"]')

            if mvpd:
                self.verify_not_exists(name="TV Provider")
            else:
                text_list.append('TV Provider')
            self.verify_in_batch(text_list, False)

            # Show Page

    def validation_g(self, user_type='anonymous'):
        if self.IS_ANDROID:
            if user_type == self.anonymous:
                self.verify_not_exists(name='Continue Watching')
                self.verify_not_exists(name='Shows You Watch')
            else:
                self.verify_exists(name='Continue Watching')
                self.verify_exists(id=self.com_cbs_app + ":id/imgThumbnail")
                self.verify_exists(name='Shows You Watch')
                self.verify_exists(id=self.com_cbs_app + ":id/showImage")

            self.swipe_down_and_verify_if_exists(name="Primetime Episodes")
            counter = 0
            while not self.exists(name="Late Night Episodes") and counter < 10:
                counter += 1
                self.swipe_down_if_element_is_not_visible(name="Late Night Episodes", short_swipe=True)
            self.swipe_down_and_verify_if_exists(name="Late Night Episodes", screenshot=True)
            self.swipe_down_and_verify_if_exists(name="Movies")
            self.swipe_down_and_verify_if_exists(name="Latest Clips")
            self.swipe_down_and_verify_if_exists(name="Popular Clips")
        elif self.IS_IOS:
            self.verify_exists(class_name='XCUIElementTypeImage')

    def validation_h(self, user_type="anonymous", clips=False):
        if self.IS_ANDROID:
            self.close_big_advertisement()
            self.show_page_android.validate_page(user_type=user_type, clips=False)
        elif self.IS_IOS:
            self.verify_navigation_back_button()
            # self.verify_share_icon()
            self.verify_search_icon()
            # self.verify_exists(id='Marquee')  # show image
            # self.verify_star_icon()

    def validation_i(self, show_page=False, home_page=False):
        if self.IS_ANDROID:
            self.verify_exists(id=self.com_cbs_app + ':id/videoThumbnail', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/txtDescription')
            self.verify_exists(name='WATCH EPISODE')
            if home_page:
                self.verify_exists(name='MORE FROM SHOW')
            if show_page:
                self.verify_not_exists(name='MORE FROM SHOW')
        elif self.IS_IOS:
            self.verify_exists(class_name='XCUIElementTypeImage', screenshot=True)
            self.verify_in_batch(['WATCH|RESUME|RESTART', 'CLOSE'])

    def validation_j(self, show_page=False, home_page=False):
        if self.IS_ANDROID:
            # self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/txtDescription')
            self.verify_exists(name='WATCH CLIP')
            if home_page:
                self.verify_exists(name='MORE FROM SHOW')
            if show_page:
                self.verify_not_exists(name='MORE FROM SHOW')
        elif self.IS_IOS:
            self.verify_exists(class_name='XCUIElementTypeImage', screenshot=True)
            self.verify_in_batch(['Watch Clip', 'More From Show', 'Close'])

    # Schedule Page
    def validation_k(self, user_type='anonymous'):
        if self.IS_ANDROID:
            self.schedule_page_android.validate_page()
        elif self.IS_IOS:
            self.close_big_advertisement()
            self.verify_exists(id='Schedule')
            self.verify_exists(id='Search')
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'ET/PT', 'Today'])
            self.close_big_advertisement()

    def validation_l(self):  # TODO update validation
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.close_big_advertisement()
            self.verify_in_batch(['Share', 'Cancel', '(Add to My CBS|Remove from My CBS)'])

            # Shows Page

    def validation_m(self, category='All Shows'):  # TODO update validation
        if self.IS_ANDROID:
            self.shows_page_android.validate_page(category)
        elif self.IS_IOS:
            self.verify_cbs_logo()
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'Search', 'I want to see: %s|%s Menu Dropdown' % (category, category)])
            self.verify_exists(class_name='XCUIElementTypeCell')  # Show card

    def validation_n(self):
        if self.IS_ANDROID:
            self.shows_page_android.validate_all_shows_dropdown_menu()
        elif self.IS_IOS:
            self.verify_in_batch(
                ['All Shows', 'Featured', 'Primetime', 'Daytime', 'Late Night', 'Specials', 'News', 'Classics'])

    def validation_o(self):  # TODO update validation
        if self.IS_ANDROID:
            if self.phone:
                self.verify_exists(id='com.cbs.app:id/showInfo', screenshot=False)
            else:
                self.verify_exists(id='android:id/message', screenshot=True)
        elif self.IS_IOS:
            pass

    def validation_p(self):
        if self.IS_ANDROID:
            self.close_big_advertisement()
            self.verify_in_batch(['Like on Facebook', 'Follow on Twitter', 'Share', 'Add to Calendar', 'Show Info'])
        elif self.IS_IOS:
            self.verify_in_batch(['Like on Facebook', 'Follow on Twitter', 'Share', 'Add to Calendar', 'Show Info'])

    def validation_q(self, user_type='anonymous'):  # TODO update validation
        self.log_info("Validation Q")
        if self.IS_ANDROID:
            self.settings_page_android.validate_page(user_type)
        elif self.IS_IOS:
            self.open_drawer()
            if user_type in [self.subscriber, self.cf_subscriber, self.trial]:
                self.verify_exists(id='Sign Out')
                self.verify_exists(id='Subscription')
            else:
                self.verify_exists(id='Subscribe')

            self.verify_navigation_drawer_button()
            self.verify_cbs_logo()
            self.verify_exists(id='Settings')
            self.verify_in_batch(
                ['App Version', 'Terms Of Use', 'Privacy Policy', 'Mobile User Agreement', 'Video Services'])
            if self.phone:
                self.verify_exists(id='Nielsen Info & Your Choices')
                self.verify_exists(id='Send Feedback')
            else:
                self.verify_exists(id='Nielsen Info')
                self.verify_exists(id='Help')

    def validation_r(self):
        if self.IS_ANDROID:
            self.verify_back_button(screenshot=True)
            self.verify_search_text()

            # todo: Check black background is shown

            # need other implementation to check if keyboard is displayed
            # self.assertTrueWithScreenShot(self.is_keyboard_displayed(), screenshot=True,
            #                               msg="Keyboard SHOULD be displayed")
        elif self.IS_IOS:
            self.verify_cancel_button()
            self.verify_search_field()
            self.verify_exists(id='Search for a Show')
            self.verify_keyboard()

    def validation_s(self):
        if self.IS_ANDROID:
            self.verify_back_button(screenshot=True)
            self.verify_search_clear_button()
            self.verify_no_shows_found_text()

        elif self.IS_IOS:
            self.verify_cancel_button()
            self.verify_search_field()
            self.verify_exists(id="No Shows Found")

    def validation_t(self, show_name=""):
        if self.IS_ANDROID:
            self.verify_movie_poster()
        elif self.IS_IOS:
            self.verify_show_cards_exist(show_name)

            # Live TV Page

    def validation_u(self, user_type="anonymous"):  # TODO update validation, Updated for IOS
        # Upsell Page
        # DEPRECATED
        if self.IS_ANDROID:
            self.live_tv_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            # This goes until you can find possible differences between users. This saves time.
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id="Search")
            self.verify_exists(id='Two ways to watch Live TV')
            self.verify_exists(id='Take the tour')
            self.verify_exists(id='OR')
            self.verify_exists(id='TV PROVIDER')
            self.verify_exists(id='VERIFY NOW')
            self.verify_exists(id='Learn more')

            if user_type == self.anonymous:
                self.verify_exists(
                    xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

            if user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.registered:
                self.verify_exists(
                    xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.subscriber:
                self.verify_exists(accessibility_id='Channels')
                self.verify_exists(accessibility_id='Live Now')

    def validation_v(self, user_type="anonymous"):
        self.log_info("Validation V")
        if self.IS_ANDROID:
            self.click_allow_popup()
            self.upsell_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered]:
                self.verify_exists(id='TRY 1 WEEK FREE')
                if self.exists(id="LIMITED COMMERCIALS"):
                    self.verify_in_batch(['COMMERCIAL FREE', 'LIMITED COMMERCIALS'])
                else:
                    self.verify_in_batch(['Stream 10,000\+ Episodes, Live TV &amp; Exclusive Content'])
                    if user_type == self.anonymous:
                        self.verify_exists(id='Sign In')
                if user_type == self.registered:
                    self.verify_not_exists(id='Sign In')

            if user_type == self.ex_subscriber:
                if self.exists(id="GET STARTED"):
                    self.verify_in_batch(['GET STARTED', 'Stream 10,000\+ Episodes, Live TV &amp; Exclusive Content'])
                else:
                    self.verify_in_batch(['LIMITED COMMERCIALS', 'COMMERCIAL FREE', 'SELECT'])
                self.verify_not_exists(id='Sign In')
                self.verify_not_exists(id='TRY 1 WEEK FREE')

            if user_type in [self.subscriber, self.trial, self.cf_subscriber]:
                if self.exists(id='Manage your subscription at cbs.com/account'):
                    self.verify_exists(id='Manage your subscription at cbs.com/account')
                    self.verify_not_exists(id='Sign In')
                else:
                    self.verify_exists(id='COMMERCIAL FREE')
                    if user_type == self.cf_subscriber:
                        self.verify_not_exists(id="UPGRADE")

    def validation_w(self, error_number):
        if self.IS_ANDROID:
            dict_errors = {"a": "You must provide a first name.",
                           "b": "You must provide a last name.",
                           "c": "You must provide an email.",
                           "d": "You must provide a valid email.",
                           "e": "Your email must match your confirmation email.",
                           "f": "You must provide a password.",
                           "g": "Your password must match your confirmation password.",
                           "h": "You must provide a ZIP Code.",
                           "i": "You must accept the terms and conditions.",
                           "j": "Password must contain at least 6 characters.",
                           "k": "You must provide a ZIP Code.",
                           "l": "Email already exists.",
                           "m": "We are sorry, but we are unable to create an account for you at this time."}

            self.verify_in_batch(dict_errors[error_number], screenshot=True)
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
            # third_party_signup_page
            self.verify_exists(name='Navigate up', screenshot=True)
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")  # cbs icon
            self.verify_exists(name='Sign Up')
        elif self.IS_IOS:
            self.verify_in_batch(
                ['Main Menu|Open CBS Menu', 'CBSEye_white', 'Sign Up', 'Search', 'Please complete your registration', 'CONTINUE'])

    def validation_xf(self):
        if self.IS_ANDROID:
            # self.verify_exists(name='Sign up with your Facebook account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
                self.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'CBSEye_white', 'Sign Up', 'Search', 'Please complete your registration',
                                  'Sign up with your Facebook account', 'CONTINUE'])

    def validation_xt(self):
        if self.IS_ANDROID:
            # self.verify_exists(name='Sign up with your Twitter account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            self.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'CBSEye_white', 'Sign Up', 'Search', 'Please complete your registration',
                                  'Sign up with your Twitter account', 'CONTINUE'])

    def validation_xg(self):
        if self.IS_ANDROID:
            # self.verify_exists(name='Sign up with your Google account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            self.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)

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

            self.verify_exists(name=dict_errors[error_number], screenshot=True)
        elif self.IS_IOS:
            dict_errors = {"a": "Invalid username/password pair",
                           "b": "By registering you become a member of the CBS Interactive family of sites and you have "
                                "read and agree to the Terms of Use, Privacy Policy, and Video Services Policy."
                                " You agree to receive updates, alerts and promotions from CBS and that CBS may share "
                                "information about you with our marketing partners so that they may contact you by "
                                "email or otherwise about their products or services."
                           }

            self.verify_exists(id=dict_errors[error_number])

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
        if self.IS_ANDROID:
            self.open_drawer()
            self.verify_exists(name=name, screenshot=True)
        elif self.IS_IOS:
            self.open_drawer_ios()
            self.click(id='Settings')
            self.click_safe(id='Allow')
            if not self.exists(id='Sign Out'):
                self._short_swipe_down()
            self.verify_exists(id='Sign Out')

    def validation_ac(self, user_type='anonymous'):
        if self.IS_ANDROID:
            if not self.IS_AMAZON:  # TODO skip for Amazon for a while
                # LCS Billing Popup
                self.wait_until_element_is_visible(element_id='com.android.vending:id/item_title')
                sleep(2)
                self.verify_exists(name='Subscribe', timeout=5, screenshot=True)
                if user_type == self.ex_subscriber:
                    self.verify_exists(name='Limited Commercials (CBS - Full Episodes & Live TV)', screenshot=True)

                # if user_type == self.registered:
                # self.verify_exists(xpath='CBS All Access 1 Week FREE (CBS - Full Episodes & Live TV)', screenshot=True)
                # self.verify_exists(xpath="//*[contains(@name,'CBS All Access 1') and contains(@name,'FREE (CBS - Full Episodes & Live TV)') and (contains(@name,'Week') or contains(@name,'Month'))]", screenshot=True)

        if self.IS_IOS:
            pass

    def validation_ad(self):
        # CF Billing Popup
        if self.IS_ANDROID and not self.IS_AMAZON:
            self.wait_until_element_is_visible(element_id='com.android.vending:id/item_title')
            self.verify_exists(name='Subscribe', timeout=20, screenshot=True)
            # self.verify_exists(xpath="//*[contains(@text,''(Commercial Free) and contains(@text,'CBS - Full Episodes')]", screenshot=True)

        elif self.IS_IOS:
            pass

    def validation_ar(self):
        self.log_info("Validation AR")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = ['Navigate up', ':id/action_search', 'Select Your Local Station', 'Channels', 'KWTX',
                         'KBTX', 'You can always change this']
            self.verify_in_batch(text_list)
        elif self.IS_IOS:
            pass

    def validation_ae(self, mvpd=False):
        self.log_info("Validation AE")
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.verify_in_batch(':id/controlsContainer', ':id/station_logo', ':id/liveTvRecyclerView')
            self.verify_exists(name='Channels')
        elif self.IS_IOS:
            # self.verify_exists(id="Search")
            # self.verify_exists(xpath=self.element_type + 'TextView[1]')  # schedule table
            # self.verify_in_batch('CBSEye_white', 'Channels', 'Live Now') #TODO CBSEye (visible:false) & Live Now / Live behaviour is unclear.
            self.verify_in_batch('Channels')

    def validation_af(self):
        self.log_info("Validation AF")
        if self.IS_ANDROID:
            self.verify_exists(name='CBS', screenshot=True)
            self.verify_exists(
                name='Sorry, the video you would like to watch is not available in the CBS app at this time.')
            self.verify_exists(name='OK')

    def validation_ag(self, user_type='anonymous'):
        self.log_info("Validation AG")
        if self.IS_ANDROID:
            self.live_tv_page_android.validate_page(self.user_type)
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'CBSEye_white'])
            # self.verify_exists(id='Live TV')
            # self.verify_exists(id='Two ways to watch Live TV')
            # self.verify_exists(id='Instantly watch your local CBS station at home or on the go!')

            if user_type in [self.anonymous, self.ex_subscriber, self.registered]:
                text_list = ['Stream 10,000\+ Episodes, Live TV &amp; Exclusive Content',
                             '(GET STARTED|TRY 1 WEEK FREE)']
                self.verify_in_batch(text_list)
            # self.verify_exists(id='OR')
            # self.verify_exists(id='TV PROVIDER')
            # self.verify_exists(id='Stream Live TV with your cable, satellite or telco provider.')
            # self.verify_exists(id='VERIFY NOW')
            # self.verify_exists(id='Learn more')
            # self.swipe_down_and_verify_if_exists(id='Where is Live TV Available')
            # self.swipe_down_and_verify_if_exists(id='Live TV is available for over 90% of the country and growing.')
            # self.swipe_down_and_verify_if_exists(id='CHECK AVAILABILITY')
            # self.swipe_down_and_verify_if_exists(id='What You Get with Live TV')
            # self.swipe_down_and_verify_if_exists(id='You don\'t have to worry about missing a minute of' /
            #                                         'your favorite shows. Stream your local news, hit CBS shows, special events like The' /
            #                                         'GRAMMYs and select sporting events at home or on the go across devices.')
            # self.swipe_down_and_verify_if_exists(id='SEE DEVICES')
            # self.swipe_down_and_verify_if_exists(id='Questions?')
            # self.swipe_down_and_verify_if_exists(id='READ OUR FAQ')
            # self.swipe_down_and_verify_if_exists(id='Disclaimer')
            # self.swipe_down_and_verify_if_exists(
            #     id='Some programming is not available for live streaming through CBS All Access.' /
            #        'We are continuing to work towards offering more live programming. In the meantime,' /
            #        'when a program is not available to you via CBS All Access, you will see a message that' /
            #        'states that the program is currently not available.')
            # if user_type == self.anonymous:
            #     self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
            #     #self.verify_exists(id='Already have an account? Sign In')

            # if user_type == self.registered:
            #     self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
            #     # self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')

            # if user_type == self.ex_subscriber:
            #     self.verify_exists(id='GET STARTED')
            #     # self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')
            #     self.verify_not_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

    def validation_ah(self):
        #DEPRECATED
        if self.IS_ANDROID:
            # see_devices_web_view_page
            sleep(5)

            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(name='Live TV')
            try:
                if self.tablet:
                    self.verify_exists(xpath="//*[@class='android.webkit.WebView']")
                else:
                    self.verify_exists(name='Desktops and Laptops')
            except:
                pass
        elif self.IS_IOS:
            sleep(8)
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            self.verify_exists(xpath=self.element_type + 'StaticText[@name="How to Watch Live TV"]')
            self.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Desktops and Laptops"]')
            self.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Smartphones and Tablets"]')
            self.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Streaming media players"]')
            self.verify_exists(
                xpath=self.element_type + 'StaticText[@name="Gaming consoles"]')

    def validation_ai(self):
        self.log_info("Validation AI")
        self.safe_screenshot()
        if self.IS_ANDROID:
            # faq_web_view
            sleep(5)
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")  # cbs icon
            self.verify_exists(xpath="//*[@class='android.webkit.WebView']")
        elif self.IS_IOS:
            sleep(5)
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'Search'])
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Frequently Asked Questions')

    def validation_aj(self):
        if self.IS_ANDROID:
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")  # cbs icon
            self.verify_exists(name='Live TV')
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(name='Check Live TV Availability')
            self.verify_exists(
                name='CBS would like to use your current location to determine if Live TV is available in your area. If prompted, please share your location. By using this CBS Application, you agree to our: Terms of Use, Privacy Policy and Video Services.')
            self.verify_exists(name='Check Availability')
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Live TV')
            self.verify_exists(id="Search")
            self.verify_exists(id='Check Live TV Availability')
            self.verify_exists(
                xpath='(//XCUIElementTypeStaticText[@name="CBS would like to use your current location to determine if Live TV is available in your area. If prompted, please share your location. By using this CBS application, you agree to our Terms of Use, Privacy Policy, and Video Service Policy."])[2]')
            self.verify_exists(id='CHECK AVAILABILITY')

    def validation_ap(self):
        self.log_info("Validation AP")
        if self.IS_ANDROID:
            # no_local_affiliate_page
            self.verify_exists(name='Sorry, your local CBS station is not currently available', screenshot=True,
                               timeout=15)
            self.verify_exists(
                name='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these Videos:')
            self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail')
            self.verify_exists(name='Questions?')
            self.verify_exists(name='READ OUR FAQ')
            self.verify_not_exists(name='Get notified when Live TV is available in your area.')
            self.verify_not_exists(name='GET NOTIFIED')
        if self.IS_IOS:
            pass

    def validation_ak(self, user_type='anonymous'):
        self.log_info("Validation AK")
        if self.IS_ANDROID:
            self.verify_exists(name='Success!', screenshot=True)
            self.verify_exists(name="Choose an option below to start streaming Live TV.")
            self.verify_exists(id=self.com_cbs_app + ':id/ivCBSLogo')
            self.verify_exists(name='OR')
            self.verify_exists(name='TV PROVIDER')
            self.verify_exists(name='Verify Now')
            self.verify_exists(id=self.com_cbs_app + ':id/txtProgramTime')
            if user_type == self.ex_subscriber:
                self.verify_exists(name='Get Started')
            else:
                self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
        elif self.IS_IOS:
            self.verify_exists(id='Success!', screenshot=True)
            self.verify_exists(
                xpath="(//XCUIElementTypeStaticText[@name='Choose an option below to start streaming live TV.'])[2]")
            self.verify_exists(name='OR')
            self.verify_exists(name='TV PROVIDER')
            self.verify_exists(name='VERIFY NOW')
            self.verify_exists(id='CBSAllAccessLogoWhite_274x24')

            if self.xcuitest:
                self.verify_exists(class_name='XCUIElementTypeCollectionView')
                self.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')
            else:
                self.verify_exists(class_name='UIACollectionView')  # schedule

            if user_type in [self.ex_subscriber, self.registered]:
                self.verify_exists(id='CBS All Access subscription required to enjoy Live TV')
            else:
                # TODO verify this check
                self.verify_exists(name='SIGN IN')

    def validation_al(self, user_type='anonymous'):
        self.log_info("Validation AL")
        self.safe_screenshot()
        if self.IS_ANDROID:
            self.verify_exists(name='Sign in with your TV provider to start streaming')
            self.verify_exists(id=self.com_cbs_app + ':id/gridRecyclerView', screenshot=True)
            self.swipe_down_and_verify_if_exists(name='Questions?')
            self.swipe_down_and_verify_if_exists(name='READ OUR FAQ')
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(id='Sign in with your TV provider to start streaming')
                self.verify_exists(id='Questions?')
                self.verify_exists(id='READ OUR FAQ')
                self.verify_exists(xpath=self.element_type + "CollectionView", screenshot=True)

    def validation_am(self):
        self.log_info("Validation AM")
        if self.IS_IOS:
            self.verify_exists(id='Complete the verification process', screenshot=True)
            self.verify_exists(id='Register for a free CBS account to get exclusive benefits including:')
            self.verify_exists(id='Personalized experience with My CBS')
            self.verify_exists(id='Resume video across apps and web')
            self.verify_exists(id='Exclusive content')
            self.verify_exists(id='Fan votes and sweepstakes')
            self.verify_exists(id='Latest content delivered right to your inbox')
            self.verify_exists(id='SIGN UP')
            self.verify_exists(xpath='(//XCUIElementTypeStaticText[@name="Already have an account? Sign in"])[2]')
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.verify_exists(name='Complete the verification process', timeout=15, screenshot=True)
            self.verify_exists(name='Register for a free CBS account to get exclusive benefits including:')
            self.verify_exists(name='Personalize experience with My CBS')
            self.verify_exists(name='Resume video across apps and web')
            self.verify_exists(name='Exclusive content')
            self.verify_exists(name='Fan votes and sweepstakes')
            self.verify_exists(name='Latest content delivered right to your inbox')
            self.verify_exists(name='Sign Up')
            self.verify_exists(name='Already have an account? Sign In')

    def validation_ao(self, user_type='anonymous'):  # TODO need clarification about TV Unavailable page
        self.log_info("Validation AO")
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.verify_exists(name='Sorry, your local CBS station is not currently available', screenshot=True)
            self.verify_exists(
                name='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these Videos:')
            self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail')
            self.verify_not_exists(name='GET NOTIFIED')
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(id="Sorry, your local CBS station is not currently available", screenshot=True)
                self.verify_exists(
                    id='Please check back soon to see if coverage has expanded to your area. In the meantime, enjoy these videos.')
                # self.verify_exist()  # TODO  video thumbnail
                self.verify_not_exists(id='GET NOTIFIED')

    def validation_aq(self, user_type='anonymous'):
        self.log_info("Validation AQ")
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.verify_exists(name='Your TV provider is not supported in this area', screenshot=True)
            self.verify_exists(name='but you can sign up for CBS All Access to watch now.')
            self.verify_exists(name='Watch Live TV')
            self.verify_exists(name='Over 8,500 Episodes on Demand')
            self.verify_exists(name='New Episodes on CBS App Next Day')
            self.verify_exists(name='Take A Quick Tour')
            self.verify_exists(name='Questions?')
            self.verify_exists(name='READ OUR FAQ')
            if user_type == self.ex_subscriber:
                self.verify_not_exists(
                    xpath="//android.widget.Button[contains(@text,'Try 1')] and [contains(@text,'free')]")
                self.verify_exists(name='Get Started')
            else:
                self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
            if user_type == self.anonymous:
                self.verify_exists(name='Already have an account? Sign In')
            else:
                self.verify_not_exists(name='Already have an account? Sign In')
        elif self.IS_IOS:
            self.verify_exists(id='Watch Live TV')
            self.verify_exists(id='Over 8,500 Episodes on Demand')
            self.verify_exists(id='New Episodes on CBS App Next Day')
            self.verify_exists(id='TAKE A QUICK TOUR')
            self.verify_exists(id='Questions?')
            self.verify_exists(id='READ OUR FAQ')

            if user_type == self.anonymous:
                self.verify_exists(id='Your TV provider is not supported in this area', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_exists(
                    xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_exists(id='Already have an account? Sign In')
            else:
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.registered:
                self.verify_exists(id='Sorry, your TV provider is not supported in this area', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_exists(
                    xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

            if user_type == self.ex_subscriber:
                self.verify_exists(id='Sorry, your TV provider is not supported in your area,', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_not_exists(
                    xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_exists(id='GET STARTED')

    def validation_as(self, user_type='anonymous'):
        self.log_info("Validation AS")
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.click_allow_popup()
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(name='We show that CBS is not authorized for you by your TV provider')
            self.verify_exists(name='Watch Live TV')
            self.verify_exists(name='Over 8,500 Episodes on Demand')
            self.verify_exists(name='Take A Quick Tour')
            self.verify_exists(name='New Episodes on CBS App Next Day')
            self.verify_exists(name='Questions?')
            self.verify_exists(name='READ OUR FAQ')
            if user_type == self.ex_subscriber:
                self.verify_exists(name='Get Started')
            else:
                self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
            if user_type == self.anonymous:
                self.verify_exists(name='Already have an account? Sign In')
            # else:
            #     self.verify_not_exists(name='Already have an account? Sign In')
        elif self.IS_IOS:
            sleep(5)
            self.safe_screenshot()
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'Search', 'We show that CBS is not authorized for you by your TV provider,',
                'but you can sign in to All Access to watch now.|but you can sign in to CBS All Access to watch now.',
                'SIGN IN', 'Take a quick tour', 'READ OUR FAQ'])
            self.verify_exists(id='Questions?')
            self.verify_exists(id='CBSEye_white')

    def validation_at(self, user_type="anonymous", category="All Shows"):
        if self.IS_ANDROID:
            self.movies_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'Movies', 'Search'])
            if self.xcuitest:
                self.assertTrueWithScreenShot(
                    len(self.driver.find_element_by_class_name(
                        'XCUIElementTypeCollectionView').find_elements_by_class_name('XCUIElementTypeCell')) > 0,
                    msg="At least 3 Movies posters should be presented")

    def validation_au(self, user_type='anonymous'):
        if self.IS_ANDROID:
            self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieName')
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieMetadata')
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieDescription')
            self.verify_exists(name='PREVIEW TRAILER')  # disabled due to CBS bug, will uncomment on new build
            if user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(name='SUBSCRIBE TO WATCH')
                self.verify_not_exists(name='WATCH MOVIE')
            elif user_type in [self.trial, self.subscriber, self.cf_subscriber]:
                self.verify_exists(name='WATCH MOVIE')
                self.verify_not_exists(name='SUBSCRIBE TO WATCH')
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                self.verify_exists(class_name=self.element_prefix() + 'Image', screenshot=True)
                self.verify_in_batch(['Subscribe to Watch', 'Preview Trailer', 'Close'], with_timeout=2)
            else:
                self.verify_in_batch(['WATCH MOVIE|RESTART MOVIE|RESUME MOVIE', 'Preview Trailer', 'Close'],
                                     with_timeout=2)

    def validation_av(self):
        if self.IS_ANDROID:
            self.verify_exists(xpath=("//*[@text='CBS']"), timeout=60)
            self.verify_exists(xpath=(
                "//*[@text='An internet connection is required to experience the CBS App. Please check your connection and try again.']"))
            self.verify_exists(xpath=("//*[@text='OK']"))

    def validation_ax1(self):
        if self.IS_ANDROID:
            self.verify_exists(id=self.com_cbs_app + ':id/appIcon')
            self.verify_exists(id=self.com_cbs_app + ':id/cbsTextView')
            self.verify_exists(id=self.com_cbs_app + ':id/appVersionTextView')
        elif self.IS_IOS:
            self.verify_in_batch(['CBSEye_white', 'App Version', 'CBS'])

    def validation_ax2(self):
        if self.IS_ANDROID:
            self.verify_exists(accessibility_id='ABOUT NIELSEN MEASUREMENT')

    def validation_ax3(self):
        if self.IS_ANDROID:
            self.verify_exists(xpath=("//*[@text='Type your feedback above the dotted line']"))
            self.verify_exists(xpath=("//*[@text='we are including some device details so we can better help you']"))
            self.verify_exists(xpath=("//*[@text='App Version']"))
            self.verify_exists(xpath=("//*[@text='OS Version']"))
            self.verify_exists(xpath=("//*[@text='Device']"))
            self.verify_exists(xpath=("//*[@text='Account']"))

    # Video Validation
    def validation_ay(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.accept_video_popup()
            self.restart_from_the_beggining()
            sleep(20)
            self.pause_video()
            self.verify_exists_video_element(id='Done', screenshot=True)
            # self.verify_exists(id='Learn More') not applicable for all users
            self.verify_exists_video_element(class_name=self.element_prefix() + 'Slider')
            self.verify_exists_video_element(id='UVPSkinClosedCaptionOnButton')
            self.verify_exists_video_element(id='UVPSkinShareOnButton')

    def validation_az(self):
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            self.accept_video_popup()
            self.restart_from_the_beggining()
            sleep(20)
            self.pause_video()
            self.verify_exists_video_element(id='Done', screenshot=True)
            self.verify_exists_video_element(class_name=self.element_prefix() + 'Slider')
            self.verify_exists_video_element(
                xpath='//' + self.element_prefix() + 'Other[./' + self.element_prefix() + 'Slider and ./' + self.element_prefix() + 'StaticText[1] and ./' + self.element_prefix() + 'StaticText[2]]')

    def validation_ba(self):
        self.log_info("Validation BA")
        if self.IS_ANDROID:
            self.verify_in_batch(":id/expand_button", ":id/cc_button")
        elif self.IS_IOS:
            self.verify_exists(xpath='//XCUIElementTypeImage')
            # self.verify_exists(id='Episode title')
            # self.verify_exists(xpath='//XCUIElementTypeText')
            self.verify_exists(xpath="//XCUIElementTypeButton[@name='LiveSkin close captioned icon ']")
            self.verify_exists(id='LiveSkin close fullscreen icon')


    def validation_bb(self, user_type='anonymous', mvpd=False):
        self.log_info("Validation BB")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                ':id/action_search',
                ':id/surfaceView',
                ':id/liveTvRecyclerView'
            ]
            if mvpd:
                text_list.append(':id/imgProviderLogo')

            self.verify_in_batch(text_list, False)
            self.verify_exists(xpath="//android.widget.FrameLayout[1]")
            self.verify_exists(xpath="//android.widget.FrameLayout[2]")

            if user_type in [self.registered, self.ex_subscriber]:
                self.verify_exists(name='Schedule')
            else:
                self.verify_exists(name='Channels')
        if self.IS_IOS:
            Player='//XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther'#TODO Player
            self.verify_exists(xpath=Player)
            self.verify_exists(xpath='//XCUIElementTypeCollectionView')
            self.verify_exists(xpath='//XCUIElementTypeCell[1]')
            self.verify_exists(xpath='//XCUIElementTypeCell[2]')
            if mvpd:
                pass
                #TODO self.verify_exists(id='Station logo')




    def validation_bc(self, mvpd=False):
        self.log_info("Validation BC")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                ':id/action_search',
                ':id/surfaceView',
                'Schedule',
                ':id/layout_backIcon',
                ':id/imgStationLogo',
            ]
            if mvpd:
                text_list.append(':id/imgProviderLogo')
            self.verify_in_batch(text_list, False)
            self.verify_exists(xpath="//android.widget.FrameLayout[1]")
        if self.IS_IOS:
            self.verify_in_batch(['Main Menu|Open CBS Menu', 'CBSEye_white'])
            Player = '//XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther'  # TODO Player
            self.verify_exists(xpath=Player)
            self.verify_exists(xpath='//XCUIElementTypeCollectionView')#TODO Schedule
            self.verify_exists(xpath='//XCUIElementTypeCell[1]')#TODO Schedule Grid
            self.verify_exists(xpath='//XCUIElementTypeImage')#TODO Station Logo
            #TODO Live Tv
            if mvpd:
                pass
                #TODO Clarify validation
                # self.verify_not_exists(id='CBS.CBSiLiveTVChannelDetailView')
                # self.verify_not_exists(id='Channels')

    def validation_bd(self):
        # self.verify_exists(xpath="//*[contains(@name,'AM') or contains(@name,'PM') or contains(@name,':')]")
        #TODO TIME
        #TODO Show Title
        #TODO Episode Title
        #TODO Description
        pass

    def validation_be(self, mvpd=False):
        self.log_info("Validation BE")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                ':id/action_search',
                ':id/surfaceView',
                'Schedule',
                ':id/layout_backIcon',
                ':id/imgStationLogo',
            ]
            if mvpd:
                text_list.append(':id/imgProviderLogo')
            self.verify_in_batch(text_list, False)
            self.verify_exists(xpath="//android.widget.FrameLayout[1]")

    def validation_bf(self):
        self.log_info("Validation BF")
        if self.IS_ANDROID:
            self.safe_screenshot()
            self.verify_in_batch(['Station Unavailable', 'Channels', 'CBS Local Station', ':id/station_logo'])
        if self.exists(name="We can't find your local CBS station."):
            self.verify_exists(name="We can't find your local CBS station.")

    def validation_bi(self, non_sub=None):
        self.log_info("Validation BI")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                ':id/action_search',
                'Please accept the Terms of Use in order to watch live TV.',
                'VIEW TERMS TO ACCEPT',
                ':id/livetv_video_view'
            ]
            if non_sub:
                text_list.append('Schedule')
            else:
                text_list.append('Channels')

            self.verify_in_batch(text_list, False)

        if self.IS_IOS:
            text_list = ['Main Menu|Open CBS Menu', 'CBSEye_white', 'Please accept the Terms of Use in order to watch live TV.', 'VIEW TERMS TO ACCEPT']
            self.verify_exists(xpath='//XCUIElementTypeCollectionView')
            self.verify_exists(xpath='//XCUIElementTypeCell[1]')
            self.verify_exists(xpath='//XCUIElementTypeCell[2]')
            self.verify_in_batch(text_list)
            #if non_sub:
               #text_list.append('Channels')
            #TODO Live TV and Search are absent



    def validation_bj(self, user_type='anonymous', mvpd=False):
        self.log_info("Validation BJ")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                ':id/action_search',
                ':id/controlsContainer',
                ':id/liveTvRecyclerView'

            ]
            if mvpd:
                text_list.append(':id/imgProviderLogo')

            self.verify_in_batch(text_list, False)
            if user_type in [self.registered, self.ex_subscriber]:
                self.verify_exists(name='Schedule')
            else:
                self.verify_exists(name='Channels')
        elif self.IS_IOS:
            sleep(5)
            self.verify_exists(xpath='//XCUIElementTypeApplication[@name="CBS"]', screenshot=True)
            self.verify_exists(xpath='//XCUIElementTypeOther/XCUIElementTypeImage[1]')  # station icon

    def validation_bk(self):
        self.log_info("Validation BK")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Share Your Location',
                'Please enable location services',
                'Channels',
                'Share Location',
                'Channels',
                'CBS Local Station',
            ]
            self.verify_in_batch(text_list, False)

    def validation_bl(self):
        self.log_info("Validation BL")
        if self.IS_ANDROID:
            self.safe_screenshot()
            text_list = [
                'Open navigation drawer',
                'Live TV',
                'Select Your Local Station',
                'You can always change this',
                'Channels',
                'CBS Local Station',
            ]
            self.verify_in_batch(text_list, False)

    def validation_bm(self, user_type='anonymous'):
        self.log_info("Validation BM")
        if self.IS_ANDROID:
            pass
        elif self.IS_IOS:
            text_list = ['Pick Your Plan',
                         'Back|Back Button',
                         'Live TV includes commercials and select shows have promotional interruptions']

            if self.user_type != self.cf_subscriber:
                text_list.append('COMMERCIAL FREE')
                text_list.append('\$9\.99\/mo')

            if self.user_type in [self.anonymous, self.registered]:
                text_list.append('TRY 1 WEEK FREE|TRY FREE FOR 1 WEEK')
            elif self.user_type == self.ex_subscriber:
                text_list.append('GET STARTED')
            elif self.user_type in [self.subscriber, self.trial]:
                text_list.append('UPGRADE')

            if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
                text_list.append('LIMITED COMMERCIALS')
                text_list.append('\$5\.99\/mo')

            self.verify_in_batch(text_list, False)
            self.verify_exists(
                xpath="//XCUIElementTypeStaticText[contains(@name,'Payment will be charged to iTunes Account')]")


    def validation_video(self):
        if self.IS_ANDROID:
            self.accept_popup_video_click()
            self.click_play_from_beginning()
            self.safe_screenshot()
            self.verify_exists(element=self.video_page_android.video_player_screen(),
                               readable_name="Video player screen", screenshot=True)
            self.back()
        elif self.IS_IOS:
            self._accept_alert(1)
            self.restart_from_the_beggining(timeout=15)
            sleep(20)  # wait for video to start
            self.verify_exists_video_element(id='Done', screenshot=True)
            if self.phone:
                self.verify_exists_video_element(class_name='XCUIElementTypeSlider', screenshot=False)
            else:
                self.exists_in_page_source('XCUIElementTypeSlider')
