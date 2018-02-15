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

    def validate_page(self):
        text_list = [
            'Open navigation drawer',
            'android.widget.ImageView',
            ':id/action_search',
            'Movies',
            ':id/movieImage'
            ]
        self.verify_in_batch(text_list, False, True, True, False, 20)

    def movie_details_popup_validation(self, user_type='anonymous'):
        text_list = [
            ':id/imgThumbnail',
            ':id/txtMovieName',
            ':id/txtMovieMetadata',
            ':id/txtMovieDescription'
            ]
        if user_type in [self.anonymous, self.ex_subscriber, self.registered]:
            text_list.append('SUBSCRIBE TO WATCH')
            self.verify_not_exists(element=self.btn_watch_movie(), name="WATCH MOVIE")
        else:
            text_list.append('WATCH MOVIE')
            self.verify_not_exists(element=self.btn_subscribe_to_watch(), name="SUBSCRIBE TO WATCH")
        self.verify_in_batch(text_list, False)
