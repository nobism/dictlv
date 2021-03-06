import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class SimpleTranslationTest(FunctionalTest):
    fixtures = ['translations.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def test_can_translate_a_word_in_english_and_latvian(self):
        # Karlis has heard of this cool new translator. He checks it out on his
        # browser.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention an English/Latvian
        # translator.
        self.assertIn('EN ⇆ LV', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('DictLV', header_text)

        # He's invited to enter a word to translate.
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Enter a word to translate')

        # He decides to put a word in English, "hello".
        inputbox.send_keys('hello')

        # When he hits enter he sees that his search term is returned
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_results_table('hello')

        # And a translation appears underneath it!
        self.wait_for_row_in_results_table('sveiki')

        # He checks if a Latvian word will work, he puts it in and hits enter.
        inputbox = self.get_item_input_box()
        inputbox.clear()
        inputbox.send_keys('sveiki')
        inputbox.send_keys(Keys.ENTER)

        # Again a translation appears!
        self.wait_for_row_in_results_table('hello')

        # Satisfied, he goes back to sleep

    def test_search_terms_dont_need_latvian_special_characters(self):
        # Karlis hates typing in the Latvian special characters on his English
        # keyboard. He wants to find out if the translator is smart enough to
        # recognise a Latvian word which isn't spelt with these characters.

        # He opens up his browser and navigates to the translator
        self.browser.get(self.live_server_url)

        # He omits the special character in his search term
        inputbox = self.get_item_input_box()
        inputbox.send_keys('pilseta')

        # When he hits enter he gets a 'Did you mean?' prompt with his intended
        # translation
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_results_table('Did you mean?')
        self.wait_for_row_in_results_table('pilsēta')

        # When he clicks it, he gets the translation!
        self.browser.find_element_by_link_text('pilsēta').click()
        self.wait_for_row_in_results_table('town')

        # Satisfied, he goes back to sleep

    def test_can_search_with_spaces(self):
        # Karlis opens his favourite translator
        self.browser.get(self.live_server_url)

        # He searches for something which has a space
        inputbox = self.get_item_input_box()
        inputbox.send_keys('train station')
        inputbox.send_keys(Keys.ENTER)

        # When he clicks it, he gets the translation!
        self.wait_for_row_in_results_table('vilciena stacija')

        # He also sees that the url can be easily reproduced himself
        self.assertIn("train+station", self.browser.current_url)

        # Satisfied, he goes back to sleep

    def test_can_search_with_or_without_question_mark(self):
        # Karlis opens his favourite translator
        self.browser.get(self.live_server_url)

        # He searches for something which has a question mark
        inputbox = self.get_item_input_box()
        inputbox.send_keys('what is the time?')
        inputbox.send_keys(Keys.ENTER)

        # When he clicks it, he gets the translation!
        self.wait_for_row_in_results_table('cik ir pulkstenis?')

        inputbox = self.get_item_input_box()
        inputbox.clear()
        inputbox.send_keys('what is the time')
        inputbox.send_keys(Keys.ENTER)

        # When he clicks it, he gets the translation!
        self.wait_for_row_in_results_table('cik ir pulkstenis?')

        # Satisfied, he goes back to sleep

    def test_layout_and_styling(self):
        # Karlis goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=10)
