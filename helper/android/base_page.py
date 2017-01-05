from time import sleep

from helper.cbs import CommonHelper


class BasePage(CommonHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

    def top_toolbar(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/toolbar')

    def search_icon(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/action_search')

    def search_field(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/search_src_text')

    def title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_class_name('android.widget.TextView')

    def navigate_up(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Navigate up')

    def hamburger_menu(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Open navigation drawer')

    def logo(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_class_name('android.widget.ImageView')

    def navigation_drawer(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/navigation_drawer_root')

    def sign_in_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/userNameView')

    def user_status_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_id(self.com_cbs_app + ':id/userStatusTextView')

    def home_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Home')

    def shows_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Shows')

    def live_tv_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Live TV')

    def schedule_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Schedule')

    def shop_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Shop')

    def settings_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('Settings')

    def get_menu_item_with_text(self, text, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name(text)

    def get_element_with_text(self, text, timeout=10):
        return self.get_element(timeout=timeout, name=text)

    def open_drawer(self):
        """
        Opens side drawer if it's not open.  If we're up a level (viewing a show) it will go back, then open the drawer.
        """
        el = self.exists(element=self.hamburger_menu(timeout=3))
        if el:
            el.click()
        else:
            # maybe we're a level deeper.  Try going back.
            self.go_back()

            # if the drawer is NOT already open, try again and throw err on failure
            if not self.is_drawer_open():
                self.click(element=self.hamburger_menu())

        sleep(1.5)

    def is_drawer_open(self):
        return not self.exists(element=self.hamburger_menu(timeout=3))

    def close_drawer(self):
        self.back()






