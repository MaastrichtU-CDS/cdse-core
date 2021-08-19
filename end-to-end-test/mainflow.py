import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
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
        self.login_keycloak(driver)

        # access main dashboard
        self.wait_for_element_with_id(driver, "content-main", 5)
        assert "Site administration | Django site admin" in driver.title

        # start prediction
        start_button = driver.find_element_by_xpath(
            "//a[@class='next-button' and @href='/prediction/start/']"
        )
        start_button.click()

        self.wait_for_element_with_id(driver, "main", 5)
        assert "Prediction - Start" in driver.title

        select_fhir_endpoint_dropdown = Select(
            driver.find_element_by_id("fhir_endpoint_id")
        )
        select_fhir_endpoint_dropdown.select_by_value("3")

        patient_id_input = driver.find_element_by_id("patient_id")
        patient_id_input.send_keys("1")

        select_model_dropdown = Select(driver.find_element_by_id("selected_model_uri"))
        select_model_dropdown.select_by_visible_text("Rectal cancer BN model.")

        next_button = driver.find_element_by_xpath(
            "//button[@class='next-button' and @value='next_screen']"
        )
        next_button.click()

        # prepare prediction
        self.wait_for_element_with_id(driver, "C48885", 10)
        assert "Prediction - Prepare" in driver.title

        assert "Peter James Chalmers" in driver.page_source
        assert "1974-12-25" in driver.page_source
        assert "Generic Primary Tumor TNM Finding" in driver.page_source
        assert "Generic Regional Lymph Nodes TNM Finding" in driver.page_source
        assert "T3 Stage Finding" in driver.page_source
        assert "N1 Stage Finding" in driver.page_source

        select_manual_override_one = Select(
            driver.find_element_by_id("C48885-override")
        )
        select_manual_override_one.select_by_value("C48720")

        next_button = driver.find_element_by_xpath(
            "//button[@class='next-button' and @value='start_prediction']"
        )
        next_button.click()

        # loading page
        self.wait_for_element_with_id(driver, "loader", 30)
        assert "Prediction - Loading" in driver.title

        # result page
        self.wait_for_element_with_id(driver, "result", 30)
        assert "Prediction - Result" in driver.title

        assert "Pathologic Primary Tumor TNM Finding" in driver.page_source
        assert "Pathologic Regional Lymph Nodes TNM Finding" in driver.page_source

        assert "0.15" in driver.page_source
        assert "0.08" in driver.page_source
        assert "0.48" in driver.page_source
        assert "0.14" in driver.page_source
        assert "0.04" in driver.page_source
        assert "0.08" in driver.page_source

        assert "0.48" in driver.page_source
        assert "0.40" in driver.page_source
        assert "0.09" in driver.page_source
        assert "0.01" in driver.page_source

        assert "Show / hide advanced view" in driver.page_source

    def tearDown(self):
        self.driver.quit()

    # @staticmethod
    # def login_local(driver):
    #     # login procedure
    #     login_button = driver.find_element_by_link_text("login")
    #     login_button.click()
    #
    #     login_input = driver.find_element_by_id("id_username")
    #     login_input.send_keys("leroy")
    #     password_input = driver.find_element_by_id("id_password")
    #     password_input.send_keys("Qwerty1$")
    #
    #     login_button = driver.find_element_by_xpath(
    #         "//input[@type='submit' and @value='Log in']"
    #     )
    #     login_button.click()

    @staticmethod
    def login_keycloak(driver):
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

    @staticmethod
    def wait_for_element_with_id(driver, element_id, timout):
        try:
            element_present = EC.presence_of_element_located((By.ID, element_id))
            WebDriverWait(driver, timout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")


if __name__ == "__main__":
    unittest.main()
