from helper.cbs import CommonHelper


class BasePage(CommonHelper):
    def __init__(self, driver, event):
        self.driver = driver
        self.event = event
        self.init_variables()

    def top_toolbar(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/toolbar')

    def search_icon(self):
        return self.top_toolbar().find_element_by_id(self.com_cbs_app + ':id/action_search')

    def search_field(self):
        return self.top_toolbar().find_element_by_id(self.com_cbs_app + ':id/search_src_text')

    def title(self):
        return self.top_toolbar().find_element_by_class_name('android.widget.TextView')

    def navigate_up(self):
        return self.top_toolbar().find_element_by_name('Navigate up')

    def hamburger_menu(self):
        return self.top_toolbar().find_element_by_name('Open navigation drawer')

    def logo(self):
        return self.top_toolbar().find_element_by_class_name('android.widget.ImageView')
