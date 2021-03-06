from time import sleep

from helper.cbs import CommonHelper

# Only for inheritance
class BasePage(CommonHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

        self.top_toolbar_selector = self.com_cbs_app + ':id/toolbar'
        self.btn_search_icon_selector = self.com_cbs_app + ':id/action_search'
        self.txt_search_field_selector = self.com_cbs_app + ':id/search_src_text'
        self.lbl_title_selector = 'android.widget.TextView'
        self.btn_navigate_up_selector = 'Navigate up'
        self.btn_hamburger_menu_selector = 'Open navigation drawer'
        self.img_logo_selector = 'android.widget.ImageView'
        self.navigation_drawer_selector = self.com_cbs_app + ':id/navigation_drawer_root'
        self.btn_sign_in_menu_item_selector = self.com_cbs_app + ':id/userNameView'
        self.btn_user_status_menu_item_selector = self.com_cbs_app + ':id/userStatusTextView'
        self.btn_home_menu_item_selector = "//*[@text='Home']"
        self.btn_shows_menu_item_selector = "//*[@text='Shows']"
        self.btn_live_tv_menu_item_selector = "//*[@text='Live TV']"
        self.btn_tv_provider_menu_item_selector = "//*[@text='TV Provider']"
        self.btn_schedule_menu_item_selector = "//*[@text='Schedule']"
        self.btn_movies_menu_item_selector = "//*[@text='Movies']"
        self.btn_shop_menu_item_selector = "//*[@text='Shop']"
        self.btn_settings_menu_item_selector = "//*[@text='Settings']"
        self.btn_upgrade_menu_item_selector = "//*[@text='Upgrade']"
        self.btn_subscribe_menu_item_selector = "//*[@text='Subscribe']"
        self.txt_welcome_to_cbs_selector = 'Welcome to the CBS app'
        self.txt_by_using_this_app_selector = 'Before you get started, please review and agree to the following:'
        self.btn_terms_of_use_selector = 'Terms of Use'
        self.btn_mobile_user_agreement_selector = 'Mobile User Agreement'
        self.btn_privacy_policy_selector = 'Privacy Policy'
        self.btn_video_services_selector = 'Video Services'
        self.btn_accept_selector = 'ACCEPT'


    def top_toolbar(self, timeout=60):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/toolbar')

    def btn_search_icon(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/action_search')

    def txt_search_field(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/search_src_text')

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_class_name('android.widget.TextView')

    def btn_navigate_up(self, timeout=10):
        if self.uiautomator2:
            return self.get_element(timeout=timeout, accessibility_id='Navigate up')
        return self.get_element(timeout=timeout, name='Navigate up')

    def btn_hamburger_menu(self, timeout=10):
        if self.uiautomator2:
            return self.get_element(timeout=timeout, accessibility_id='Open navigation drawer')
        return self.get_element(timeout=timeout, name='Open navigation drawer')

    def img_logo(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_class_name('android.widget.ImageView')

    def navigation_drawer(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/navigation_drawer_root')

    def btn_sign_in_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/userNameView')

    def btn_user_status_menu_item(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/userStatusTextView')

    def btn_home_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_home_menu_item_selector)

    def btn_shows_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_shows_menu_item_selector)

    def btn_live_tv_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_live_tv_menu_item_selector)

    def btn_tv_provider_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_tv_provider_menu_item_selector)

    def btn_schedule_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_schedule_menu_item_selector)

    def btn_movies_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_movies_menu_item_selector)

    def btn_shop_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_shop_menu_item_selector)

    def btn_settings_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_settings_menu_item_selector)

    def btn_upgrade_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_upgrade_menu_item_selector)

    def btn_subscribe_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath(self.btn_subscribe_menu_item_selector)

    def get_menu_item_with_text(self, text, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='" + text + "']")

    def get_element_with_text(self, text, timeout=10):
        return self.get_element(timeout=timeout, name=text)

    def is_navigate_up_visible(self):
        return self.exists(element=self.btn_navigate_up(timeout=5))

    def validate_menu_page(self, name):
        text_list = [
            'settings', 
            'home', 
            'shows', 
            'live tv', 
            'shop', 
            'subscribe'
            ]
        if self.user_type == self.anonymous:
            text_list.append('sign in')
        else:
            text_list.append(name)
        if self.user_type in [self.subscriber, self.trial]:
            text_list.append('upgrade')
        elif self.user_type == self.cf_subscriber:
            text_list.append('upgrade')
            text_list.append('subscribe')
        else:
            text_list.append('subscribe')
        self.verify_in_batch(text_list, False)

    def validate_tou_page(self):
        # Validation A   
        text_list = [
        self.txt_welcome_to_cbs_selector,
        self.txt_by_using_this_app_selector,
        self.btn_terms_of_use_selector,
        self.btn_mobile_user_agreement_selector,
        self.btn_privacy_policy_selector,
        self.btn_video_services_selector,
        self.btn_accept_selector
        ]
        self.verify_in_batch(text_list, False)





