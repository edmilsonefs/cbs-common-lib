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
from helper.android.video_page import VideoPage as VideoPageAndroid


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
                                  'By using this CBS Application, you agree to our:',
                                  'Terms of Use',
                                  'Mobile User Agreement',
                                  'Privacy Policy',
                                  'Video Services',
                                  'ACCEPT'])
        elif self.IS_IOS:
            self.verify_in_batch(['By watching this video, you agree to our: |By watching this video or stream, you agree to our: ',
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
            self.verify_in_batch(['Main Menu', 'Search'])
            # self.verify_exists(id='MarqueeCollectionView', timeout=10) #add home page marquee

    def validation_c(self):
        if self.IS_ANDROID:
            self.verify_in_batch(['Our Terms Have Changed',
                                  ':id/terms_accept_checkBox',
                                  'By registering you become a member of the CBS Interactive family of sites and you have '
                                  'read and agree to the Terms of Use, Privacy Policy and Video Services Policy. '
                                  'You understand that on occasion, you will receive updates, alerts and promotions from '
                                  'CBS. You agree that CBS may share information about you with companies that provide '
                                  'content, products or services featured on CBS sites so that they may contact '
                                  'you about their products or services.',
                                  'CANCEL',
                                  'SUBMIT'])
        elif self.IS_IOS:
            self.verify_in_batch(['Search', 'Sign In', 'Our terms have changed', 'CONTINUE'])

    def validation_d(self):
        if self.IS_ANDROID:
            self.sign_in_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_navigation_back_button()  # Cbs logo appear as back button
            self.verify_in_batch(['SIGN IN', 'Sign in with your social account', 'Sign in with your email'], screenshot=True)
            # self.verify_exists(id="Don't have an account? Sign Up")

    def validation_e(self):
        if self.IS_ANDROID:
            self.sign_up_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_in_batch(['Sign up with your email', 'SIGN UP'])
            # Already have an account? Sign in - doesn't exist on this page

    def validation_f(self, user_type='anonymous', name=None):  # TODO update Validation.
        if self.IS_ANDROID:
            if user_type == self.anonymous:
                self.verify_exists(element=self.home_page_android.btn_sign_in_menu_item())
            else:
                self.verify_exists(name=name)
            if user_type in [self.subscriber, self.trial]:
                self.verify_exists(element=self.home_page_android.btn_upgrade_menu_item())

            elif user_type == self.cf_subscriber:
                self.verify_not_exists(name='Upgrade')
                self.verify_not_exists(name='Subscribe')
            else:
                self.verify_exists(element=self.home_page_android.btn_subscribe_menu_item())
            self.verify_exists(element=self.home_page_android.btn_settings_menu_item(), screenshot=True)
            self.verify_exists(element=self.home_page_android.btn_home_menu_item())
            self.verify_exists(element=self.home_page_android.btn_shows_menu_item())
            self.verify_exists(element=self.home_page_android.btn_live_tv_menu_item())
            self.verify_exists(element=self.home_page_android.btn_movies_menu_item())
            self.verify_exists(element=self.home_page_android.btn_schedule_menu_item())
            self.verify_exists(element=self.home_page_android.btn_shop_menu_item())
        if self.IS_IOS:
            if user_type == self.anonymous:
                self.verify_exists(id='Sign In', screenshot=False)
            self.verify_in_batch(['Settings', 'Home', 'Shows', 'Schedule', 'Store'])
            # self.verify_exists(id='Live TV') TODO update validation
            # self.verify_exists(id='Movies')
            # self.verify_exists(name='My CBS')

            # Show Page

    def validation_g(self, user_type='anonymous'):
        if self.IS_ANDROID:
            if user_type == self.anonymous:
                self.verify_not_exists(name='Recently Watched')
                self.verify_not_exists(name='My CBS')
            else:
                self.verify_exists(name='Recently Watched')
                self.verify_exists(id=self.com_cbs_app + ":id/imgThumbnail")
                self.verify_exists(name='My CBS')
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
            #self.verify_share_icon()
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
            self.verify_exists(id='WATCH')
            self.verify_exists(id='CLOSE')

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
            self.verify_in_batch(['Main Menu', 'ET/PT', 'Today', 'Search'])
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
            self.verify_in_batch(['Main Menu', 'Search', 'I want to see: %s' % category])
            self.verify_exists(xpath="//XCUIElementTypeCell//XCUIElementTypeImage") # DO NOT MAKE IT OVER COMPLICATED
            #self.verify_show_cards_exist()

    def validation_n(self):
        if self.IS_ANDROID:
            self.shows_page_android.validate_all_shows_dropdown_menu()
        elif self.IS_IOS:
            self.verify_in_batch(['All Shows', 'Featured', 'Primetime', 'Daytime', 'Late Night', 'Specials', 'News', 'Classics'])

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
            self.verify_exists(element=self.show_page_android.btn_like_on_facebook(), screenshot=True, name='Like on Facebook')
            self.verify_exists(element=self.show_page_android.btn_follow_on_twitter(), name='Follow on Twitter')
            self.verify_exists(element=self.show_page_android.btn_share(), name='Share')
            self.verify_exists(element=self.show_page_android.btn_add_to_calendar(), name='Add to Calendar')
            self.verify_exists(element=self.show_page_android.btn_show_info(), name='Show Info')
        elif self.IS_IOS:
            self.verify_in_batch(['Like on Facebook', 'Follow on Twitter', 'Share', 'Add to Calendar', 'Show Info'])

    def validation_q(self, user_type='anonymous'):  # TODO update validation
        if self.IS_ANDROID:
            self.settings_page_android.validate_page(user_type)
        elif self.IS_IOS:
            if user_type in [self.subscriber, self.cf_subscriber, self.trial]:
                self.verify_exists(id='Sign Out')
                self.verify_exists(id='Subscription')
            else:
                self.verify_exists(id='Subscribe')

            self.verify_navigation_drawer_button()
            self.verify_cbs_logo()
            self.verify_exists(id='Settings')
            self.verify_in_batch(['App Version', 'Terms Of Use', 'Privacy Policy', 'Mobile User Agreement', 'Video Services'])
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

    def validation_t(self):
        if self.IS_ANDROID:
            self.verify_movie_poster()
        elif self.IS_IOS:
            self.verify_show_cards_exist()

            # Live TV Page

    def validation_u(self, user_type="anonymous"):  # TODO update validation, Updated for IOS
        # Upsell Page
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
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

            if user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.registered:
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.subscriber:
                if self.phone:
                    self.verify_exists(id='Start Watching')
                else:
                    if self.xcuitest:
                        self.verify_exists(
                            xpath='//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]')  # Schedule
                        self.verify_exists(
                            xpath='//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage')  # Video Image

    def validation_v(self, user_type="anonymous"):
        if self.IS_ANDROID:
            self.upsell_page_android.validate_page(user_type=user_type)
        elif self.IS_IOS:
            if user_type in [self.anonymous, self.registered]:
                self.verify_exists(
                    id="LIMITED COMMERCIALS",
                    screenshot=True, timeout=20)
            if user_type == self.registered:
                self.verify_not_exists(name='SELECT', timeout=10)
            elif user_type in [self.subscriber, self.trial]:
                self.verify_exists(id="COMMERCIAL FREE")
                self.verify_exists(xpath="//XCUIElementTypeStaticText[contains(@name,'UPGRADE')]")
            elif user_type == self.cf_subscriber:
                self.verify_exists(id="COMMERCIAL FREE")
            else:
                if user_type == self.ex_subscriber:
                    self.verify_exists(
                        id="LIMITED COMMERCIALS",
                        timeout=20)
                    self.verify_exists(id="COMMERCIAL FREE", timeout=20)
                    self.verify_exists(xpath="//XCUIElementTypeStaticText[contains(@name,'Only $5.99/month')]", timeout=20)
                    self.verify_exists(id='SELECT', timeout=20)
                    self.verify_not_exists(id='GET STARTED', timeout=10)
                    self.verify_not_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]", timeout=10)

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
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Sign Up')
            self.verify_exists(id="Search")
            self.verify_exists(id='Please complete your registration')
            self.verify_exists(id='CONTINUE')

    def validation_xf(self):
        if self.IS_ANDROID:
            #self.verify_exists(name='Sign up with your Facebook account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
                self.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Sign Up')
            self.verify_exists(id="Search")
            self.verify_exists(id='Please complete your registration')
            self.verify_exists(id='Sign up with your Facebook account')
            self.verify_exists(id='CONTINUE')

    def validation_xt(self):
        if self.IS_ANDROID:
            #self.verify_exists(name='Sign up with your Twitter account', screenshot=True)
            for _ in range(0, 3):
                self._short_swipe_down()
            self.verify_exists(id=self.com_cbs_app + ':id/btnSignUp', screenshot=True)
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id='Sign Up')
            self.verify_exists(id="Search")
            self.verify_exists(id='Please complete your registration')
            self.verify_exists(id='Sign up with your Twitter account')
            self.verify_exists(id='CONTINUE')

    def validation_xg(self):
        if self.IS_ANDROID:
            #self.verify_exists(name='Sign up with your Google account', screenshot=True)
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
            self.verify_exists(id='Sign Out')

    def validation_ac(self, user_type='anonymous'):
        if self.IS_ANDROID:
            if not self.IS_AMAZON: #TODO skip for Amazon for a while
                # LCS Billing Popup
                self.wait_until_element_is_visible(element_id='com.android.vending:id/item_title')
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
        if self.IS_ANDROID:
            self.wait_until_element_is_visible(element_id='com.android.vending:id/item_title')
            self.verify_exists(name='Subscribe', timeout=20, screenshot=True)
            # self.verify_exists(xpath="//*[contains(@text,''(Commercial Free) and contains(@text,'CBS - Full Episodes')]", screenshot=True)

        elif self.IS_IOS:
            pass

    def validation_ar(self):
        # multiple_channel_selector_page
        if self.IS_ANDROID:
            sleep(5)
            self.safe_screenshot()
            # if self.tablet:
            #     self.verify_exists(name='Navigate up', screenshot=True)
            # else:
            #     self.verify_exists(name='Open navigation drawer', screenshot=True)

            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            # cbs all access
            self.verify_exists(name='Select Your Local Station')
            # self.verify_exists(name='You can always change this by visiting Settings > Live TV')
            self.verify_exists(xpath="//android.widget.TextView[contains(@text,'You can always change this')]")
            self.verify_exists(name='Channels')
            self.verify_exists(name='KWTX')
            self.verify_exists(name='KBTX')
        elif self.IS_IOS:
            pass

    def validation_ae(self, mvpd=False):
        if self.IS_ANDROID:
            # cbs logo
            self.accept_popup_video_click()
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(id=self.com_cbs_app + ':id/station_logo')
            self.verify_exists(id=self.com_cbs_app + ':id/controlsContainer')
            # if mvpd:
            #     self.verify_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
            # else:
            #     self.verify_not_exists(id=self.com_cbs_app + ':id/imgProviderLogo') # TODO needs to update this validation
            self.verify_exists(id=self.com_cbs_app + ':id/liveTvRecyclerView')  # schedule table
        elif self.IS_IOS:
            self.verify_exists(id='CBSEye_white', screenshot=True)
            # self.verify_exists(id="Search")
            # self.verify_exists(xpath=self.element_type + 'TextView[1]')  # schedule table
            self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Channels"]')
            self.verify_exists(xpath='//XCUIElementTypeApplication[@name="CBS"]')
            self.verify_exists(xpath='//XCUIElementTypeOther/XCUIElementTypeImage[1]')  # station icon

    def validation_af(self):
        if self.IS_ANDROID:
            self.verify_exists(name='CBS', screenshot=True)
            self.verify_exists(
                name='Sorry, the video you would like to watch is not available in the CBS app at this time.')
            self.verify_exists(name='OK')

    def validation_ag(self, user_type='anonymous'):
        if self.IS_ANDROID:
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(name='Live TV')
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(name='Two ways to watch Live TV')
            self.verify_exists(name='Instantly watch your local CBS station at home or on the go!')
            self.verify_exists(id=self.com_cbs_app + ':id/imageView')  # cbs all access
            self.verify_exists(name='Stream Live TV plus thousands of full episodes on demand.')
            if user_type == self.anonymous:
                self.verify_exists(name='Already have an account? Sign In')
                self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
                # self.verify_exists(xpath="//android.widget.Button[contains(@text,'Try 1')] and [contains(@text,'free')]")
                self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
            elif user_type == self.ex_subscriber:
                try:
                    self.verify_exists(name='Get Started')
                    self.verify_exists(name='Note: CBS All Access subscription required to enjoy Live TV')
                except:
                    pass

                self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
                self.verify_not_exists(name='Already have an account? Sign In')
            else:
                self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
                self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
                self.verify_not_exists(name='Already have an account? Sign In')
            self.swipe_down_and_verify_if_exists(name='OR')
            self.swipe_down_and_verify_if_exists(name='TV PROVIDER')
            self.swipe_down_and_verify_if_exists(name='Stream Live TV with your cable, satellite or telco provider.',
                                                 screenshot=True)
            self.swipe_down_and_verify_if_exists(name='Verify Now')
            # self.swipe_down_and_verify_if_exists(id_element='com.cbs.app:id/txtLearnMore')
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')  # cbs icon
            self.verify_exists(id='Live TV')
            self.verify_exists(id='Two ways to watch Live TV')
            self.verify_exists(id='Instantly watch your local CBS station at home or on the go!')
            self.verify_exists(id='Stream Live TV plus thousands of full episodes on demand.', timeout=30)
            self.verify_exists(
                id='Take the tour')  # TODO Take the tour on Simulator, in Spec - Take a tour  (in spec for validation_u there is take the tour). Need clarification
            self.verify_exists(id='OR')
            self.verify_exists(id='TV PROVIDER')
            self.verify_exists(id='Stream Live TV with your cable, satellite or telco provider.')
            self.verify_exists(id='VERIFY NOW')
            self.verify_exists(id='Learn more')
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
            if user_type == self.anonymous:
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_exists(id='Already have an account? Sign In')

            if user_type == self.registered:
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')

            if user_type == self.ex_subscriber:
                self.verify_exists(id='GET STARTED')
                self.verify_not_exists(id='Already have CBS ALL ACCESS? Sign In')
                self.verify_not_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

    def validation_ah(self):
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
        if self.IS_ANDROID:
            # faq_web_view
            sleep(5)
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/action_search')
            self.verify_exists(
                xpath="//*[@resource-id='" + self.com_cbs_app + ":id/toolbar']//*[@class='android.widget.ImageView']")  # cbs icon
            self.verify_exists(xpath="//*[@class='android.webkit.WebView']")
        elif self.IS_IOS:
            self.driver.implicitly_wait(5)
            sleep(5)
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id="Search")
            self.verify_exists(id="Frequently Asked Questions")
            self.safe_screenshot()
            # self.verify_exists(xpath='//XCUIElementTypeStaticText[@name="Frequently Asked Questions"]')
            self.driver.implicitly_wait(30)

    def validation_aj(self):
        if self.IS_ANDROID:
            if self.tablet:
                self.verify_exists(name='Navigate up')
            else:
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
        if self.IS_ANDROID:
            # no_local_affiliate_page
            self.verify_exists(name='Sorry, your local CBS station is not currently available', screenshot=True, timeout=15)
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
                self.verify_exists(xpath='//XCUIElementTypeCollectionView')
                self.verify_exists(xpath='//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]')
            else:
                self.verify_exists(class_name='UIACollectionView')  # schedule

            if user_type in [self.ex_subscriber, self.registered]:
                self.verify_exists(id='CBS All Access subscription required to enjoy Live TV')
            else:
                #TODO verify this check
                self.verify_exists(name='SIGN IN')

    def validation_al(self, user_type='anonymous'):
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
            self.verify_exists(name='Complete the verification process', screenshot=True)
            self.verify_exists(name='Register for a free CBS account to get exclusive benefits including:')
            self.verify_exists(name='Personalize experience with My CBS')
            self.verify_exists(name='Resume video across apps and web')
            self.verify_exists(name='Exclusive content')
            self.verify_exists(name='Fan votes and sweepstakes')
            self.verify_exists(name='Latest content delivered right to your inbox')
            self.verify_exists(name='Sign Up')
            self.verify_exists(name='Already have an account? Sign In')

    def validation_ao(self, user_type='anonymous'):  # TODO need clarification about TV Unavailable page
        if self.IS_ANDROID:
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
        if self.IS_ANDROID:
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
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_exists(id='Already have an account? Sign In')
            else:
                self.verify_not_exists(id='Already have an account? Sign In')

            if user_type == self.registered:
                self.verify_exists(id='Sorry, your TV provider is not supported in this area', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")

            if user_type == self.ex_subscriber:
                self.verify_exists(id='Sorry, your TV provider is not supported in your area,', screenshot=True)
                self.verify_exists(id='but you can sign up for CBS All Access to watch now.')
                self.verify_not_exists(xpath="//XCUIElementTypeButton[contains(@name,'TRY 1') and contains(@name, 'FREE') and (contains(@name, 'MONTH') or contains(@name, 'FREE'))]")
                self.verify_exists(id='GET STARTED')

    def validation_as(self, user_type='anonymous'):
        if self.IS_ANDROID:
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
            else:
                self.verify_not_exists(name='Already have an account? Sign In')
        elif self.IS_IOS:
            self.verify_exists(id='Main Menu', screenshot=True)
            self.verify_exists(id='CBSEye_white')
            self.verify_exists(id="Search")
            self.verify_exists(id='We show that CBS is not authorized for you by your TV provider,')
            self.verify_exists(id='but you can sign in to CBS All Access to watch now.')
            self.verify_exists(id='SIGN IN')
            self.verify_exists(id='Take a quick tour')
            self.verify_exists(id='Questions?')
            self.verify_exists(id='READ OUR FAQ')

    def validation_at(self, user_type="anonymous", category="All Shows"):
        if self.IS_ANDROID:
            self.movies_page_android.validate_page()
        elif self.IS_IOS:
            self.verify_in_batch(['Main Menu', 'Movies', 'Search'])
            if self.xcuitest:
                self.assertTrueWithScreenShot(
                    len(self.get_elements(xpath='//XCUIElementTypeCollectionView//XCUIElementTypeCell')) >= 3,
                    msg="At least 3 Movies posters should be presented")

    def validation_au(self, user_type='anonymous'):
        if self.IS_ANDROID:
            self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail', screenshot=True)
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieName')
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieMetadata')
            self.verify_exists(id=self.com_cbs_app + ':id/txtMovieDescription')
            self.verify_exists(name='PREVIEW TRAILER') #disabled due to CBS bug, will uncomment on new build
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
                self.verify_in_batch(['Watch', 'Preview Trailer', 'Close'], with_timeout=2)

    def validation_av(self):
        if self.IS_ANDROID:
            self.verify_exists(xpath=("//*[@text='CBS']"))
            self.verify_exists(xpath=("//*[@text='An internet connection is required to experience the CBS App. Please check your connection and try again.']"))
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

    def validation_video(self):
        if self.IS_ANDROID:
            self.accept_popup_video_click()
            self.click_play_from_beginning()
            self.verify_exists(element=self.video_page_android.video_player_screen(), readable_name="Video player screen", screenshot=True)
            self.back()
        elif self.IS_IOS:
            self._accept_alert(1)
            self.restart_from_the_beggining(timeout=15)
            sleep(20) # wait for video to start
            self.verify_exists_video_element(id='Done', screenshot=True)
            if self.phone:
                self.verify_exists_video_element(xpath=
                    '//XCUIElementTypeSlider', screenshot=False)
            else:
                self.exists_in_page_source('XCUIElementTypeSlider')
