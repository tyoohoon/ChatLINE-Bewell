from selenium.webdriver.chrome.webdriver import WebDriver
import constants as const
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def bypass_login_with_cookies(driver: WebDriver):
#     with open('ChatLINE\cookies.csv', encoding='utf-8-sig') as f:
#         dict_reader = DictReader(f)
#         list_of_dicts = list(dict_reader)
#     for i in list_of_dicts:
#         driver.add_cookie(i)
#     driver.refresh()

# def wait_for_login(driver: WebDriver):
#     elem = WebDriverWait(driver, 30).until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, '.list-group.list-group-flush'))
#     )
#     chat_list = driver.find_elements_by_class_name('list-group-item')
#     for chat in chat_list:
#         chat.click()
