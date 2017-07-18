class Validations():

    def validation_b(self): #TODO update validation
        if self.user_type in [self.subscriber, self.trial, self.cf_subscriber]:
            self.verify_exists(id='CBSLogo_AllAccess_white', screenshot=False)
        else:
            self.verify_exists(id='CBSLogo_white', screenshot=False)
            self.verify_exists(id="Main Menu")
            self.verify_exists(id='Search')
            # self.verify_exists(id='Marquee', timeout=60) TODO impossible to verify because of sliding

    def validation_d(self): #TODO update validation
        self.verify_exists(name='Sign In', screenshot=False)
        self.verify_exists(name='Sign in with your email')

    def validation_e(self): #TODO update validation
        self.verify_exists(id="Sign in with your social account", screenshot=False)
        self.verify_exists(id="FacebookLogo")
        self.verify_exists(id="TwitterLogo")
        self.verify_exists(id="GooglePlusLogo")
        self.verify_exists(id="Sign in with your email")
        self.verify_exists(id="Forgot Password?")
        self.verify_exists(id="SIGN IN")
        self.verify_exists(id="Subscribed through iTunes? Restore Purchase")
        self.verify_exists(id="Don\'t have an account? Sign Up")

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

    def validation_i(self): #TODO update validation
        self.verify_exists(id='Watch Episode', screenshot=False)
        self.verify_exists(id='More From Show')
        self.verify_exists(id='Close')

    def validation_l(self): # TODO update validation
        self.close_big_advertisement()
        self.verify_exists(xpath="//UIAButton[@name='Add to My CBS' or @name='Remove from My CBS']", screenshot=True)
        self.verify_exists(id='Share')
        self.verify_exists(id='Cancel')

    def validation_m(self, category): #TODO update validation
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

    def validation_q(self, name): #TODO update validation

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

    def validation_u(self): #TODO update validation
        if self.user_type in [self.subscriber, self.trial, self.cf_subscriber]:
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

    def validation_y(self): #TODO update validation

        self.verify_exists(name='Our Terms Have Changed', screenshot=False)
        self.verify_exists(id='com.cbs.app:id/terms_accept_checkBox')
        self.verify_exists(
            name="By registering you become a member of the CBS Interactive family of sites and you have "
                 "read and agree to the Terms of Use, Privacy Policy and Video Services Policy. "
                 "You understand that on occasion, you will receive updates, alerts and promotions from "
                 "CBS. You agree that CBS may share information about you with companies that provide "
                 "content, products or services featured on CBS sites so that they may contact "
                 "you about their products or services.")
        self.verify_exists(name='CANCEL')
        self.verify_exists(name='SUBMIT')

    def validation_ae(self):
        #TODO uncomment
        # self.verify_cbs_logo()
        self.verify_exists(id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(id=self.com_cbs_app + ':id/imgStationLogo')
        #TODO add flow depending on MVPD on not for this validation
        self.verify_exists(id=self.com_cbs_app + ':id/imgProviderLogo')
        self.verify_exists(id=self.com_cbs_app + ':id/programsContentFlipper')  # schedule table

    def validation_ag(self, anonymous=False, ex_subscriber=False):
        #TODO remove. This is not in the spec
        self.live_tv_page.btn_check_availability()
        #TODO this if-else flow not in the spec, but need to check if this is applicable
        if self.tablet:
            self.verify_exists(name='Navigate up', screenshot=True)
        else:
            self.verify_exists(name='Open navigation drawer', screenshot=True)
            #TODO uncomment and change indentation <-
            # self.verify_cbs_logo()
        self.verify_exists(name='Live TV')
        self.verify_exists(id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(name='Two ways to watch Live TV')
        self.verify_exists(name='Instantly watch your local CBS station at home or on the go!')
        self.verify_exists(id=self.com_cbs_app + ':id/imageView')  # cbs all access
        #TODO should be substituted with 'Get Live TV plus thousands of full episodes on demand.'
        self.verify_exists(name='Stream Live TV plus thousands of full episodes on demand.')

        # <user-state specific values> step starts here
        #TODO add flow for registered user:
        #TRY 1 WEEK FREE [button] → Should NOT have text: “Already have CBS ALL ACCESS? Sign In”
        if anonymous:
            self.verify_exists(name='Already have an account? Sign In')

            self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
            # self.verify_exists(xpath="//android.widget.Button[contains(@text,'Try 1')] and [contains(@text,'free')]")
            #TODO Remove. This is not in the spec
            self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
        elif ex_subscriber:
            self.verify_exists(name='Get Started')
            #TODO Remove next 3 lines. Not in the spec
            self.verify_exists(name='Note: CBS All Access subscription required to enjoy Live TV')
            self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
            self.verify_not_exists(name='Already have an account? Sign In')
            #TODO add verify_not_exists 'Already have CBS ALL ACCESS? Sign In'
            #TODO add Should NOT have text: 'TRY 1 WEEK FREE'

        else:
            #TODO remove next line. It is not in the spec
            self.verify_exists(id=self.com_cbs_app + ':id/btnTryOneWeekFree')
            self.verify_exists(id=self.com_cbs_app + ':id/txtTakeTour')
            self.verify_not_exists(name='Already have an account? Sign In')
        #TODO There is no info in spec on special flow for phones. This is part of flow for non-subscriber. Even if it is phone only, it should be added to 'else' flow
        if self.phone:
            self.swipe_down_and_verify_if_exists(name='OR')
            self.swipe_down_and_verify_if_exists(name='TV PROVIDER')
            #TODO text should be changed to 'Stream CBS live with your cable or satellite provider'
            self.swipe_down_and_verify_if_exists(name='Stream Live TV with your cable, satellite or telco provider.', screenshot=True)
            self.swipe_down_and_verify_if_exists(name='Verify Now')
            #TODO remove next line comment
            # self.swipe_down_and_verify_if_exists(id_element='com.cbs.app:id/txtLearnMore')
            #TODO add next flow:
            # Learn More → Where is Live TV Available →
            # Live TV is available in many markets across the country and through select TV providers. →
            # CHECK AVAILABILITY [button] → What You Get with Live TV → You don’t have to worry
            # about missing a minute of your favorite shows. Stream your local news, hit CBS shows, special
            # events like The GRAMMYs and select sporting events at home or on the go across devices. →
            # SEE DEVICES [button] → Questions? → READ OUR FAQ → Disclaimer → Some
            # programming is not available for live streaming through CBS All Access. We are continuing to
            # work towards offering more live programming. In the meantime, when a program is not
            # available to you via CBS All Access, you will see a message that states that the program is
            # currently not available.

    def validation_at(self, category): #TODO update validation
        self.verify_exists(id="Main Menu", screenshot=False)
        self.verify_exists(id='Movies')
        self.verify_exists(id='Search')
        self.verify_exists(id='I want to see: %s' % category)

    def validation_al(self, anonymous=False):

        self.verify_exists(id=self.com_cbs_app + ':id/gridRecyclerView', screenshot=True)
        #TODO remove 'if' flow. Not in the spec.
        if not anonymous:
            self.verify_not_exists(xpath="//android.widget.TextView[contains(@text,'free CBS account.')]")
        self.verify_exists(name='Questions?')
        self.verify_exists(name='READ OUR FAQ')
        #TODO there is '+ <below user state validations>' in validations.pdf, but it is not clear.

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
