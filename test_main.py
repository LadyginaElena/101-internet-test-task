import random
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.fixture()
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.headless = False
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    browser.implicitly_wait(15)
    yield browser
    browser.quit()


link = "https://piter-online.net/"

# TestData
street = "Тестовая линия"
house_number = 1
phone_number = 1111111111
username = "Автотест"

# Locators:
INPUT_STREET = (
    By.XPATH,
    "(//span[contains(text(),'Введите улицу')])[1]/following-sibling::input",
)
INPUT_HOUSE = (By.XPATH, "(//span[contains(text(),'Дом')])[1]/following-sibling::input")
DROP_DOWN = (By.CSS_SELECTOR, ".app115 .icon-arrow-1-down")
TYPE_CONNECT = (By.XPATH, "(//li[contains(text(),'В квартиру')])[1]")
BTN_SHOW_TARIFF = (By.XPATH, '(//div[@data-test="find_tohome_button"])[1]')
BTN_CONNECT = (
    By.CSS_SELECTOR,
    "[datatest='providers_form_inspect_connect_tariff_button']",
)
BTN_CLOSE_POPUP = (By.CSS_SELECTOR, "[datatest='close_popup1_from_quiz_input_tel']")
INPUT_USERNAME = (By.CSS_SELECTOR, "[datatest='providers_provider_order_input_name']")
INPUT_PHONE = (By.CSS_SELECTOR, "[datatest='providers_provider_order_input_tel']")
SEND_BTN = (By.XPATH, "//div[contains(text(),'Оставить заявку')]")
LOGO = (By.CSS_SELECTOR, ".app10 a[aria-label]")


def test_user_can_make_5_requests(browser):
    """1. Открыть сайт https://piter-online.net/, в поиске ввести улицу Тестовая линия, дом 1"""

    browser.get(link)
    """Повторить пункты  пять раз. """
    for i in range(5):
        input_street = browser.find_element(*INPUT_STREET)
        input_street.send_keys(street)
        actions = ActionChains(browser)
        actions.pause(2)
        actions.move_to_element_with_offset(
            to_element=input_street, xoffset=0, yoffset=-60
        ).click()
        actions.perform()
        input_street.send_keys(Keys.ENTER)

        input_house = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable(INPUT_HOUSE)
        )
        input_house.send_keys(house_number)
        input_house.send_keys(Keys.ENTER)

        drop_down = browser.find_element(*DROP_DOWN)
        drop_down.click()
        select_type = browser.find_element(*TYPE_CONNECT)
        select_type.click()

        btn_show_tariff = browser.find_element(*BTN_SHOW_TARIFF)
        btn_show_tariff.click()

        """2.На открывшейся странице кликнуть на "подключить" или "подключить по акции" на тарифе"""
        close_popup = browser.find_element(*BTN_CLOSE_POPUP)
        close_popup.click()
        all_btn_connect = list(browser.find_elements(*BTN_CONNECT))
        random_index = random.randrange(len(all_btn_connect))
        btn_connect = all_btn_connect[random_index]
        btn_connect.click()

        """"3. На открывшейся странице ввести имя Автотест, номер телефона 1111111111."""
        input_username = (
            WebDriverWait(browser, 10)
            .until(ec.visibility_of_element_located(INPUT_USERNAME))
            .send_keys(username)
        )
        input_phone = browser.find_element(*INPUT_PHONE)
        input_phone.send_keys(phone_number)
        send_request = browser.find_element(*SEND_BTN)
        send_request.click()

        """5. Убедиться, что у всех отправленных заявок статус 200."""
        request_last = browser.last_request
        assert request_last.response.status_code == 200, "Wrong status code"

        logo = browser.find_element(*LOGO)
        logo.click()
        assert f"{browser.current_url}" == f"{link}leningradskaya-oblast"
