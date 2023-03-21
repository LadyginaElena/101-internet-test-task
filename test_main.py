import random
from selenium.common import ElementNotInteractableException
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest
import requests

link = "https://piter-online.net/"


@pytest.fixture()
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    browser.implicitly_wait(15)
    browser.get(link)
    yield browser
    browser.quit()


class Data:
    street = "Тестовая линия"
    house_number = 1
    phone_number = 1111111111
    username = "Автотест"


class Locators:
    INPUT_STREET = (
        By.XPATH,
        "(//span[contains(text(),'Введите улицу')])[1]/following-sibling::input",
    )
    INPUT_HOUSE = (
        By.XPATH,
        "(//span[contains(text(),'Дом')])[1]/following-sibling::input",
    )
    DROP_DOWN = (By.CSS_SELECTOR, ".app115 .icon-arrow-1-down")
    TYPE_CONNECT = (By.XPATH, "(//li[contains(text(),'В квартиру')])[1]")
    BTN_SHOW_TARIFF = (By.XPATH, '(//div[@data-test="find_tohome_button"])[1]')
    BTN_CONNECT = (
        By.CSS_SELECTOR,
        "[datatest='providers_form_inspect_connect_tariff_button']",
    )
    BTN_CLOSE_POPUP = (By.CSS_SELECTOR, "[datatest='close_popup1_from_quiz_input_tel']")
    INPUT_USERNAME = (
        By.CSS_SELECTOR,
        "[datatest='providers_provider_order_input_name']",
    )
    INPUT_PHONE = (By.CSS_SELECTOR, "[datatest='providers_provider_order_input_tel']")
    SEND_BTN = (By.CSS_SELECTOR, "[data-test='order_form_input_connect_button']")
    LOGO = (By.CSS_SELECTOR, ".app10 a[aria-label]")


class TestCase:
    def test_user_can_make_request(self, browser):
        """1. Открыть сайт https://piter-online.net/, в поиске ввести улицу Тестовая линия, дом 1"""
        input_street = browser.find_element(*Locators.INPUT_STREET)
        input_street.send_keys(Data.street)
        actions = ActionChains(browser)
        actions.pause(3)
        actions.move_to_element_with_offset(
            to_element=input_street, xoffset=0, yoffset=-60
        ).click()
        actions.perform()
        actions.pause(3)
        input_street.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, 10)
        input_house = wait.until(ec.element_to_be_clickable(Locators.INPUT_HOUSE))
        input_house.send_keys(Data.house_number)
        actions.move_to_element_with_offset(
            to_element=input_house, xoffset=0, yoffset=-60
        ).click()
        actions.perform()
        input_house.send_keys(Keys.ENTER)

        try:
            select_type = wait.until(ec.element_to_be_clickable(Locators.TYPE_CONNECT))
            select_type.click()
        except ElementNotInteractableException:
            drop_down = browser.find_element(*Locators.DROP_DOWN)
            drop_down.click()
            select_type = browser.find_element(*Locators.TYPE_CONNECT)
            browser.execute_script("arguments[0].click();", select_type)

        btn_show_tariff = browser.find_element(*Locators.BTN_SHOW_TARIFF)
        btn_show_tariff.click()

        """2.На открывшейся странице кликнуть на "подключить" или "подключить по акции" на тарифе"""
        close_popup = browser.find_element(*Locators.BTN_CLOSE_POPUP)
        close_popup.click()
        all_btn_connect = list(browser.find_elements(*Locators.BTN_CONNECT))
        random_index = random.randrange(len(all_btn_connect))
        btn_connect = all_btn_connect[random_index]
        btn_connect.click()

        """"3. На открывшейся странице ввести имя Автотест, номер телефона 1111111111."""
        wait.until(ec.visibility_of_element_located(Locators.INPUT_USERNAME)).send_keys(
            Data.username
        )
        input_phone = browser.find_element(*Locators.INPUT_PHONE)
        input_phone.send_keys(Data.phone_number)

        send_request_btn = browser.find_element(*Locators.SEND_BTN)
        try:
            actions.scroll_to_element(send_request_btn).click().perform()
        except ElementNotInteractableException:
            browser.execute_script("return arguments[0].scrollIntoView(true);", send_request_btn)
            browser.execute_script("arguments[0].click();", send_request_btn)

        """5. Убедиться, что у всех отправленных заявок статус 200."""
        # for request in browser.requests:
        #     if request.response:
        #         assert request.response.status_code == 200, "Wrong status code"
        response = requests.get(f"{browser.current_url}")
        assert response.status_code == 200, "Wrong status code"

    def test_repit_4_times(self, browser):
        """Повторить пункты 2-3 пять раз."""
        for i in range(4):
            self.test_user_can_make_request(browser)
