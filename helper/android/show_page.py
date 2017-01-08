from helper.android.base_page import BasePage


class ShowPage(BasePage):
    def __init__(self, driver, event):
        super(ShowPage, self).__init__(driver, event)

    def btn_episode_indicator(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/allAccessEpisodesContainer')

    def validate_page(self):
        self.verify_exists(element=self.btn_navigate_up(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        # self.verify_exists(id=self.com_cbs_app + ':id/imgThumbnail')
        self.verify_exists(name='More options')
        # self.verify_exists(xpath="//*[@resource-id='" + self.com_cbs_app + ":id/imgMyCbsToggle']")
        if self.user_type in [self.anonymous, self.registered, self.ex_subscriber]:
            self.verify_exists(element=self.btn_episode_indicator())
        else:
            self.verify_not_exists(element=self.btn_episode_indicator())

    def click_all_access_video(self):
        if self.exists(name='paid', timeout=10):
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()
        else:
            self._short_swipe_down(duration=3000)
            self._short_swipe_down(duration=3000)
            list_episodes = self.driver.find_elements_by_name('paid')
            self.click(element=list_episodes[0])
            self.click_play_from_beginning()
