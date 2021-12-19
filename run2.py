from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from datetime import datetime, timedelta
from selenium.common.exceptions import StaleElementReferenceException
driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

login_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'form[action*="/login/line?type=login"]'))  # This is a dummy element
)
login_button.click()

wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input[name*="tid"]'))).send_keys(const.EMAIL)
wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input[name*="tpasswd"]'))).send_keys(const.PASS)
second_login_button = driver.find_element_by_class_name('MdBtn01')
second_login_button.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)
i = 0
chat_list = driver.find_elements_by_class_name('list-group-item')
chat_message_details = []
chat_text_freq_dict = []

# for chat in chat_list:  # iterate customers
for c in range(0, len(chat_list)):
    driver.implicitly_wait(2)  # to avoid StaleElementReferenceException
    current_chat_message_details = []
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
    list_chat_section = driver.find_elements_by_css_selector(
        '.chatsys-content, .chat-secondary, .chat-reverse')
    date_original = ''
    time_original = 'time_original'
    message_id = ''
    date = ''
    try:
        # for chat_section in list_chat_section:
        for i in range(2, len(list_chat_section)):
            # to avoid StaleElementReferenceException
            driver.implicitly_wait(3)
            sender_id = driver.current_url.split('/')[-1]
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
                    thaimonth = {
                        '01': 'ม.ค.',
                        '02': 'ก.พ.',
                        '03': 'มี.ค.',
                        '04': 'เม.ย.',
                        '05': 'พ.ค.',
                        '06': 'มิ.ย.',
                        '07': 'ก.ค.',
                        '08': 'ส.ค.',
                        '09': 'ก.ย.',
                        '10': 'ต.ค.',
                        '11': 'พ.ย.',
                        '12': 'ธ.ค.',
                    }
                    try:
                        date_original = date_original.split(' ')[0]+list(thaimonth.keys())[list(
                            thaimonth.values()).index(date_original.split(' ')[1])]+str(datetime.now().year)
                        date = datetime.strptime(
                            date_original, '%d%m%Y').date()
                    except:
                        print('-')
                        # print(date_original)

            if 'chat-reverse' in list_chat_section[i].get_attribute("class"):
                list_message_bubble = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-body')
                sent_by = 'sale'
                sender_id = '1234'
                for message_bubble in list_message_bubble:
                    message_id = message_bubble.get_attribute('data-id')
                    try:
                        message_type = 'text'
                        message_text = message_bubble.find_element_by_css_selector(
                            '.chat-item-text').get_attribute('innerText')
                    except:
                        message_type = 'not text'
                        message_text = ''
                time_original = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-sub span')[-1].get_attribute('innerText')
                print(message_id, sender_id, sent_by,
                      message_type, message_text)
                # current_chat_message_details.append({
                #     'message_id': message_id,
                #     'sender_id': sender_id,
                #     'sent_by': sent_by,
                #     'message_type': message_type,
                #     'message_text': message_type,
                #     'time': datetime.combine(date, datetime.strptime(time_original, '%H.%M น.').time()),
                # })

            if 'chat-secondary' in list_chat_section[i].get_attribute("class"):
                list_message_bubble = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-body')
                sent_by = 'customer'
                # sender_id = driver.current_url
                # print(sender_id)
                for message_bubble in list_message_bubble:
                    message_id = message_bubble.get_attribute('data-id')
                    try:
                        message_type = 'text'
                        message_text = message_bubble.find_element_by_css_selector(
                            '.chat-item-text').get_attribute('innerText')
                    except:
                        message_type = 'not text'
                        message_text = ''
                time_original = list_chat_section[i].find_elements_by_css_selector(
                    '.chat-sub span')[-1].get_attribute('innerText')
                print(message_id, sender_id, sent_by,
                      message_type, message_text)
                # current_chat_message_details.append({
                #     'message_id': message_id.split("/")[-1],
                #     'sender_id': sender_id,
                #     'sent_by': sent_by,
                #     'message_type': message_type,
                #     'message_text': message_text,
                #     'time': datetime.combine(date, datetime.strptime(time_original, '%H.%M น.').time()),
                # })
        # chat_message_details.append(current_chat_message_details)
        # print(chat_message_details)
    except StaleElementReferenceException as Exception:
        print('StaleElementReferenceException: so some messages will be skipped')
