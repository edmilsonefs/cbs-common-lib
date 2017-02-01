from helper.android.base_page import BasePage


class ShowPage(BasePage):
    def __init__(self, driver, event):
        super(ShowPage, self).__init__(driver, event)

    def btn_episode_indicator(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/allAccessEpisodesContainer')

    def lbl_total_episode_count(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/totalEpisodeCount')

    def btn_all_access_episodes(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/txtAllAccessEpisodes')

    def lst_video_icons(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/imgThumbnail')

    def show_page_header(self, timeout=10):
        return self.get_elements(timeout=timeout, id=self.com_cbs_app + ':id/imgHeader')

    def btn_clips(self, timeout=10):
        self.get_element(timeout=timeout, name='Clips')

    def btn_free(self, timeout=10):
        self.get_element(timeout=timeout, name='Free')

    def btn_full_episodes(self, timeout=10):
        self.get_element(timeout=timeout, name='Full Episodes')

    def btn_more_options(self, timeout=10):
        self.get_element(timeout=timeout, name='More options')

    def btn_like_on_facebook(self, timeout=10):
        self.get_element(timeout=timeout, name='Like on Facebook')

    def btn_follow_on_twitter(self, timeout=10):
        self.get_element(timeout=timeout, name='Follow on Twitter')

    def btn_share(self, timeout=10):
        self.get_element(timeout=timeout, name='Share')

    def btn_see_all(self, timeout=10):
        self.get_element(timeout=timeout, name='See all')

    def btn_show_info(self, timeout=10):
        self.get_element(timeout=timeout, name='Show Info')

    def btn_my_cbs(self, timeout=10):
        self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/imgMyCbsToggle')

    def btn_watch_episode(self, timeout=10):
        self.get_element(timeout=timeout, name='Watch Episode')

    def txt_all_access_episode(self, timeout=10):
        self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/txtAllAccessEpisodes')

    def txt_show_name(self, timeout=10):
        self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/txtShowName')

    def txt_episode_name(self, timeout=10):
        self.get_element(timeout=timeout, id=':id/txtEpisodeName')

    def txt_air_date(self, timeout=10):
        self.get_element(timeout=timeout, id=':id/txtAirDate')

    def txt_episode_description(self, timeout=10):
        self.get_element(timeout=timeout, id=':id/txtDescription')

    def validate_page(self):
        self.verify_exists(element=self.btn_navigate_up(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lst_video_icons())
        self.verify_exists(element=self.btn_more_options())
        self.verify_exists(element=self.btn_my_cbs())
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
