import os
from time import sleep

from helper.ios_cbs import CommonIOSHelper


class BasePage(CommonIOSHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

    def btn_search_icon(self, timeout=10):
        return self.get_element(timeout=timeout, id='Search')

    def txt_search_field(self, timeout=10):
        return self.get_element(timeout=timeout, id='Search for a Show')

    def lbl_title(self, timeout=10):
        return self.get_element(timeout=timeout, xpath='//UIAStaticText[1]')

    def btn_navigate_up(self, timeout=10):
        return self.get_element(timeout=timeout, id='BackArrow_white')

    def btn_hamburger_menu(self, timeout=10):
        return self.get_element(timeout=timeout, id='Main Menu')

    def img_logo(self, timeout=10):
        return self.get_element(timeout=timeout, id='CBSLogo_white')

    def navigation_drawer(self, timeout=10):
        if os.environ['AUTOMATION_NAME'] == 'XCUITest':
            return self.get_element(timeout=timeout, name='Main Menu')
        else:
            return self.get_element(timeout=timeout, xpath='//UIATableView[1]')

    def btn_sign_in_menu_item(self, timeout=10):
        return self.get_elements(timeout=timeout, id='Sign In')[0]

    def btn_user_status_menu_item(self, timeout=10):
        return self.get_elements(timeout=timeout, id='Subscribe')[0]

    def btn_home_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Home']")

    def btn_shows_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Shows']")

    def btn_live_tv_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Live TV']")

    def btn_schedule_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Schedule']")

    def btn_store_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Store']")

    def btn_settings_menu_item(self, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='Settings']")

    def get_menu_item_with_text(self, text, timeout=10):
        return self.navigation_drawer(timeout=timeout).find_element_by_xpath("//*[@name='" + text + "']")

    def get_element_with_text(self, text, timeout=10):
        return self.get_element(timeout=timeout, id=text)

    def open_drawer(self):
        e = self.exists_and_visible(element=self.btn_hamburger_menu(timeout=5), timeout=5)

        if not e:
            self.go_back()
            sleep(1)
            e = self.exists_and_visible(element=self.btn_hamburger_menu(timeout=5), timeout=5)

        if e.location['x'] > 80:
            return

        if e:
            e.click()
        else:
            self.go_back()
            sleep(1)
            self.click(element=self.btn_hamburger_menu(timeout=5))

    def close_drawer(self):
        e = self.exists_and_visible(element=self.btn_hamburger_menu(timeout=5))

        if e.location['x'] < 80:
            return

        if e:
            e.click()
        else:
            self.go_back()
            sleep(1)
            self.click(element=self.btn_hamburger_menu(timeout=5))

    def goto_home(self):
        self.open_drawer()
        self.click(element=self.btn_home_menu_item())

    def goto_shows(self):
        self.open_drawer()
        self.click(element=self.btn_shows_menu_item())

    def goto_subscribe(self):
        self.open_drawer()
        self.click(element=self.btn_user_status_menu_item())

    def goto_live_tv(self):
        self.open_drawer()
        self.click(element=self.btn_live_tv_menu_item())
        self._accept_alert(2)

    def goto_schedule(self):
        self.open_drawer()
        self.click(element=self.btn_schedule_menu_item())

    def goto_settings(self):
        self.open_drawer()
        self.click(element=self.btn_settings_menu_item())

    def goto_show(self, show_name):
        self.search_for(show_name)
        self.click_first_search_result()
        t_f = self.exists(xpath="//UIAButton[contains(@name,'MyCBSStar')]", timeout=30)

        self.assertTrueWithScreenShot(t_f, msg="Assert we're on individual show page")

        self.send_keys(data=show_name, element=self.txt_search_field())
        self._hide_keyboard()
        sleep(5)

        self.click_first_search_result()
        sleep(10)






