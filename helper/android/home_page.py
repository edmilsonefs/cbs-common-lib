from time import sleep

from helper.android.base_page import BasePage

PAID = "paid"


class HomePage(BasePage):
    def __init__(self, driver, event):
        super(HomePage, self).__init__(driver, event)

    def click_all_access_video(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_name('Free Episodes')
            self._short_swipe_down(duration=3000)
        except:
            self.driver.implicitly_wait(60)
            pass
        if self.exists(name=PAID, timeout=5):
            list_episodes = self.driver.find_elements_by_name(PAID)
            self.click(element=list_episodes[0])
        else:
            prime_container = self._find_element(
                xpath="//android.widget.LinearLayout[./android.widget.TextView[contains(@text,'Primetime')]]")
            for _ in range(0, 40):
                self._short_swipe_left(prime_container, 500)
            count = 0
            while count < 70:
                self._short_swipe_left(prime_container, 1000)
                if self.exists(name=PAID, timeout=5):
                    list_episodes = self.driver.find_elements_by_name(PAID)
                    self.click(element=list_episodes[0])
                    break
                else:
                    count += 1
