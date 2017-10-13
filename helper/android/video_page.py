from time import time
from helper.android.show_page import BasePage


class VideoPage(BasePage):
    def __init__(self, driver, event):
        super(VideoPage, self).__init__(driver, event)

    def btn_play_from_beginning(self, timeout=10):
        return self.get_element(timeout=timeout, name='PLAY FROM BEGINNING')

    def btn_continue_playing(self, timeout=10):
        return self.get_element(timeout=timeout, name='Continue Playing')

    def video_player_screen(self, timeout=10):
        return self.get_element(timeout=timeout, id=self.com_cbs_app + ':id/playerMainContainer')

    def wait_for_video_to_start(self, buffer_wait=60):
        """
        Waits for video skin to appear
        This method is problematic because sometimes the loading spinner does not appear at all, and if we wait
        60 seconds, the entire pre-roll ad may finish playing.
        """

        start_time = time()
        self.exists(id=self.com_cbs_app + ':id/loading', timeout=buffer_wait)

        elapsed_time = time() - start_time
        timeout = buffer_wait - elapsed_time

        # make sure we're not still spinning/buffering
        ex = self.not_exists(id=self.com_cbs_app + ':id/loading', timeout=timeout)
        self.assertTrueWithScreenShot(ex, screenshot=False, msg="Assert that video buffer spinner disappears")