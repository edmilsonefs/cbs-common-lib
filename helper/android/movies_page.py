from helper.android.base_page import BasePage


class MoviesPage(BasePage):
    def __init__(self, driver, event):
        super(MoviesPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Movies']")

    def video_thumbnail(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/imgThumbnail")

    def btn_movie_poster(self, timeout=10):
        return self.get_element(timeout=timeout, id= self.com_cbs_app + ":id/movieImage")

    def txt_movie_name(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/txtMovieName")

    def txt_meta_data(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/txtMovieMetadata")

    def txt_movie_description(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/txtMovieDescription")

    def btn_subscribe_to_watch(self, timeout=10):
        return self.get_element(timeout=timeout, name="SUBSCRIBE TO WATCH")

    def btn_watch_movie(self, timeout=10):
        return self.get_element(timeout=timeout, name="WATCH MOVIE")

    def validate_page(self, user_type='anonymous', category='All Shows'):
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True)
        self.verify_exists(element=self.img_logo())
        self.verify_exists(element=self.btn_search_icon())
        self.verify_exists(element=self.lbl_title())
        self.verify_exists(element=self.btn_movie_poster())
        # self.verify_exists(xpath="//*[@text='I want to see:']", timeout=20)
        # self.verify_exists(xpath="//*[@text='" + category + "']")
        if user_type in [self.cf_subscriber, self.subscriber, self.trial]:
            pass
        else:
            pass

    def movie_details_popup_validation(self, user_type='anonymous'):
        self.verify_exists(element=self.video_thumbnail())
        self.verify_exists(element=self.txt_movie_name())
        self.verify_exists(element=self.txt_meta_data())
        self.verify_exists(element=self.txt_movie_description())
        if user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            self.verify_exists(element=self.btn_subscribe_to_watch())
            self.verify_not_exists(element=self.btn_watch_movie())
        else:
            self.verify_exists(element=self.btn_watch_movie())
            self.verify_not_exists(element=self.btn_subscribe_to_watch())