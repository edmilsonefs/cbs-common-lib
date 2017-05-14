from time import sleep

from helper.cbs import CommonHelper


class BasePage(CommonHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

    def top_toolbar(self, timeout=60):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/toolbar')

    def btn_search_icon(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/action_search')

    def txt_search_field(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/search_src_text')

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_class_name('android.widget.TextView')

    def btn_navigate_up(self, timeout=10):
        return self.get_element(timeout=timeout, name='Navigate up')

    def btn_hamburger_menu(self, timeout=10):
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
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Home']")

    def btn_shows_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Shows']")

    def btn_live_tv_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Live TV']")

    def btn_schedule_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Schedule']")

    def btn_movies_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Movies']")

    def btn_shop_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Shop']")

    def btn_settings_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Settings']")

    def btn_upgrade_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Upgrade']")

    def btn_subscribe_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='Subscribe']")

    def get_menu_item_with_text(self, text, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@text='" + text + "']")

    def get_element_with_text(self, text, timeout=10):
        return self.get_element(timeout=timeout, name=text)

    def open_drawer(self):
        """
        Opens side drawer if it's not open.  If we're up a level (viewing a show) it will go back, then open the drawer.
        """
        el = self.exists(element=self.btn_hamburger_menu(timeout=3))
        if el:
            el.click()
        else:
            # maybe we're a level deeper.  Try going back.
            self.go_back()

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

    def validate_menu_page(self, name):
        if self.user_type == self.anonymous:
            self.verify_exists(element=self.btn_sign_in_menu_item())
        else:
            self.verify_exists(name=name)
        if self.user_type in [self.subscriber, self.trial]:
            self.verify_exists(element=self.btn_upgrade_menu_item())
        elif self.user_type == self.cf_subscriber:
            self.verify_not_exists(element=self.btn_upgrade_menu_item())
            self.verify_not_exists(element=self.btn_subscribe_menu_item())
        else:
            self.verify_exists(element=self.btn_subscribe_menu_item())
        self.verify_exists(element=self.btn_settings_menu_item(), screenshot=True)
        self.verify_exists(element=self.btn_home_menu_item())
        self.verify_exists(element=self.btn_shows_menu_item())
        self.verify_exists(element=self.btn_live_tv_menu_item())
        self.verify_exists(element=self.btn_schedule_menu_item())
        self.verify_exists(element=self.btn_shop_menu_item())






