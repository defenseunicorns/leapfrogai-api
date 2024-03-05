import os
import threading
import unittest
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestParallelization(unittest.IsolatedAsyncioTestCase):
    target_file = None
    driver = None
    failures = 0

    @classmethod
    def setUpClass(cls):
        cls.url = os.environ["API_ADDRESS"]
        cls.target_file = "0min12sec.wav"

    def file_exists(self, temp_file_path, file_name):
        return os.path.exists(temp_file_path + file_name)

    def file_open(self, temp_file_path, file_name):
        file = open(temp_file_path + file_name, "r")
        file_text = file.read()
        file.close()
        return file_text

    def parallel_upload(self):
        temp_file_path = os.path.abspath("/tmp/" + str(uuid.uuid4())) + "/"
        os.mkdir(temp_file_path)

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": temp_file_path,
                "download.prompt_for_download": False,
                "profile.default_content_settings.popups": 0,
            },
        )
        driver = webdriver.Chrome(options=options)

        # Load the DougTranslate Page
        driver.get(self.url)

        # Wait for the page to load
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Find and click start button
        audio_start_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Upload an Audio File')]"
        )
        audio_start_button.click()

        # Find file submission form
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")

        # Select the test file
        file_input.send_keys(os.path.abspath("../data/" + self.target_file))

        # Find and click upload button
        upload_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Upload')]"
        )
        upload_button.click()

        download_transcript_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(), 'Download Transcript')]")
            )
        )
        download_transcript_button.click()

        transcription_file_name = self.target_file + "-transcript.txt"
        wait = WebDriverWait(driver, timeout=30)
        wait.until(lambda d: self.file_exists(temp_file_path, transcription_file_name))

        transcription_file_content = self.file_open(
            temp_file_path, transcription_file_name
        )

        self.assertEqual(
            transcription_file_content.strip(),
            "I don't oppose war in all circumstances and when I look "
            "out over this crowd today I know there is no shortage of "
            "patriots or patriotism When I do oppose is a dumb war",
        )

        # Find and click summarize button
        summarize_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Summarize')]"
        )
        summarize_button.click()

        # Wait for the "Download Summary" button to appear
        download_summary_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(), 'Download Summary')]")
            )
        )
        download_summary_button.click()

        summary_file_name = self.target_file + "-summary.txt"
        wait = WebDriverWait(driver, timeout=30)
        wait.until(lambda d: self.file_exists(temp_file_path, summary_file_name))

        summary_file_content = self.file_open(temp_file_path, summary_file_name)

        self.assertTrue(summary_file_content.count("BOTTOM LINE UP FRONT:") == 1)
        self.assertTrue(summary_file_content.count("NOTES:") == 1)
        self.assertTrue(summary_file_content.count("ACTION ITEMS:") == 1)
        self.failures -= 1
        driver.quit()
        os.rmdir(temp_file_path)

    async def test_parallel_upload(self):
        threads = []
        test_count = 3
        self.failures = test_count

        for i in range(test_count):
            t = threading.Thread(target=self.parallel_upload)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(0, self.failures)


if __name__ == "__main__":
    unittest.util._MAX_LENGTH = 300
    unittest.main()
