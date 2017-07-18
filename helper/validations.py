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

    def validation_at(self, category): #TODO update validation
        self.verify_exists(id="Main Menu", screenshot=False)
        self.verify_exists(id='Movies')
        self.verify_exists(id='Search')
        self.verify_exists(id='I want to see: %s' % category)
