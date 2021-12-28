from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from datetime import datetime, timedelta
from selenium.common.exceptions import StaleElementReferenceException
import csv
from selenium.webdriver.common.keys import Keys
import loginpass as lp
import time as t

driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

login_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'form[action*="/login/line?type=login"]'))
)
login_button.click()

wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input[name*="tid"]'))).send_keys(lp.EMAIL)
wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input[name*="tpasswd"]'))).send_keys(lp.PASS)
second_login_button = driver.find_element_by_class_name('MdBtn01')
second_login_button.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)

f = open("chat_log.csv", "w", encoding="utf-8")
writer = csv.writer(f)
chat_not_read = False

chat_list_window = driver.find_element_by_css_selector(
    '.flex-fill.overflow-y-auto')

while True:
    driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', chat_list_window)
    t.sleep(2)     # Wait to load the page.
    the_len = len(driver.find_elements_by_class_name('list-group-item'))
    print(the_len)
    if the_len > 300:
        break

chat_list = driver.find_elements_by_class_name('list-group-item')

for c in range(0, len(chat_list)):  # len(chat_list)
    if len(chat_list[c].find_elements_by_class_name('badge-pin')) >= 1:
        continue
        chat_not_read = True
    driver.implicitly_wait(2)
    try:
        chat_list[c].click()
        driver.implicitly_wait(1)
    except:
        break

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'chatsys'))
    )

    # ===each customer chat=====================================================
    print('------------------------')
    chat_window = driver.find_element_by_css_selector(
        '.p-3.h-100.overflow-y-auto')
    while True:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].offsetHeight;', chat_window)
        t.sleep(1)     # Wait to load the page.
        if (len(driver.find_elements_by_xpath("//*[text()='ผู้ใช้นี้เพิ่มคุณเป็นเพื่อนแล้ว']")) > 0):
            break

    list_chat_section = driver.find_elements_by_css_selector(
        '.chatsys-content, .chat-secondary, .chat-reverse')
    date_original = ''
    time_original = 'time_original'
    message_id = ''
    date = ''
    tags = set()
    customer_id = driver.current_url.split('/')[-1]
    cs_id = driver.find_elements_by_css_selector(
        '.chat-header')[-1].get_attribute('innerText')
    try:
        # for chat_section in list_chat_section:
        for i in range(0, len(list_chat_section)):  #
            # to avoid StaleElementReferenceException
            driver.implicitly_wait(1)
            message_type = ''
            message_text = ''
            if list_chat_section[i].get_attribute("class") == 'chatsys-content':
                date_original = list_chat_section[i].get_attribute(
                    'innerText')  # วันนี้ เมื่อวาน
                if(date_original.strip() == 'เมื่อวาน'):
                    date = (datetime.today() - timedelta(days=1)).date()
                elif(date_original.strip() == 'วันนี้'):
                    date = datetime.today().date()
                else:
                    try:
                        date_original = date_original.split(' ')[0]+list(const.THAI_MONTH.keys())[list(
                            const.THAI_MONTH.values()).index(date_original.split(' ')[1])]+str(datetime.now().year)
                        date = datetime.strptime(
                            date_original, '%d%m%Y').date()
                    except:
                        print('-')

            # CS
            elif 'chat-reverse' in list_chat_section[i].get_attribute("class"):
                list_message_bubble = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-body')
                sent_by = 'sale'
                cs_id = list_chat_section[i].find_element_by_css_selector('.chat-header').get_attribute(
                    'innerText')
                time_original = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-sub span')[-1].get_attribute('innerText')
                time = datetime.combine(date, datetime.strptime(
                    time_original, '%H.%M น.').time())
                for message_bubble in list_message_bubble:
                    message_id = message_bubble.get_attribute('data-id')
                    try:
                        message_type = 'text'
                        message_text = message_bubble.find_element_by_css_selector(
                            '.chat-item-text').get_attribute('innerText')
                    except:
                        message_type = 'not text'
                        message_text = ''
                    print(message_id, customer_id, sent_by,
                          message_type, message_text)
                    writer.writerow(
                        [message_id, customer_id, cs_id, sent_by, message_type, time, message_text])

            # customer
            elif 'chat-secondary' in list_chat_section[i].get_attribute("class"):
                list_message_bubble = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-body')
                sent_by = 'customer'
                # sender_id = driver.current_url
                # print(sender_id)
                time_original = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-sub span')[-1].get_attribute('innerText')
                time = datetime.combine(date, datetime.strptime(
                    time_original, '%H.%M น.').time())
                for message_bubble in list_message_bubble:
                    message_id = message_bubble.get_attribute('data-id')
                    try:
                        message_type = 'text'
                        message_text = message_bubble.find_element_by_css_selector(
                            '.chat-item-text').get_attribute('innerText')
                        for keyword in const.KEYWORDS_DICT:
                            # print('---------for keyword in const.KEYWORDS_DICT:')
                            if keyword in message_text:
                                # print('--------if keyword in message_text:')
                                tags.add(keyword)
                    except:
                        message_type = 'not text'
                        message_text = ''
                    print(message_id, customer_id, sent_by,
                          message_type, message_text)
                    writer.writerow([message_id, customer_id, cs_id, sent_by,
                                    message_type, time, message_text])

    #     # add tags

    #     # edit_tag_button = driver.find_elements_by_css_selector(
    #     #     '.mt-3 a')[-1]
    #     # edit_tag_button.click()
    #     # for tag in tags:
    #     #     wait.until(EC.element_to_be_clickable(
    #     #         (By.CSS_SELECTOR, 'input[name*="edit-tag-suggestions"]'))).send_keys(tag, Keys.RETURN)

    #     # if driver.find_element_by_class_name("btn-primary").is_enabled():
    #     #     driver.find_element_by_class_name("btn-primary").click()
    #     # else:
    #     #     close_button = driver.find_elements_by_css_selector(
    #     #         '.close')[-1]
    #     #     close_button.click()

    except StaleElementReferenceException as Exception:
        print('StaleElementReferenceException: so some messages will be skipped')

f.close()
