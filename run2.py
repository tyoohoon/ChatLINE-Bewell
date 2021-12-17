from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
import functions as func
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from datetime import datetime, timedelta
driver = webdriver.Chrome(
    executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
driver.get(const.BASE_URL)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.list-group.list-group-flush'))
)
i = 0
chat_list = driver.find_elements_by_class_name('list-group-item')
chat_text_dict = []
chat_text_freq_dict = []

for chat in chat_list:  # iterate customers
    message_details = []
    try:
        chat.click()
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
        '.chatsys-content, .chat-secondary, .chat-primary')
    date_original = ''
    time_original = 'time_original'
    message_id = ''
    date = ''

    for chat_section in list_chat_section:
        sender_id = driver.current_url.split('/')[-1]
        message_type = ''
        message_text = ''
        if chat_section.get_attribute("class") == 'chatsys-content':
            date_original = chat_section.get_attribute(
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
                    date = datetime.strptime(date_original, '%d%m%Y').date()
                except:
                    print('error------------------')
                    print(date_original)

        if chat_section.get_attribute("class") == 'chat chat-text-dark chat-reverse chat-primary':
            list_message_bubble = chat_section.find_elements_by_css_selector(
                '.chat-body')
            for message_bubble in list_message_bubble:
                sent_by = 'sale'
                sender_id = '1234'
                message_id = message_bubble.get_attribute('data-id')
                try:
                    message_type = 'text'
                    message_text = message_bubble.find_element_by_css_selector(
                        '.chat-item-text').get_attribute('innerText')
                except:
                    message_type = 'not text'
                    message_text = ''
            time_original = chat_section.find_elements_by_css_selector(
                '.chat-sub span')[-1].get_attribute('innerText')
            message_details.append({
                'message_id': message_id,
                'sender_id': sender_id,
                'sent_by': sent_by,
                'message_type': message_type,
                'message_text': message_text,
                'time': datetime.combine(date, datetime.strptime(time_original, '%H.%M น.').time()),
            })

        if chat_section.get_attribute("class") == 'chat chat-text-dark chat-secondary':
            list_message_bubble = chat_section.find_elements_by_css_selector(
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
            time_original = chat_section.find_elements_by_css_selector(
                '.chat-sub span')[-1].get_attribute('innerText')
            message_details.append({
                'message_id': message_id.split("/")[-1],
                'sender_id': sender_id,
                'sent_by': sent_by,
                'message_type': message_type,
                'message_text': message_text,
                'time': datetime.combine(date, datetime.strptime(time_original, '%H.%M น.').time()),
            })

    print(message_details)
    # time_origital = chat_section.find_elements_by_css_selector('.chat-sub span')[-1].get_attribute('innerHTML')
    # print(date_original)
    break
