from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class ShowsPage(BasePage):
    def __init__(self, driver, event):
        super(ShowsPage, self).__init__(driver, event)
