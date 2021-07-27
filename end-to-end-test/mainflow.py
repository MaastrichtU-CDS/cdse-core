import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestMainFlow(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor="http://192.168.100.9:4444/wd/hub",
            desired_capabilities={
                "browserName": "firefox",
            },
        )

    def test_main_flow(self):
        driver = self.driver
        driver.get("http://192.168.100.9/")

        # login procedure
        login_button = driver.find_element_by_link_text("login")
        login_button.click()
        assert "Sign in to maastro" in driver.title

        login_input = driver.find_element_by_id("username")
        login_input.send_keys("leroy")
        password_input = driver.find_element_by_id("password")
        password_input.send_keys("Qwerty1$")

        login_button = driver.find_element_by_xpath(
            "//input[@type='submit' and @value='Sign In']"
        )
        login_button.click()

        # access main dashboard
        try:
            element_present = EC.presence_of_element_located((By.ID, "content-main"))
            WebDriverWait(driver, 5).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        assert "Site administration | Django site admin" in driver.title

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
