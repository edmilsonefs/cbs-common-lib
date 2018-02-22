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
        self.btn_schedule_menu_item_selector = "//*[@text='Schedule']"
        self.btn_movies_menu_item_selector = "//*[@text='Movies']"
        self.btn_shop_menu_item_selector = "//*[@text='Shop']"
        self.btn_settings_menu_item_selector = "//*[@text='Settings']"
        self.btn_upgrade_menu_item_selector = "//*[@text='Upgrade']"
        self.btn_subscribe_menu_item_selector = "//*[@text='Subscribe']"
        self.txt_welcome_to_cbs_selector = 'Welcome to the CBS app'
        self.txt_by_using_this_app_selector = 'By using this CBS Application, you agree to our:'
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
        return self.get_element(timeout=timeout, accessibility_id='Navigate up')

    def btn_hamburger_menu(self, timeout=10):
        return self.get_element(timeout=timeout, accessibility_id='Open navigation drawer')

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

    def open_drawer(self):
        """
        Opens side drawer if it's not open.  If we're up a level (viewing a show) it will go back, then open the drawer.
        """
        el = self.exists(element=self.btn_hamburger_menu(timeout=10))
        if el:
            el.click()
        else:
            # maybe we're a level deeper.  Try going back.
            self.back_while_open_drawer_is_visible()

            # if the drawer is NOT already open, try again and throw err on failure
            if not self.is_drawer_open():
                self.click(element=self.btn_hamburger_menu())

        sleep(1.5)

    def is_drawer_open(self):
        return not self.exists(element=self.btn_hamburger_menu(timeout=3))

    def is_navigate_up_visible(self):
        return self.exists(element=self.btn_navigate_up(timeout=5))

    def close_drawer(self):
        self.back()

    def goto_home(self):
        self.back_while_open_drawer_is_visible()
        self.open_drawer()
        self.click(element=self.btn_home_menu_item())

    def goto_shows(self):
        self.back_while_open_drawer_is_visible()
        self.open_drawer()
        self.click(element=self.btn_shows_menu_item())
        self.wait_for_show_page_to_load()

    def goto_subscribe(self):
        self.open_drawer()
        self.click(element=self.btn_user_status_menu_item())

    def goto_live_tv(self):
        self.back_while_open_drawer_is_visible()
        self.open_drawer()
        self.click(element=self.btn_live_tv_menu_item())
        self.safe_screenshot()
        self.click_allow_popup()
        self.safe_screenshot()
        self.click_allow_popup()
        self.safe_screenshot()

    def goto_schedule(self):
        self.open_drawer()
        self.click(element=self.btn_schedule_menu_item())

    def goto_movies(self):
        self.open_drawer()
        self.click(element=self.btn_movies_menu_item(), screenshot=True)

    def goto_settings(self):
        self.back_while_open_drawer_is_visible()
        self.open_drawer()
        self.click(element=self.btn_settings_menu_item())

    def goto_show(self, show_name):
        self.click(element=self.btn_search_icon(), screenshot=True)
        self.wait_for_show_page_to_load()

        self.send_keys(data=show_name, element=self.txt_search_field())
        self._hide_keyboard()
        sleep(5)

        self.click_first_search_result()
        sleep(10)
        self.close_big_advertisement()

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





