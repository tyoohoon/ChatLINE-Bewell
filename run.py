from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)

chat_list = driver.find_elements_by_class_name('list-group-item')
chat_text_dict = {}
i = 0
print(type(chat_list))
print(len(chat_list))
for chat in chat_list:  # iterate customers
    chat.click()
    # customer_name = driver.find_element_by_css_selector(
    #     'h4.mb-0.text-truncate')[0].innerText
    customer_name = i
    chat_text_dict[customer_name] = []
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'chatsys'))
    )
    group_bubble_list = driver.find_elements_by_css_selector(
        '.chat-primary, .chat-secondary')
    for group_bubble in group_bubble_list:  # iterate each customer chat
        bubble_list = driver.find_elements_by_css_selector('.chat-item-text')
        for bubble in bubble_list:
            chat_text_dict[customer_name].append(
                bubble.get_attribute('innerText'))
    i += 1
    if (i == 7):
        break

print(chat_text_dict)
