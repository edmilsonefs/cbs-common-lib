from helper.android.base_page import BasePage


class MoviesPage(BasePage):
    def __init__(self, driver, event):
        super(MoviesPage, self).__init__(driver, event)

    def lbl_title(self, timeout=10):
        return self.top_toolbar(timeout=timeout).find_element_by_xpath("//*[@text='Movies']")

    def video_thumbnail(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/imgThumbnail")

    def btn_movie_poster(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ":id/movieImage")

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
        self.verify_exists(element=self.btn_hamburger_menu(), screenshot=True, name='Open navigation drawer')
        self.verify_exists(element=self.img_logo(), class_name='android.widget.ImageView')
        self.verify_exists(element=self.btn_search_icon(), id=self.com_cbs_app + ':id/action_search')
        self.verify_exists(element=self.lbl_title(), xpath="//*[@text='Movies']")
        self.verify_exists(element=self.btn_movie_poster(), id=self.com_cbs_app + ":id/movieImage")
        # self.verify_exists(xpath="//*[@text='I want to see:']", timeout=20)
        # self.verify_exists(xpath="//*[@text='" + category + "']")
        if user_type in [self.cf_subscriber, self.subscriber, self.trial]:
            pass
        else:
            pass

    def movie_details_popup_validation(self, user_type='anonymous'):
        self.verify_exists(element=self.video_thumbnail(), id=self.com_cbs_app + ":id/imgThumbnail")
        self.verify_exists(element=self.txt_movie_name(), id=self.com_cbs_app + ":id/txtMovieName")
        self.verify_exists(element=self.txt_meta_data(), id=self.com_cbs_app + ":id/txtMovieMetadata")
        self.verify_exists(element=self.txt_movie_description(), id=self.com_cbs_app + ":id/txtMovieDescription")
        if user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            self.verify_exists(element=self.btn_subscribe_to_watch(), name="SUBSCRIBE TO WATCH")
            self.verify_not_exists(element=self.btn_watch_movie(), name="WATCH MOVIE")
        else:
            self.verify_exists(element=self.btn_watch_movie(), name="WATCH MOVIE")
            self.verify_not_exists(element=self.btn_subscribe_to_watch(), name="SUBSCRIBE TO WATCH")