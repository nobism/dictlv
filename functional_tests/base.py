import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait(fn):

        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)

        return modified_fn

    @wait
    def wait_for_row_in_results_table(self, row_text):
        table = self.browser.find_element_by_id('id_results_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text.lower(), [row.text.lower() for row in rows])
