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
i = 0
chat_list = driver.find_elements_by_class_name('list-group-item')
chat_text_dict = {}

for chat in chat_list:  # iterate customers
    try:
        chat.click()
        driver.implicitly_wait(1)
        print('-------------------------------okay')
    except:
        print('not okay------------------')
        break
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'chatsys'))
    )
    # customer_name = driver.find_element_by_tag_name('h4')
    customer_name = i
    chat_text_dict[customer_name] = []
    group_bubble_list = driver.find_elements_by_css_selector(
        '.chat-primary, .chat-secondary')
    # for group_bubble in group_bubble_list:  # iterate each customer chat
    bubble_list = driver.find_elements_by_css_selector('.chat-item-text')
    for bubble in bubble_list:
        print(bubble.get_attribute('innerText'))
        chat_text_dict[customer_name].append(
            bubble.get_attribute('innerText'))

    i += 1

print(chat_text_dict)
