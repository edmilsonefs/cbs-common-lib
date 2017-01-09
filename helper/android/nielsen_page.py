from helper.android.base_page import BasePage


class NielsenPage(BasePage):
    def __init__(self, driver, event):
        super(NielsenPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_name('Nielsen Info & Your Choices')

    def btn_opt_out(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//android.view.View[contains(@content-desc,'click here')][1]")

    def btn_opt_in(self, timeout=10):
        return self.get_element(timeout=timeout, xpath="//android.view.View[contains(@content-desc,'click here')][2]")

    def btn_ok(self, timeout=10):
        return self.get_element(timeout=timeout, name='OK')







