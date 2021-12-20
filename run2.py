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

driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

login_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'form[action*="/login/line?type=login"]'))
)
login_button.click()

wait = WebDriverWait(driver, 1)
# wait.until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, 'input[name*="tid"]'))).send_keys(lp.EMAIL)
# wait.until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, 'input[name*="tpasswd"]'))).send_keys(lp.PASS)
# second_login_button = driver.find_element_by_class_name('MdBtn01')
# second_login_button.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)

chat_list = driver.find_elements_by_class_name('list-group-item')

f = open("chat_log.csv", "w", encoding="utf-8")
writer = csv.writer(f)
chat_not_read = False
for c in range(0, len(chat_list)):
    if len(chat_list[c].find_elements_by_class_name('badge')) >= 1:
        chat_not_read = True
    # badge
    keyword_freq = {
        'hello0': 0,
        'hello1': 0,
    }
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
    list_chat_section = driver.find_elements_by_css_selector(
        '.chatsys-content, .chat-secondary, .chat-reverse')
    date_original = ''
    time_original = 'time_original'
    message_id = ''
    date = ''
    try:
        # for chat_section in list_chat_section:
        for i in range(0, len(list_chat_section)):
            # to avoid StaleElementReferenceException
            driver.implicitly_wait(1)
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
                    try:
                        date_original = date_original.split(' ')[0]+list(const.THAI_MONTH.keys())[list(
                            const.THAI_MONTH.values()).index(date_original.split(' ')[1])]+str(datetime.now().year)
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
                time = datetime.combine(date, datetime.strptime(
                    time_original, '%H.%M น.').time())
                print(message_id, sender_id, sent_by,
                      message_type, message_text)
                writer.writerow([message_id, sender_id, sent_by,
                                 message_type, message_text, time])
                # f.write(', '.join([message_id, sender_id, sent_by,
                #         message_type, message_text]))
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
                time = datetime.combine(date, datetime.strptime(
                    time_original, '%H.%M น.').time())
                print(message_id, sender_id, sent_by,
                      message_type, message_text)
                writer.writerow([message_id, sender_id, sent_by,
                                 message_type, message_text, time])

                for keyword in const.KEYWORDS:
                    if keyword in message_text:
                        if(keyword == 'สวัสดี'):
                            keyword_freq['hello0'] += 1
                        if(keyword == 'หวัดดี'):
                            keyword_freq['hello1'] += 1
                # f.write(', '.join([message_id, sender_id, sent_by,
                #         message_type, message_text]))
                # current_chat_message_details.append({
                #     'message_id': message_id.split("/")[-1],
                #     'sender_id': sender_id,
                #     'sent_by': sent_by,
                #     'message_type': message_type,
                #     'message_text': message_text,
                #     'time': datetime.combine(date, datetime.strptime(time_original, '%H.%M น.').time()),
                # })

            # add tags
        edit_tag_button = driver.find_elements_by_css_selector(
            '.mt-3 a')[-1]
        edit_tag_button.click()

        for freq in keyword_freq:
            if keyword_freq[freq] >= 1:
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[name*="edit-tag-suggestions"]'))).send_keys(freq, Keys.RETURN)
                if chat_not_read == True:
                    wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'input[name*="edit-tag-suggestions"]'))).send_keys('ยังไม่ได้อ่าน', Keys.RETURN)
                    chat_not_read = False
        if driver.find_element_by_class_name("btn-primary").is_enabled():
            driver.find_element_by_class_name("btn-primary").click()
        else:
            close_button = driver.find_element_by_css_selector(
                '.close')
            close_button.click()

        # chat_message_details.append(current_chat_message_details)
        # print(chat_message_details)

        # print(keyword_freq)
        keyword_freq = {
            'hello0': 0,
            'hello1': 0,
        }
    except StaleElementReferenceException as Exception:
        print('StaleElementReferenceException: so some messages will be skipped')

f.close()
