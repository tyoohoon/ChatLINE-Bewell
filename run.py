from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

# func.bypass_login_with_cookies(driver)
# func.wait_for_login(driver)

elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)

chat_list = driver.find_elements_by_class_name('list-group-item')
for chat in chat_list:
    chat.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'chatsys'))
    )

    group_bubble_list = driver.find_elements_by_css_selector(
        '.chat-primary, .chat-secondary')
    for group_bubble in group_bubble_list:
        bubble_list = driver.find_elements_by_css_selector('.chat-item-text')
        for bubble in bubble_list:
            print('------------------')
            print(bubble.get_attribute('innerText'))
        break
