from time import sleep

from helper.cbs import CommonHelper


class BasePage(CommonHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

    def btn_search_icon(self, timeout=10):
        return self.get_element(timeout=timeout, name='Search Action')

    def img_logo(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/title_badge')

    def navigation_drawer(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/browse_headers')

    def txt_search_field(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/lb_search_text_editor')

    def btn_discover_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('DISCOVER')

    def btn_shows_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('SHOWS')

    def btn_live_tv_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('LIVE TV')

    def btn_settings_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name('SETTINGS')

    def get_menu_item_with_text(self, text, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_name(text)

    def get_element_with_text(self, text, timeout=10):
        return self.get_element(timeout=timeout, name=text)

    def open_drawer(self):
        """
        Opens side drawer if it's not open.  If we're up a level (viewing a show) it will go back, then open the drawer.
        """
        if not self.is_drawer_open():
            self.back()

        sleep(1.5)

    def is_drawer_open(self):
        return self.btn_discover_menu_item().is_displayed()

    def goto_discover(self, close_drawer=True):
        self.open_drawer()
        self.click(element=self.btn_shows_menu_item())
        if close_drawer is True:
            self.click(element=self.btn_shows_menu_item())

    def goto_shows(self, close_drawer=True):
        self.open_drawer()
        self.click(element=self.btn_shows_menu_item())
        if close_drawer is True:
            self.click(element=self.btn_shows_menu_item())

    def goto_live_tv(self, close_drawer=True):
        self.open_drawer()
        self.click(element=self.btn_live_tv_menu_item())
        if close_drawer is True:
            self.click(element=self.btn_live_tv_menu_item())

    def goto_settings(self, close_drawer=True):
        self.open_drawer()
        self.click(element=self.btn_settings_menu_item())
        if close_drawer is True:
            self.click(element=self.btn_settings_menu_item())

    def goto_show(self, show_name):
        self.goto_discover()
        self.click(element=self.btn_search_icon())

        self.send_keys(data=show_name, element=self.txt_search_field())
        self._hide_keyboard()
        sleep(5)

        self.click(element=self.get_elements(timeout=10, id=self.com_cbs_app + ':id/imgPoster')[0])
        sleep(10)

    def validate_menu(self):
        self.verify_exists(element=self.btn_discover_menu_item(), screenshot=True)
        self.verify_exists(element=self.btn_shows_menu_item())
        self.verify_exists(element=self.btn_live_tv_menu_item())
        self.verify_exists(element=self.btn_settings_menu_item())
        self.verify_exists(element=self.btn_search_icon())

    def validate_menu_is_hidden(self):
        self.assertTrueWithScreenShot(not self.is_drawer_open(), screenshot=True, msg="Menu should be hidden")







