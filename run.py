from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import datetime

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
chat_text_freq_dict = {}

# ==calculate response rate by (num green badge)/(num all chat)===================================
green_badge = driver.find_elements_by_css_selector(
    '.badge.badge-pin.badge-primary.border-0')
print('response rate:')
print(1-len(green_badge)/len(chat_list))
# print(len(green_badge))
# print(len(chat_list))
# ------------------------------------------------------------------------------------------------

for chat in chat_list:  # iterate customers
    try:
        chat.click()
        driver.implicitly_wait(1)
    except:
        break
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'chatsys'))
    )
    # customer_name = driver.find_element_by_tag_name('h4')
    customer_name = i
    chat_text_dict[customer_name] = []

    # ===each customer chat=====================================================
    bubble_list = driver.find_elements_by_css_selector('.chat-item-text')
    for bubble in bubble_list:
        chat_text_dict[customer_name].append(
            bubble.get_attribute('innerText'))
    # -----------------------------------------------------------------------

    # ===calculate keyword freq=====================================================
    chat_text_freq_dict[customer_name] = {}
    for tag in ['สวัสดี', 'หวัดดี']:
        chat_text_freq_dict[customer_name][tag] = ' '.join(
            chat_text_dict[customer_name]).count(tag)
    # ----------------------------------------------------------------------------
    i += 1
print(chat_text_freq_dict)
print(chat_text_dict)


# == avg response time ============================================================================
isCus = False
number_of_time_intervals = 0
sum_of_time_intervals = 0
customer_sent_time = ''
sale_sent_time = ''

all_sent_time = driver.find_elements_by_css_selector(
    '.chat-secondary span, .chat-primary span')  # also contains 'อ่านแล้ว'

# ------------------------------------------------------------------------------------------------
